import csv
from datetime import datetime
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import interp1d
import scipy.integrate as integrate
import os
from scipy.optimize import brute


class dynamic_device:
    def __init__(self,name,duration,deadline=None,watt=None,first_time=True):
        if watt==None:
            self.__watt=get_wattage(number_meter)#bla de die bla
        else:
            self.__watt=watt
        self.__duration=duration
        self.__deadline=deadline
        self.__name=name
        self.__first_time=first_time
    def get_name(self):
        return self.__name
    def get_watt(self):
        return self.__watt
    def get_duration(self):
        return self.__duration//15
    def get_deadline(self):
        return self.__deadline
    def add_deadline(self,new_deadline):
        self.__deadline= new_deadline
    def change_wattage(self,new_wattage):
        self.__watt=new_wattage
    def start_time(self,time):
        self.__start_time=time

class battery:
    def __init__(self,max_wattage,max_capacity,loss=0,current_capacity=0):
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

        self.__current_capacity=new_capacity

def total_consumption(X,devices):
    consumption=[]

    for i in range(0,96):
        consumption.append(0)
    for dev_index in range(0,len(devices)):
        dev=devices[dev_index]
        watt=dev.get_watt()
        duration=dev.get_duration()
        start_time=X[dev_index]
        for x in range(0,duration):
            consumption[int(start_time)+x]+=watt
    return consumption

def optimalisation(devices,remaining_energy, starting_energy, battery=False):
    """

    :param devices: a list containing dynamic device  objects
    :param remaining_energy: a function repesenting the available energy with as argument time in unit of quarter
    :param battery: either False if there is no battery or the name of a battery object
    :return: if there is no battery it returns a list containing:
                as first argument a list of start times in the same order as the list of devices
                as second argument a function that gives what still remains of the energy after apllying the optimisation
            if there is a battery this appended with:
                a list of quarters in which the battery charges
                a list of quarters in which the battery is discharging
    """

    to_minimize=lambda  y:total(subtract_vector(remaining_energy,total_consumption(y,devices),True))
    x_bounds=[]

    for device in devices:
        x_bounds.append(slice(0,97-device.get_duration()))

    x_bounds=tuple(x_bounds)

    res= brute(to_minimize,x_bounds,full_output=True)


    new_remaining_energy=subtract_vector(remaining_energy,total_consumption(res[0],devices),False)
    if  battery==False:

        return [res[0],new_remaining_energy, starting_energy]
    else:
        charging=[]
        discharging=[]
        max_cap=battery.get_max_capacity()
        max_watt = battery.get_max_wattage()
        output_efficiency = 1-battery.get_loss()
        for t in range(0,96):
            usage_at_t=new_remaining_energy[t]
            current_cap=battery.get_current_capacity()
            if usage_at_t>0:
                if usage_at_t<max_watt:
                    if current_cap<=(max_cap-(usage_at_t*0.25/1000)):
                        charging.append(t)
                        battery.update_current_capacity(usage_at_t * 0.25 / 1000)
                        new_remaining_energy[t]-=usage_at_t
                elif usage_at_t>=max_watt:
                    if current_cap<=(max_cap-(max_watt*0.25/1000)):
                        charging.append(t)
                        battery.update_current_capacity(max_watt*0.25/1000)
                        new_remaining_energy[t]-=max_watt
            elif usage_at_t<0:
                if abs(usage_at_t)<max_watt:
                    if current_cap>=(abs(usage_at_t)*0.25/1000):
                        discharging.append(t)
                        battery.update_current_capacity(usage_at_t*0.25/1000/output_efficiency)
                        new_remaining_energy[t]-=usage_at_t
                elif abs(usage_at_t)>=max_watt:
                    if current_cap>=(max_watt*0.25/1000):
                        discharging.append(t)
                        battery.update_current_caoacity(-1*max_watt*0.25/1000/output_efficiency)
                        new_remaining_energy[t]+=max_watt



            # if usage_at_t>0 and current_cap<= max_cap-usage_at_t*0.25/1000 and usage_at_t<max_watt :#als max capaciteit gegeven is in kwh
            #     charging.append(t)
            #     battery.update_current_capacity(usage_at_t*0.25/1000)
            #     new_remaining_energy[t]-=usage_at_t
            #
            #
            # elif usage_at_t>0 and current_cap<= max_cap-max_watt*0.25/1000 and usage_at_t> max_watt:
            #     charging.append(t)
            #     new_remaining_energy[t]-=usage_at_t
            #     battery.update_current_capacity(max_watt * 0.25 / 1000)
            #
            # elif usage_at_t <0 and -1*usage_at_t>=max_watt and current_cap*output_efficiency>=max_watt*0.25/1000:
            #     discharging.append(t)
            #     new_remaining_energy[t]+=max_watt
            #     battery.update_current_capacity(-max_watt * 0.25 / 1000/output_efficiency)
            #
            # elif usage_at_t < 0 and -1 * usage_at_t < max_watt and current_cap*output_efficiency >= usage_at_t * 0.25 / 1000:
            #     discharging.append(t)
            #     new_remaining_energy[t]-=usage_at_t
            #     battery.update_current_capacity(usage_at_t * 0.25 / 1000/output_efficiency)
            # print(battery.get_current_capacity())
        return [res[0],new_remaining_energy,charging,discharging]




