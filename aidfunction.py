import csv
from datetime import datetime
# from warmtepomp import *
import os
from scipy.optimize import brute


class dynamic_device:
    def __init__(self,name,duration,deadline=None,watt=None,first_time=True):
        #de "=...." is voor het geval er niks wordt ingegeven, worden deze waarden gebruikt
        if watt==None:
            self.__watt=get_wattage(number_meter)
            #houdt in dat wanneer er nog geen wattage gekend is, bv nieuw toestel -> gaat een eerste opmeting doen via
            #  speciale stekker, niet nodig voor het verdere programma, enkel voorbeeld vr uiteindelijk product
        else:
            self.__watt=watt
            #anders is het device zijn wattage hetgene wat er in de database is opgeslagen/ wordt ingegeven
        self.__duration=duration
        #duur van een gebruikscyclus van het toestel
        self.__deadline=deadline
        #dag waartegen het uitgevoerd moet worden, op dit moment nog geen uurlijkse deadline, nog in ontwikkeling
        self.__name=name
        self.__first_time=first_time
    def get_name(self):
        return self.__name
    def get_watt(self):
        return self.__watt
    def get_duration(self):
        return self.__duration//15
    #duration oorspronkelijk in minuten -> kwartieren dus delen door 15
    def get_deadline(self):
        return self.__deadline
    def add_deadline(self,new_deadline):
        self.__deadline= new_deadline
    def change_wattage(self,new_wattage):
        self.__watt=new_wattage
    def start_time(self,time):
        self.__start_time=time
        #kent een starttijd toe aan het device, GEBRUIKEN WE DIT??????????????????????????????????????????????????????????????????????????????

class battery:
    def __init__(self,max_wattage,max_capacity,loss=0,current_capacity=0):
        #max wattage is de maximale snelheid waaraan de batterij kan opladen/energie leveren
        # max capacity is de maximale hoeveelheid energie die er op 1 moment opgeslagen kan zijn
        #loss is de verliesfactor, de batterij kan niet de energie die die gebruikt om op te laden, volledig terug afgeven

        self.__max_capacity=max_capacity
        self.__max_wattage= max_wattage
        self.__loss=loss
        self.__current_capacity=current_capacity
    def get_current_capacity(self):
        return self.__current_capacity
    def get_loss(self):
        return self.__loss
    def get_max_wattage(self):
        return self.__max_wattage
    def get_max_capacity(self):
        return self.__max_capacity
    def update_current_capacity(self,addition):
        new_capacity=self.get_current_capacity()+addition
        #verhoogt de capaciteit met de additional energy als de batterij oplaadt of ontlaadt
        self.__current_capacity=new_capacity

def total_consumption(X,devices):
    #stelt een lijst op met het verbruik per kwartier, uitgaande van X (de starttijden van de verplaatsbare devices,
    # en devices, waar de specificaties aangekoppeld zijn (via de klasse)
    #X en devices zijn in dezelfde volgorde -> eerste elem van X is de starttijd van eerste device in devices
    consumption=[]

    for i in range(0,96):
        consumption.append(0)
        #gaat al de juiste lengte maken voor lijst, met kwartier 0 tot en met 95
    for dev_index in range(0,len(devices)):
        #gaat elk device af, door dit via een index te doen kan men ineens ook de starttijd via dit nummer oproepen
        #dit in tegenstelling tot "for device in devices" waar het device wel gekend is, maar niet de starttijd
        #voor elk device apart wordt in de binnenste forloop het verbuik aan de lijst toegevoegd
        #na afloop van deze forloop zijn alle devices overlopen en is het totale verbuik die dag in de lijst per kwartier
        dev=devices[dev_index]
        #gaat telkens het device selecteren om de specificaties te kunnen oproepen
        watt=dev.get_watt()
        #wattage van het geselecteerde device
        duration=dev.get_duration()
        start_time=X[dev_index]
        #via de index is elk device aan de juiste starttijd gekoppeld (zelfde index)
        for x in range(0,duration):
            #voor dit device wordt gedurende de hele gebruiksduur (tot duration-1), per kwartier het wattage toegevoegd aan het verbruik
            #waarom duration-1? (range telt 2e grens niet meer bij)-> bv. duur=2 kwartieren-> kwartier 0 en kwartier 1
            consumption[int(start_time)+x]+=watt
            #de verbruikslijst wordt verhoogd met het wattage van de verbruiker, op het interval [starttijd,starttijd+duur-1]
    return consumption

