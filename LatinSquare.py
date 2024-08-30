from multiprocessing.reduction import AbstractReducer
import numpy as np
import random
import matplotlib.pyplot as plt 
import copy
import itertools


class DesignOfExperiments:
    """
    Design of Experiments approach to find the optimum experimental conditions

    Input:
    --------------------
    arr_min: ndarray (N)
        minimum values for N-dimensional experimental parameters
    arr_max: ndarray (N)
        maximum values for N-dimensional experimental parameters
    arr_step: ndarray (N)
        step sizes for N-dimensional experimental parameters
    nmb_exp: int
        number of experiments
    self.center: Boolean
        True, place an item in the center
    self.period: Boolean
        True, it is periodically in space
    """
    
    def __init__(self, arr_min=[], arr_max=[], arr_step=[], nmb_exp=10, run_nmb=1000, center=False, period=False):
        self.min = np.array(arr_min)
        self.max = np.array(arr_max)
        self.step = np.array(arr_step)
        self.run_nmb = run_nmb
        self.nmb_exp = nmb_exp
        self.center = center
        self.period = period
        self.average = True
        self.mini_method = 'std'
        self.update_list = []
        self.previous_pts = []


    def _set_range(self):
        """
        Set the range of the parameters
        """
        self.max_step = (self.max - self.min) / self.step
        self.dimensions = list()
        for d in self.max_step:
            self.dimensions.append(np.arange(d+1).tolist())


    def _run_DoE(self):
        """
        Use the dimensional to increase the maximum values
        """
        self._set_range()
        self.average_dist = 0; self.std = 1E5; self.min_ener = 1E5; self.min_force = 1E5
        list_average = list(); list_std = list(); list_arrays = list(); list_force = list(); list_energy = list()
        for test in range(self.run_nmb):
            calculate_distance = True
            array_val = []
            for x in range(len(self.max_step)):
                array_val.append([])
            
            dim = copy.deepcopy(list(self.dimensions))

            if len(self.update_list) > 0:
                dim = copy.deepcopy(list(self.update_list))
                array_val = copy.deepcopy(self.previous_pts)
                        

            if self.center:
                for i in range(len(dim)):
                    cent_dim = int(len(dim[i])/2)
                    array_val[i].append(cent_dim)
                    dim[i] = [x for x in dim[i] if x != dim[i][cent_dim]]
                
                nmbexp = self.nmb_exp - 1

            else:
                nmbexp = self.nmb_exp

            if len(self.update_list) == 0:
                for sample in range(nmbexp):
                    for i in range(len(dim)):
                        val = random.randint(0, len(dim[i])-1)
                        array_val[i].append(dim[i][val])
                        dim[i] = [x for x in dim[i] if x != dim[i][val]]

            else:
                for sample in range(nmbexp):
                    val = random.randint(0, len(dim[0]) - 1)
                    lst_remove = list()
                    for d in range(len(dim)):
                        array_val[d].append(dim[d][val])
                        value = dim[d][val]
                        lst_remove.extend(np.argwhere(dim[d] == value))
                    set_ = np.unique(np.array(lst_remove))
                    
                    for d in range(len(dim)):
                        dim[d] = [dim[d][x] for x in range(len(dim[d])) if x not in set_]
      
            array_val = np.transpose(array_val) 
            if self.period:
                data_pts = self.nmb_exp * 3**len(dim)
                arrays = list()
                for d in self.max_step:
                    arrays.append([-d, 0, d])
                periodicity = list(itertools.product(*arrays))
                new_array = np.zeros((data_pts, len(dim)), dtype=float)
                nmb = 0
                for idx, ar in enumerate(periodicity):
                    for ex in range(self.nmb_exp):
                        new_array[nmb] = np.array(ar) + array_val[ex]
                        nmb += 1

            else:
                data_pts = len(array_val)
                new_array = array_val

            if calculate_distance:
                
                distances = []; energy = []; force = []
                for i in range(data_pts):
                    for j in range(data_pts):
                        
                        if i != j:
                            pt1 = []; pt2 = []
                            for x in range(len(self.max_step)):
                                pt1.append(new_array[i][x]); pt2.append(new_array[j][x])
                            
                            distances.append(np.linalg.norm(np.array(pt1) - np.array(pt2)))
                            energy.append(1/distances[-1])
                            force.append(1/distances[-1]**2)
                
                average = np.average(np.array(distances)); stdev_distance = np.std(np.array(distances))
                minimum = np.min(np.array(distances))
                std_min = stdev_distance / minimum
                avg_ener = np.average(energy)
                avg_force = np.average(force)
                
                if (std_min < self.std):
                    if stdev_distance < 1e-7:
                        self.mini_method = 'force'
                        self._run_DoE()
                    self.std = std_min
                    list_std.append(std_min); list_average.append(average)
                    if self.mini_method == 'std':
                        list_arrays.append(array_val)
                        print(std_min, average, avg_ener, avg_force, test, 'std')

                if self.min_ener > avg_ener:
                    self.min_ener = avg_ener
                    list_energy.append(avg_ener)
                    if self.mini_method == 'energy':
                        list_arrays.append(array_val)
                        print(std_min, average, avg_ener, avg_force, test, 'ener')

                if self.min_force > avg_force:
                    self.min_force = avg_force
                    list_force.append(avg_force)
                    if self.mini_method == 'force':
                        list_arrays.append(array_val)
                        print(std_min, average, avg_ener, avg_force, test, 'force')

        if len(list_average) > 2 and self.average:
            average = 0
            print(list_average, list_std)
            for i in range(3):
                if average < list_average[-3 + i]:
                    average = list_average[-3 + i]
                    self.std = list_std[-3 + i]
                    self.array_min = list_arrays[-3 + i]
        
        else:
            self.array_min = list_arrays[-1]
            average = list_average[-1]
            self.std = list_std[-1]
        
        for x in range(len(self.array_min)):
            for y in range(len(self.array_min[x])):
                self.array_min[x][y] = self.array_min[x][y] * self.step[y] + self.min[y]

        self.array_min = np.transpose(self.array_min)
        print(self.array_min, 'final')


    def _plot_3D(self, xlabel='', ylabel='', zlabel=''):
        """
        Plot a 3D figure
        """
        self.fig = plt.figure()
        ax = self.fig.add_subplot()
        ax = plt.axes(projection ='3d')
        ax.scatter(*self.array_min, c='green', edgecolor='k')
        print(self.array_min)

        if len(self.previous_pts) > 0:
            
            previous_pts = list()
            for pp in range(3):
                previous_pts.append([self.array_min[pp][i] for i in range(len(self.previous_pts[pp]))])
            ax.scatter(*previous_pts, edgecolor='k', c='orange')

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        ax.set_xlim(self.min[0], self.max[0])
        ax.set_ylim(self.min[1], self.max[1])
        ax.set_zlim(self.min[2], self.max[2])
        plt.tight_layout()


    def _plot_2D(self, xlabel='', ylabel=''):
        """
        Plt a 2D figure
        """
        self.fig = plt.figure()
        ax = self.fig.add_subplot()
        plt.scatter(*self.array_min, edgecolor='k', c='green')

        if len(self.previous_pts) > 0:
            
            previous_pts = list()
            for pp in range(2):
                previous_pts.append([self.array_min[pp][i] for i in range(len(self.previous_pts[pp]))])
            plt.scatter(*previous_pts, edgecolor='k', c='orange')
       
        plt.xlim(self.min[0], self.max[0])
        plt.ylim(self.min[1], self.max[1])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()



if __name__ == "__main__":
    min_arr = [0.9, 300]
    max_arr = [1.3, 350]
    step_arr = [0.01, 1.0]
    DoE = DesignOfExperiments(min_arr, max_arr, step_arr, nmb_exp=10)
    DoE.run_nmb = 100000
    DoE._set_range()
    DoE._run_DoE()
    DoE._plot_2D()
    plt.show()