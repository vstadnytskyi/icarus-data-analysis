import unittest
import os
from matplotlib import pyplot as plt
from numpy import gradient, transpose, genfromtxt, nanmean, argwhere, where, nan, isnan, asarray
from pdb import pm
plt.ion()

folder = '/Users/femto-13/All-Projects-on-femto/NMR-Pressure-Jump/icarus_software/log/'
folder = '/Users/femto-13/NMR_data/2019-04-30-18-45-20-i2-50/'
folder = '/Users/femto-13/NMR_data/2019-05-06-19-30-18-spirit-122inches/'
folder = '/Users/femto-13/NMR_data/2019-05-08-09-20-43-i2-50-restrictor/'

class Icarus_Data_Analysis():

    def __init__(self,folder = ''):
        self.folder = folder

    def init(self):
        f = open(self.folder + 'experiment.log', "r")
        a = f.readline()
        a = f.readline().replace('b','').replace('\n','').replace(' ','').replace("'","")
        self.log_header = a.split(',')

        self.lists = {}
        self.lists['cooling'] = self.get_lst(self.folder, 'cooling')
        self.lists['pre'] = self.get_lst(self.folder, 'pre')
        self.lists['depre'] = self.get_lst(self.folder, 'depre')
        self.lists['pump'] = self.get_lst(self.folder, 'pump')
        self.lists['period'] = self.get_lst(self.folder, 'period')
        self.lists['meanbit3'] = self.get_lst(self.folder, 'meanbit3')

        self.history_log = genfromtxt(self.folder + 'experiment.log', delimiter = ',', skip_header = 2)

        self.period = self.combine_log_entries(self.history_log)

        self.max_period = self.period[0]


    def get_lst(self,folder = '', type = 'cooling'):
        from numpy import genfromtxt
        import os
        dir_lst = os.listdir(folder + "/buffer_files/")
        temp_lst = []
        for item in dir_lst:
            if '_'+type in item and '._' not in item:
                t_lst = item.split('_')
                t_lst.append(item)
                temp_lst.append(t_lst)
        lst2 = sorted(temp_lst, key=lambda x: int(x[1]))
        return lst2



    def get_history_log(self):
        history_log= genfromtxt(self.folder + 'experiment.log', delimiter = ',', skip_header = 2)
        dic = {} #create dictionary
        i = 0
        for key in self.log_header:
            if key != "":
                dic[key] = history_log[:,i]
                i+=1
        return dic

    def combine_log_entries(self,history_log):
        #find maximum period indexes
        max_period = int(max(history_log[:,2]))
        period = []
        for i in list(range(max_period+1)):
            temp = []
            for j in range(len(self.log_header)):
                value = history_log[where(history_log[:,2] == i),:][:,:,j][~isnan(history_log[where(history_log[:,2] == i),:][:,:,j])]
                if len(value) == 1:
                    temp.append(float(history_log[where(history_log[:,2] == i),:][:,:,j][~isnan(history_log[where(history_log[:,2] == i),:][:,:,j])]))
                elif len(value) == 0:
                    temp.append(nan)
                elif len(value) >1:
                    temp.append(float(history_log[where(history_log[:,2] == i),:][:,:,j][~isnan(history_log[where(history_log[:,2] == i),:][:,:,j])][0]))
            period.append(temp)
        return asarray(period)

    def get_log_vector(self,param = 'None'):
        from numpy import squeeze
        try:
            idx = dataset_1.log_header.index(param)
        except:
            print("param %r doesn't exist" %param)
            idx = None
        if not None:
            vector = self.period[:,idx]
        return vector

    def get_trace(self,period = 0,name = ''):
        import os
        from numpy import genfromtxt, transpose
        filename = 'some_nonexisting_file.x'
        for item in self.lists[name]:
            print(item)
            if item[1] == str(period):
                filename = item[3]
        filepath = self.folder + '/buffer_files/'+filename
        exists = os.path.isfile(filepath)
        if exists:
            data = transpose(genfromtxt(filepath,delimiter = ','))
            x = data[:,0]
            sample = data[:,1]
            target = data[:,2]
        else:
            data = None
        return data

    def test_slow_leak(self):
        test_data_folder = '/Users/femto-13/NMR_data/cooling-data/2019-04-12-19-05-23/'
        lst = event_detector.get_cooling_traces_lst(folder = test_data_folder)
        data = event_detector.get_cooling_traces(lst,test_data_folder,0)