def optimalisation(devices,remaining_energy,battery=False):
    """

    :param devices: a list containing dynamic device  objects
    :param remaining_energy: a function representing the available energy with as argument time in unit of quarter
    :param battery: either False if there is no battery, or the name of a battery object
    :return: if there is no battery, the function returns a list containing:
                as first argument a list of start times in the same order as the list of devices
                as second argument a function that gives what still remains of the energy after applying the optimisation
            if there is a battery, this result is appended with:
                a list of quarters in which the battery charges
                a list of quarters in which the battery is discharging
    """

    to_minimize=lambda  y:total(subtract_vector(remaining_energy,total_consumption(y,devices),True))
    #dit is hetgene dat uiteindelijk zo minimaal mogelijk moet zijn: de som (total) van de afwijkingen per kwartier, TRUE geeft aan dat het telkens in absolute waarde wordt berekend
    #aangezien de energie zo optimaal mogelijk benut moet worden, moet er zo weinig mogelijk energie van en naar het net moet vloeien
    #dit wordt weergegeven door de beschikbare energie per kwartier af te trekken van het verbruik,
    # de positieve stukken zijn energieoverschotten, de negatieve zijn energietekorten(stroom van net) -> tekening indien onduidelijk
    #aangezien in het beste geval deze beiden zo klein mogelijk moeten zijn, nemen we de absolute waarde, anders zouden deze elkaar kunnen opheffen
    #is een lambdafunctie omdat dit moet geoptimaliseerd worden, de waarde is afhankelijk van de starttijdenmatrix y

    x_bounds=[]
    #hier worden grenzen voor de starttijd opgeslagen, bv door deadlines

    for device in devices:
        #gaat voor elk device in de volgorde van de deviceslijst een uiterste starttijd opgeven
        x_bounds.append(slice(0,97-device.get_duration()))
        #waarom 97 -> gemakkelijk na te gaan met voorbeeld: device met duur van 2 kwartieren -> ten laatste kwartier 94 en 95 -> uiterste starttijd 94
        #de grens in dit geval is 97-2=95 wat bij de slice niet meer erbijgenomen wordt dus 94
        #@EMIEL: werkt dit met "slice", ipv gwn een tuple (begin, einde)???????????????????????????????????????????????????????????????????????????????????????????????????????????????
        #@EMIEL2: uurlijkse deadlines lijken mij hier ook gewoon ingevoerd te kunnen worden
    x_bounds=tuple(x_bounds)

    res= brute(to_minimize,x_bounds,full_output=True)
    #gaat de functie "to minimize" minimaliseren, en dus de optimale starttijdenmatrix y zoeken,
    # waarbij de oplossing y zal voldoen aan de opgegeven x_bounds
    #"brute" is een optimalisatiefunctie via een externe python module


    new_remaining_energy=subtract_vector(remaining_energy,total_consumption(res[0],devices),False)
    #de overgebleven energie per kwartier na optimalisatie is het vectorverschil van enerzijds remaining energy en anderzijds de lijst van totale vebruik uitgaande van de optimale startijden
    #res[0] is hier de starttijdenmatrix, die uit de optimalisatie voortkwam, de optimalisatie was opgeslagen onder res en geeft verschillende dingen terug, vandaar de indexing
    # radiator.apply_heating(new_remaining_energy,get_outside_temp())# deze statement returnt niks maar past het argument new_remaining_energy aan
    if  battery==False:

        return [res[0],new_remaining_energy]
    else:
        #als er een batterij is, kan die bijkomende afwijkingen wegwerken
        charging=[]
        discharging=[]
        max_cap=battery.get_max_capacity()
        max_watt = battery.get_max_wattage()
        output_efficiency = 1-battery.get_loss()
        #dit zijn allemaal systeemkarakteristieken, die niet gewijzigd worden doorheen de dag
        #we gebruiken de loss hier in het geval dit verlies aan de ontlading van de batterij gebeurt
        for t in range(0,96):
            usage_at_t=new_remaining_energy[t]
            #gaat op elk kwartier van de dag kijken of er een overschot(+) of een tekort(-) is aan energie
            current_cap=battery.get_current_capacity()
            #op elk kwartier wordt de huidige capciteit opnieuw opgevraagd
            if usage_at_t>0:
                #overschot aan energie
                if usage_at_t<max_watt:
                    #het overschotwattage overschrijdt de maximale oplaadsnelheid niet en alle energie kan opgenomen worden poor de batterij
                    if current_cap<=(max_cap-(usage_at_t*0.25/1000)):
                     #gedurende het hele kwartier kan er opgeladen worden, zonder dat de batterij volgeraakt, *0.25/1000 is om het wattage om te zetten in kWh (max cap in kWh)
                        charging.append(t)
                     #dit kwartier gaat de batterij opladen
                        battery.update_current_capacity(usage_at_t * 0.25 / 1000)
                     #de energie (wattage*hoeveelheid uur /1000) wordt aan de batterij toegevoegd
                        new_remaining_energy[t]-=usage_at_t
                        #in de lijst met energieafwijkingen per kwartier, wordt op het bekeken kwartier het overschot verminderd (deze energie gaat nr de batterij)
                elif usage_at_t>=max_watt:
                    #de batterij kan niet snel genoeg opladen om alle overschot op te nemen
                    if current_cap<=(max_cap-(max_watt*0.25/1000)):
                        # de batterij kan gedurende het hele kwartier aan maximumsnelheid opladen
                        charging.append(t)
                        battery.update_current_capacity(max_watt*0.25/1000)
                        new_remaining_energy[t]-=max_watt
            elif usage_at_t<0:
                #er is een tekort aan energie
                if abs(usage_at_t)<max_watt:
                    #het nodige wattage valt binnen de leversnelheid van de batterij (batterij kan maar met bepaalde snelheid/wattage ontladen)
                    if current_cap>=(abs(usage_at_t)*0.25/1000/output_efficiency):
                        #de batterij heeft genoeg energie om de energie dat kwartier te leveren, HIER MOET OOK NOG DE VERLIESFACTOR BIJKOMEN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        discharging.append(t)
                        #de batterij ontlaadt
                        battery.update_current_capacity(usage_at_t*0.25/1000/output_efficiency)
                        #de energie wordt uit de batterij gehaald (usageatt is negatief dus aftrekking) hierbij wordt rekening gehouden met het verlies
                        #ontvangen=efficientie*uitgaand-> uitgaand = ontvangen(benodigde)/efficientie
                        new_remaining_energy[t]-=usage_at_t
                        #het tekort wordt aangevuld met energie van de batterij
                elif abs(usage_at_t)>=max_watt:
                    #de batterij zou meer moeten leveren dan de maximumsnelheid
                    if current_cap>=(max_watt*0.25/1000/output_efficiency):
                        #VERLIESFACTOR ONTBREEKT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        discharging.append(t)
                        battery.update_current_capacity(-1*max_watt*0.25/1000/output_efficiency)
                        new_remaining_energy[t]+=max_watt




        return [res[0],new_remaining_energy,charging,discharging]




