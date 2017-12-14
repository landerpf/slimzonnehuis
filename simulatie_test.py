from aidfunction import battery
from simulatie import simulatie_met_batterij

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
b= battery(5000,13.5)
simulatie_met_batterij(12,"gem",3000,battery=b,angle=35,s_offset=0,efficiency_matrix=effeciency_matrix )



















# b= battery(5000,13.5)
# y=simulation("dag6","gem",3000,battery=b)
# print (y[0])
# # print(y[2])
# # print(y[3])
# import matplotlib.pyplot as plt
# plt.plot(y[1])
# plt.ylabel('some numbers')
# plt.show()