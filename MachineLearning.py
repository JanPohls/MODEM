import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR


class MachineLearning:
    """
    Machine Learning combined with Design of Experiments to find the optimum value

    Input:
    -------------------
    filename: str
        Name of .csv file with first N rows are the values for N dimensions and N + 1 is the result
    para_min, para_max, para_steps: float
        Range for the plot
    """

    def __init__(self, filename='', arr=[], para_min=[], para_max=[], para_steps=[], labels=[], regularization=300, epsilon=0.1, kernel='rbf', gamma='auto'):
        self.name = filename
        self.arr = np.transpose(arr)
        self.para_min = para_min
        self.para_max = para_max
        self.para_steps = para_steps
        self.labels = labels
        self.axis1 = 0
        self.axis2 = 1
        if self.is_float(gamma):
            self.gamma = float(gamma)
        else:
            self.gamma = gamma
        self._scale_float2int = 100
        self.kernel = kernel
        self.regularization = float(regularization)
        self.epsilon = float(epsilon)
        self.label_con = False
        self.font = 'Arial'
        self.font_size = 14
        self.font_label_size = 28
        self.step = []
        for idx, x in enumerate(para_min):
            self.step.append(int((para_max[idx]- x) / para_steps[idx]))
        self.steps = np.ones(len(self.step), dtype=int) * np.max(np.array(self.step))
        

    def _get_data_csv(self):
        """
        Read .csv file and split up in names
        """
        with open(self.name) as fil:
            data = fil.readlines()

        self.names = data[0].split(',')
        self.arr_param = np.zeros((len(data) - 1, len(self.names) - 1), dtype=float)
        self.arr_order_param = np.zeros((len(self.names) - 1, len(data) - 1), dtype=float)
        self.arr_results = np.zeros(len(data) - 1, dtype=int)
        for c in range(len(self.names) - 1):
            for l in range(1, len(data)):
                self.arr_param[l-1][c] = data[l].split(',')[c]
                self.arr_order_param[c][l-1] = data[l].split(',')[c]

        for l in range(1, len(data)):
            self.arr_results[l-1] = float(data[l].split(',')[-1]) * self._scale_float2int   


    def _get_data_arr(self):
        """
        Get data from array
        """

        self.arr_results = self.arr[-1]
        self.arr_param = np.transpose(self.arr[:-1])


    def is_float(self, string):
        """
        Check if string is a float

        Output:
        --------------------------------
        answer: Boolean
            True if float, False if string
        """
        try:
            float(string)
            return True
        
        except ValueError:
            return False


    def _svmc(self):
        """
        Predict values using support vector machine for classification
        """
        self.arr_results *= self._scale_float2int; self.arr_results = self.arr_results.astype(int)
        self.pipe = Pipeline([('scalar', StandardScaler()), ('clf', SVC(kernel=self.kernel, C=self.regularization, gamma=self.gamma))])
        #print(self.arr_param, self.arr_results, self.pipe, 'class')
        self.pipe.fit(self.arr_param, self.arr_results)
        self.predicted_results = self.pipe.predict(self.arr_param) 
        self.arr_results = self.arr_results.astype(float); self.arr_results /= self._scale_float2int
        self.label_con = False

    
    def _svmr(self):
        """
        Predict values using support vector machine for regression
        """
        self._scale_float2int = 1
        self.pipe = Pipeline([('scalar', StandardScaler()), ('reg', SVR(kernel=self.kernel, C=self.regularization, gamma=self.gamma, epsilon=self.epsilon))])
        #print(self.arr_param, self.arr_results, self.pipe)
        self.pipe.fit(self.arr_param, self.arr_results)
        self.predicted_results = self.pipe.predict(self.arr_param)
        self.label_con = True


    def _plot_pre_exp(self):
        """
        Plot experimental values versus predicted values
        """
        exp_result = self.arr_results
        pred_result = self.predicted_results / self._scale_float2int
        plt.rcParams["font.family"] = self.font
        plt.rcParams.update({'font.size': self.font_size})
        plt.scatter(
            exp_result, 
            pred_result, 
            edgecolor='k')
        plt.plot([np.min(exp_result) - 100, np.max(exp_result) + 100], [np.min(exp_result) - 100, np.max(exp_result) + 100], ls="--", c=".3")
        
        plt.xlabel('Experiments')
        plt.ylabel('Prediction')
        plt.xlim(np.min(exp_result) - 0.15 * np.abs(np.min(exp_result)), np.max(exp_result) * 1.15)
        plt.ylim(np.min(pred_result) - 0.15 * np.abs(np.min(pred_result)), np.max(pred_result) * 1.15)
        plt.tight_layout()
        plt.show()


    def _plot_slice(self, dim=[0, 1]):
        """
        Plot slice through the N-dimensional data

        Input:
        -------------------
        dim = list
            List of the dimensions used for the slice; default: [0, 1] meaning 0th and 1st dimension
        """
        xs = np.linspace(self.para_min[self.axis1], self.para_max[self.axis1], self.steps[self.axis1])
        ys = np.linspace(self.para_min[self.axis2], self.para_max[self.axis2], self.steps[self.axis2])
        
        xm,	ym = np.meshgrid(xs, ys)
        render = np.c_[xm.flatten(), ym.flatten()]
        prediction = self.pipe.predict(render).reshape(self.steps[self.axis1], self.steps[self.axis2])
        plt.rcParams["font.family"] = self.font
        plt.rcParams.update({'font.size': self.font_size})
        plt.rcParams['contour.negative_linestyle'] = 'solid'
        fig, ax = plt.subplots()
        
        print(prediction.shape, xs.shape, ys.shape)
        cm = plt.pcolormesh(xs, ys, prediction / self._scale_float2int, shading='auto', cmap='viridis')
        cs = ax.contour(xs, ys, prediction / self._scale_float2int, origin='lower', extend='both', colors='k',
                linewidths=2)
        if self.label_con:
            ax.clabel(cs, inline=5, fontsize=16)
        ax.set_xlabel(self.labels[self.axis1], fontsize=self.font_label_size)
        ax.set_ylabel(self.labels[self.axis2], fontsize=self.font_label_size)
        plt.scatter(self.arr[0], self.arr[1], marker='*', c='blue', edgecolor='k', s=150)

        plt.colorbar(cm)	
        plt.tight_layout()
        plt.show()




if __name__ == '__main__':
    filename = '../Seebeck.csv'
    min_p = [1, 2]; max_p = [1.03, 2.06]; step = [0.0001, 0.0001]; label = ['Sb', 'Te']
    ML = MachineLearning(filename, para_min=min_p, para_max=max_p, para_steps=step, labels=label)
    ML._get_data_csv()
    ML._svmr()
    ML._plot_pre_exp()
    ML._plot_slice()