#de te minimaliseren functie is van de vorm int(abs(f(x)-w(x)))
    # met f(x) de opbrengst en w(x) de verbruike

def get_starting_energy(efficiency_matrix, watt_piek, angle, orientation_south_offset, data_matrix):
    #gaat de opgewekte enrgie van die dag berekenen op basis van verschillende parameters
    #de voorspelling houdt rekening met de orientatie(orientation) en dakhelling(angle) via de efficiency matrix
    #energievoorspelling is gebaseerd op aantal watpiek van de installatie
    angle_index= angle//10
    #zie tabel met efficientie -> invloed van dakhelling per 10° (rijen)
    orientation_index=(orientation_south_offset+90//15)
    #kolomnummer in efficiencymatrix afhankelijk van orientatie dak
    effeciency=1.35*efficiency_matrix[angle_index][orientation_index]/100
    #factor 1.35 is erbijgezet omdat het aantal wattpiek berekend is voor op een plat dak, de nieuwe standaard wordt hier op 30/35° gelegd

    starting_energy=[]
    for data in data_matrix:
#voor de stralingsgegevens (per kwartier) in de datamatrix wordt de bijbehorende energieopbrengst berekend
        starting_energy.append(data[2] * watt_piek*effeciency)
    return starting_energy

def open_file_csv(pad_naar_file):
    #niet belangrijk voor optimalisatie zelf, opent de databestanden in de gewenste vorm
    #ken ik zelf niet veel van
    path = pad_naar_file
    file = open(path,newline="")
    read = csv.reader(file)

    header = next(read)

    data = []

    for row in read:
        #rij per rij behandeld
        row1 = str(row)
        #de tekst van een regel wordt opgeslagen

        irradiance_str = row1[20:len(row1) - 3]
        #de irradiantie wordt uit de file gehaald (deel na de tijd en datum)
        if len(irradiance_str)==0:
            #er is geen informatie betreffende de irradiantie terug te vinden
            irradiance_int = 0
        else:
            irradiance_int = int(irradiance_str[0:len(irradiance_str)])
            #de effectieve waarde van de irradiantie wordt opgeslagen

        date_and_time = row1[2:18]
        if date_and_time == "\\n']":
            date = 0
        else:
            date = datetime.strptime(date_and_time,'%Y-%m-%d %H:%M')
            #het moment wordt in de geweenste vorm gezet via module datetime
        data.append([date,irradiance_int])
        #de tijdstippen met bijbehorende irradianties worden in een matrix door de functie teruggegeven
    file.close()
    return data

def matrix_kwartieren(datamatrix):
    #gaat de matrix met irradianties omzetten in een matrix per kwartier, de gegevens zijn in de oorspronkelijke file per 5 min
    k = len(datamatrix)
    t = 0
    data = []
    #maakt een neiuwe lege lijst waar de irradianties per kwartier gaan komen
    while t<k:
        date = datamatrix[t][0]
        #het tijdstip wordt overgenomen per kwartier (3 intervallen van 5 min, zie hieronder t+3)
        average_radiation = int((datamatrix[t][1]+datamatrix[t+1][1]+datamatrix[t+2][1])//3)
        #gedurende dit interval wordt de bestraling genomen als het gemiddelde over de 3 intervallen van 5 min
        referentie = average_radiation/1000
        data.append([date,average_radiation,referentie])
        t = t+3
        #dit wordt per kwartier gedaan dus worden er 2 intervallen van 5 min overgeslaan, totdat alle tijdstippen uit de oorspronkelijke file behandeld zijn

    return data

effeciency_matrix=[
    [90,90,90,90,90,90,90,90,90,90,90,90,90],
    [89,91,92,94,95,95,96,95,95,94,93,91,90],
    [87,90,93,96,97,98,98,98,97,96,94,91,88],
    [86,89,93,96,98,99,100,100,98,96,94,90,86],
    [82,86,90,95,97,99,100,99,98,96,92,88,84],
    [78,84,88,92,95,96,97,97,96,93,89,85,80],
    [74,79,84,87,90,91,93,93,92,89,86,81,76],
    [69,74,78,82,85,86,87,87,86,84,80,76,70],
    [63,68,72,75,77,79,80,80,79,77,74,69,65],
    [56,60,64,67,69,71,71,71,71,69,65,62,58]
    ]
#dit is de matrix die rekening houd met de helling (rijen) en orientatie(kolom) overgetypt om deze te kunnen gebruiken in de berekeningen

def subtract_vector(matrix1,matrix2,absolute=False):
    #trekt twee vectoren van elkaar af, en geeft het resultaat als een nieuwe vector met al dan niet de absolute waarde van de afwijkingen
    result = []
    if absolute:
        for index in range(0,len(matrix1)):

            result.append(abs(matrix1[index]-matrix2[index]))

    else:
        for index in range(0,len(matrix1)):
            result.append(matrix1[index]-matrix2[index])

    return result

def total(vector):
    #berekend de som van alle elementen van een vector
    sum=0
    for x in vector:
        sum+=x
    return sum

def simulation(dag,soort_verbruiker,watt_piek,battery=False,angle=35,s_offset=0,efficiency_matrix=effeciency_matrix ):
    #voorlopig zonder deadlines met deadlines werken moet consumption aangepast worden
    #brengt alles samen om  voor een bepaalde situatie een beeld te scheppen vn het systeem
    """

    :param dag: dag1 of dag2 ..of dag6 als string
    :param soort_verbruiker: gem of zuinig als string
    :return:
    """
    dir = os.path.dirname(__file__)
    #gaat de locatie van het bestand opslaan om de bijbehorende files  te kunnen opsporen vanaf daar
    standard_usage_path= dir+"/data/verbruiksprofiel_"+soort_verbruiker+".csv"
    #geeft de locatie van de file met het vast verbruik van de opgegeven verbruiker
    #@EMIEL: zouden we de vaste verbruikers ook niet een klasse  geven, of zoals hier iedereen klassificeren onder de mogelijkheden, anders kunnen we ervan uitgaan dat die file telkens wordt opgesteld voor de specifieke verbruiker?????????????????????????????????????????????????????????????????????????????????????
    #nieuw device wordt eerst in de aparte files toegevoegd
    dynamic_devices_path=dir+"/data/verplaatsbaar_"+soort_verbruiker+".csv"
    #analoog
    day_forcast=dir+"/data/"+dag+".csv"
    #pad naar voorspelling van die dag
    standard_usage_file= open(standard_usage_path,newline='')
    standard_usage_reader=csv.reader(standard_usage_file)
    standard_usage_list=[]
    next(standard_usage_reader)
    for row in standard_usage_reader:
        #gaat per kwartier het standaardverbruik weergeven, de hele dag wordt een lijst van standaardverbruiken
        #dit zijn de vaste verbruikers
        standard_usage_list.append(float(row[1]))
    standard_usage_file.close()

    dat = open_file_csv(day_forcast)
    day_forcast=matrix_kwartieren(dat)
    #day_forecast geeft nu de stralingsvoorspelling van de energyvillefiles per kwartier weer in een enkele lijst


    dynamic_devices_file= open(dynamic_devices_path,newline='')
    dynamic_devices_reader=csv.reader(dynamic_devices_file)
    dynamic_devices_list=[]
    next(dynamic_devices_reader)
    for row in dynamic_devices_reader:
        #de dynamic devices van de verbruiker worden geimporteerd
        dynamic_devices_list.append(dynamic_device(row[0],int(row[2]),watt=int(row[1])))
        #voor elk van de devices wordt een object gecreeerd
    dynamic_devices_file.close()

    starting_energy=get_starting_energy(efficiency_matrix,watt_piek,angle,s_offset,day_forcast)
    original_energy= starting_energy.copy()
    # gaat een energieproductievoorspelling maken voor de situatie

    remaining_energy=subtract_vector(starting_energy,standard_usage_list)
    #de energie waarmee geoptimaliseerd kan worden is het overschot van de opgewekte energie zonder het standaardverbruik


    return [optimalisation(dynamic_devices_list,remaining_energy,battery),original_energy]
    #gaat hierop optimaliseren en returnt dus de starttijden, het overschot aan energie en mogelijks de oplaad- en ontlaadtijden

"""
To do:
deadlines
warmtepomp

Opmerkingen:
hoe voegen we de verbruikers toe?
is die via de gui kiezen vast/verplaatsbaar/continu
en dit dan rechtstreeks in de datafiles aanpassen lijkt mij het gemakkelijkste

ik zou zonder dagelijkse deadline werken en enkel met uurlijkse, dagelijkse maakt het te ingewikkeld
 aangezien je dan moet kunnen grenzen trekken die heel abstract kunnen zijn rekening houdend met de batterij
 uiteindelijk zijn er realistisch niet zo veel toestellen met een dagelijkse deadline
 een uurlijkse zou wel gemakkelijk moeten lukken, door de boundaries aan te passen
"""

