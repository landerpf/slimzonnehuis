from aidfunction import*
# thermiscje_conductie=0.04 #mineraal wol
# dikte=0.18 #dikte in meter
# cop=3.25
def simulatie_zonder_batterij(dagen,soort_verbruiker,watt_piek,battery=False,angle=35,s_offset=0,efficiency_matrix=effeciency_matrix ):

    dir = os.path.dirname(__file__)

    standard_usage_path= dir+"/data/verbruiksprofiel_"+soort_verbruiker+".csv"

    dynamic_devices_path=dir+"/data/verplaatsbaar_"+soort_verbruiker+".csv"



    standard_usage_file= open(standard_usage_path,newline='')
    standard_usage_reader=csv.reader(standard_usage_file)
    standard_usage_list=[]
    next(standard_usage_reader)
    for row in standard_usage_reader:

        standard_usage_list.append(float(row[1]))
    standard_usage_file.close()



    dynamic_devices_file= open(dynamic_devices_path,newline='')
    dynamic_devices_reader=csv.reader(dynamic_devices_file)
    dynamic_devices_list=[]
    next(dynamic_devices_reader)
    for row in dynamic_devices_reader:

        dynamic_devices_list.append(dynamic_device(row[0],int(row[2]),watt=int(row[1])))

    dynamic_devices_file.close()

    file = open("simulatie"+soort_verbruiker+".txt", "w")
    file.write("opbrengst,norm_stort,norm_trekken,opti_stort,opti_trek\n")

    for x in range(1,dagen+1): #aantal dagen da ik ga testen klaar zetten met naam gewoon een cijfer
        day_forcast = dir + "/data/" + str(x) + ".csv"
        dat = open_file_csv(day_forcast)
        day_forcast = matrix_kwartieren(dat)

        starting_energy=get_starting_energy(efficiency_matrix,watt_piek,angle,s_offset,day_forcast)
        original_energy= total(starting_energy)*0.25/1000#totale opgewekte energie door zonnen panelen inkwh

        remaining_energy=subtract_vector(starting_energy,standard_usage_list)
        total_remaining_energy=total_pos_neg(remaining_energy)
        normaal_van_net=total_remaining_energy[1]*0.25/1000+0.17+1+2.4#*0.25/1000+0.19+1.9+2.4 dit voor gem, +0.17+1+2.4 dit voor zuinig
        normaal_op_net=total_remaining_energy[0]*0.25/1000
        optimized=optimalisation(dynamic_devices_list, remaining_energy, battery)[1]
        total_optimal=total_pos_neg(optimized)
        opti_van_net=total_optimal[1]*0.25/1000
        opti_op_net=total_optimal[0]*0.25/1000
        file.write(str(original_energy)+","+str(normaal_op_net)+","+str(normaal_van_net)+','+str(opti_op_net)+','+str(opti_van_net)+'\n')

    file.close()

def simulatie_met_batterij(dagen,soort_verbruiker,watt_piek,battery=False,angle=35,s_offset=0,efficiency_matrix=effeciency_matrix ):

    dir = os.path.dirname(__file__)

    standard_usage_path= dir+"/data/verbruiksprofiel_"+soort_verbruiker+".csv"

    dynamic_devices_path=dir+"/data/verplaatsbaar_"+soort_verbruiker+".csv"



    standard_usage_file= open(standard_usage_path,newline='')
    standard_usage_reader=csv.reader(standard_usage_file)
    standard_usage_list=[]
    next(standard_usage_reader)
    for row in standard_usage_reader:

        standard_usage_list.append(float(row[1]))
    standard_usage_file.close()



    dynamic_devices_file= open(dynamic_devices_path,newline='')
    dynamic_devices_reader=csv.reader(dynamic_devices_file)
    dynamic_devices_list=[]
    next(dynamic_devices_reader)
    for row in dynamic_devices_reader:

        dynamic_devices_list.append(dynamic_device(row[0],int(row[2]),watt=int(row[1])))

    dynamic_devices_file.close()

    file = open("simulatie"+soort_verbruiker+"batterij"+".txt", "w")
    file.write("opbrengst,norm_stort,norm_trekken,opti_stort,opti_trek\n")

    for x in range(1,dagen+1): #aantal dagen da ik ga testen klaar zetten met naam gewoon een cijfer
        day_forcast = dir + "/data/" + str(x) + ".csv"
        dat = open_file_csv(day_forcast)
        day_forcast = matrix_kwartieren(dat)

        starting_energy=get_starting_energy(efficiency_matrix,watt_piek,angle,s_offset,day_forcast)


        remaining_energy=subtract_vector(starting_energy,standard_usage_list)


        optimized=optimalisation(dynamic_devices_list, remaining_energy, battery)[1]
        total_optimal=total_pos_neg(optimized)
        opti_van_net=total_optimal[1]*0.25/1000
        opti_op_net=total_optimal[0]*0.25/1000
        file.write(str(opti_op_net)+','+str(opti_van_net)+'\n')

    file.close()


def total_pos_neg(vector):
    pos=0
    neg=0
    for x in vector:
        if x>=0:
            pos+=x
        else:
            neg-=x
    return [pos,neg]