if __name__ == '__main__':
    ##Examples of commands
    ## to get a trace: dataset_1.get_trace(i,'pre') -> return a pressurization trace of all 10 channels at period i
    ## to get a vector from log file for given parameter: dataset_1.get_log_vector(param = 'tSwitchDepressure_1')
    dataset_1 = Icarus_Data_Analysis(folder)
    #folder = '/Users/femto-13/NMR_data/2019-05-07-15-37-32/'
    #dataset_2 = Icarus_Data_Analysis(folder)

    dataset_1.init()
    dic = dataset_1.history_log
    plt.figure()
    plt.subplot(321)
    plt.title('Depressure in kbar')
    plt.plot(dataset_1.get_log_vector(param = 'pDepre_0'),'or',label = 'Sample')
    plt.legend()
    plt.subplot(323)
    plt.title('Depressurization Time to Switch in ms')
    plt.plot(dataset_1.get_log_vector(param = 'tSwitchDepressure_1'),'or',label = 'Sample')
    plt.plot(dataset_1.get_log_vector(param = 'tSwitchDepressure_0'),'ob',label = 'Origin')
    plt.plot(dataset_1.get_log_vector(param = 'tSwitchDepressureEst_0'),'og',label = 'Sample Est.')
    plt.legend()
    plt.subplot(325)
    plt.title('Depressurization Slope in kbar/ms')
    plt.plot(dataset_1.get_log_vector(param = 'gradientDepressure_1'),'or',label = 'Sample')
    plt.plot(dataset_1.get_log_vector(param = 'gradientDepressure_0'),'ob',label = 'Origin')
    plt.plot(dataset_1.get_log_vector(param = 'gradientDepressureEst_0'),'og',label = 'Sample Est.')
    plt.legend()

    plt.subplot(322)
    plt.title('Pressure in kbar')
    plt.plot(dataset_1.get_log_vector(param = 'pPre_after_0'),'or',label = 'Sample')
    plt.legend()
    plt.subplot(324)
    plt.title('Pressurization Time to Switch in ms')
    plt.plot(dataset_1.get_log_vector(param = 'tSwitchPressure_1'),'or',label = 'Sample')
    plt.plot(dataset_1.get_log_vector(param = 'tSwitchPressure_0'),'ob',label = 'Origin')
    plt.plot(dataset_1.get_log_vector(param = 'tSwitchPressureEst_0'),'og',label = 'Sample Est.')
    plt.legend()
    plt.subplot(326)
    plt.title('Pressurization Slope in kbar/ms')
    plt.plot(dataset_1.get_log_vector(param = 'gradientPressure_1'),'or',label = 'Sample')
    plt.plot(dataset_1.get_log_vector(param = 'gradientPressure_0'),'ob',label = 'Origin')
    plt.plot(dataset_1.get_log_vector(param = 'gradientPressureEst_0'),'og',label = 'Sample Est.')
    plt.legend()
    # print('tSwitchDepressure_0: %r , tSwitchDepressure_1: %r , tSwitchDepressureEst_0: %r' %(nanmean(dic[b'tSwitchDepressure_0']),nanmean(dic[b'tSwitchDepressure_1']),nanmean(dic[b'tSwitchDepressureEst_0'])))
    # print(nanmean(dic[b'tSwitchDepressureEst_0'])-nanmean(dic[b'tSwitchDepressure_1']))
    # print('tSwitchPressure_0: %r , tSwitchPressure_1: %r , tSwitchPressureEst_0: %r' %(nanmean(dic[b'tSwitchPressure_0']),nanmean(dic[b'tSwitchPressure_1']),nanmean(dic[b'tSwitchPressureEst_0'])))
    # print(nanmean(dic[b'tSwitchPressureEst_0'])-nanmean(dic[b'tSwitchPressure_1']))
    #
    # print('gradientDepressure_0: %r , gradientDepressure_1: %r , gradientDepressureEst_0: %r' %(nanmean(dic[b'gradientDepressure_0']),nanmean(dic[b'gradientDepressure_1']),nanmean(dic[b'gradientDepressureEst_0'])))
    # print(nanmean(dic[b'gradientDepressure_0'])/nanmean(dic[b'gradientDepressure_1']))
    # print('gradientPressure_0: %r , gradientPressure_1: %r , gradientPressureEst_0: %r' %(nanmean(dic[b'gradientPressure_0']),nanmean(dic[b'gradientPressure_1']),nanmean(dic[b'gradientPressureEst_0'])))
    # print(nanmean(dic[b'gradientPressure_0'])/nanmean(dic[b'gradientPressure_1']))
