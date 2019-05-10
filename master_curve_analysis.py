"""
Script to extract cooling event from a sequence of period buffer files and save as a separate file

"""

from data_analysis import Icarus_Data_Analysis
from matplotlib import pyplot as plt
from numpy import concatenate

#folder = '/Volumes/C/Pressure-Jump-NMR/2019-05-08-09-20-43-i2-50-restrictor/'
#the path to femto-data -> folder = '/Volumes/C/Pressure-Jump-NMR/2019-05-07-15-37-32/'
folder = '/Volumes/C/Pressure-Jump-NMR/2019-05-07-15-37-32/'
dataset_1 = Icarus_Data_Analysis(folder)
dataset_1.init()

data_res = dataset_1.get_trace(period = 0, name = 'pre')

plt.plot(data_res[5,:])
for i in range(0,50):
    data = dataset_1.get_trace(period = i, name = 'pre')
    plt.plot(data[5,:])
    plt.plot(data[6,:])
    #data_res = concatenate((data_res,data))