#de te minimaliseren functie is van de vorm int(abs(f(x)-w(x)))
    # met f(x) de opbrengst en w(x) de verbruike

def get_starting_energy(effeciency_matrix, watt_piek, angle, orientation_south_offset, data_matrix):
    angle_index= angle//10
    orientation_index=orientation_south_offset+90//15
    effeciency=1.35*effeciency_matrix[angle_index][orientation_index]/100
    starting_energy=[]
    for data in data_matrix:

        starting_energy.append(data[2] * watt_piek*effeciency)
    return starting_energy

def open_file_csv(pad_naar_file):
    path = pad_naar_file
    file = open(path,newline="")
    read = csv.reader(file)

    header = next(read)

    data = []

    for row in read:
        row1 = str(row)

        irradiance_str = row1[20:len(row1) - 3]
        if len(irradiance_str)==0:
            irradiance_int = 0
        else:
            irradiance_int = int(irradiance_str[0:len(irradiance_str)])

        date_and_time = row1[2:18]
        if date_and_time == "\\n']":
            date = 0
        else:
            date = datetime.strptime(date_and_time,'%Y-%m-%d %H:%M')
        data.append([date,irradiance_int])
    file.close()
    return data

def matrix_kwartieren(datamatrix):
    k = len(datamatrix)
    t = 0
    data = []
    while t<k:
        date = datamatrix[t][0]
        average_radiation = int((datamatrix[t][1]+datamatrix[t+1][1]+datamatrix[t+2][1])//3)
        referentie = average_radiation/1000
        data.append([date,average_radiation,referentie])
        t = t+3

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

def subtract_vector(matrix1,matrix2,absolute=False):
    result = []
    if absolute:
        for index in range(0,len(matrix1)):

            result.append(abs(matrix1[index]-matrix2[index]))

    else:
        for index in range(0,len(matrix1)):
            result.append(matrix1[index]-matrix2[index])

    return result

def total(vector):
    sum=0
    for x in vector:
        sum+=x
    return sum

def simulation(dag,soort_verbruiker,watt_piek, dynamic_devices_list, battery=False,angle=35,s_offset=0,efficiency_matrix=effeciency_matrix ):#voorlopig zonder deadlines met deadlines werken moet consumption aangepast worden
    """

    :param dag: dag1 of dag2 ..of dag6 als string
    :param soort_verbruiker: gem of zuinig als string
    :return:
    """
    dir = os.path.dirname(__file__)
    standard_usage_path= dir+"/data/verbruiksprofiel_"+soort_verbruiker+".csv"
    dynamic_devices_path=dir+"/data/verplaatsbaar_"+soort_verbruiker+".csv"
    day_forcast=dir+"/data/"+dag+".csv"
    standard_usage_file= open(standard_usage_path,newline='')
    standard_usage_reader=csv.reader(standard_usage_file)
    standard_usage_list=[]
    next(standard_usage_reader)
    for row in standard_usage_reader:
        standard_usage_list.append(float(row[1]))
    standard_usage_file.close()

    dat = open_file_csv(day_forcast)
    day_forcast=matrix_kwartieren(dat)


    # dynamic_devices_file= open(dynamic_devices_path,newline='')
    # dynamic_devices_reader=csv.reader(dynamic_devices_file)
    #dynamic_devices_list=[]#insert_devices
    # next(dynamic_devices_reader)
    # for row in dynamic_devices_reader:
    #     dynamic_devices_list.append(dynamic_device(row[0],int(row[2]),watt=int(row[1])))
    # dynamic_devices_file.close()

    starting_energy=get_starting_energy(efficiency_matrix,watt_piek,angle,s_offset,day_forcast)

    remaining_energy=subtract_vector(starting_energy,standard_usage_list)


    return optimalisation(dynamic_devices_list,remaining_energy, starting_energy, battery)