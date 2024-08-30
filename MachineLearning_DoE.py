from tkinter import OptionMenu, Button, Checkbutton, Radiobutton, Label, Entry, Text, Menu, Frame, Spinbox
from tkinter import Tk, Toplevel, colorchooser
from PIL import ImageTk, Image
from tkinter import INSERT, END, RIDGE, NORMAL, DISABLED, SUNKEN
from tkinter import messagebox, filedialog
from tkinter import StringVar, IntVar, DoubleVar, BooleanVar
from tkinter import font as tkFont

import json
import numpy as np
import os
import re 
from copy import deepcopy

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from LatinSquare import DesignOfExperiments
from MachineLearning import MachineLearning


class FullScreenApp(object):
    """
    Class to increase the window to the maximum screen size
    """

    def __init__(self, screen, **kwargs):
        """
        Change screen to fullscreen
        Input:
        ----------------
        screen: The window to maximize
        """
        self.screen = screen
        edge = 3
        self._small = '400x200+0+0'
        screen.geometry("{0}x{1}+0+0".format(
            screen.winfo_screenwidth()-edge, screen.winfo_screenheight()-edge))
        screen.bind('<Escape>', self.toggle_screen)

    def toggle_screen(self, event):
        small = self.screen.winfo_geometry()
        self.screen.geometry(self._small)
        self._small = small


    def screen_dim(self):
        """
        Get dimensions of screen

        Output:
        -----------------
        screenheight, screenwidth: int
            Height and width of screen
        """
        return self.screen.winfo_screenheight(), self.screen.winfo_screenwidth()


class Help:
    """
    Help Menu to link to other websites/documentations
    """

    def __init__(self):
        """
        Help menu window
        """
        self.screen_help = Toplevel()
        self.screen_help.configure(bg = MainApplication._from_rgb(self, (11, 165, 193)))
        self.screen_help.geometry('700x300')
        #self.screen_help.iconbitmap('icon_band.ico')

    def welcome(self):
        """
        Welcome window
        """
        text = Text(self.screen_help, height=15)
        text.insert(INSERT, 'Welcome to the MODEM! \n')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'Optimize your input parameters using a fraction of experiments. ')
        text.insert(INSERT, ' \n')
        text.insert(INSERT, '\n')
        text.insert(END, ' Please check out the documentaries for more information!  \n \n Thank you for choosing MODEM!')
        text.grid(row=0, column=0, padx=10, pady=(30, 10))

    def documentary(self, *args):
        """
        Documentary window
        """
        text = Text(self.screen_help, height=15)
        text.insert(INSERT, 'Welcome to MODEM! \n')
        text.insert(INSERT, '\n')
        text.insert(END, 'I will update the documentaries at a later point!')
        text.grid(row=0, column=0, padx=10, pady=(30, 10))

    def about(self):
        """
        About window
        """
        text = Text(self.screen_help)
        text.insert(INSERT, 'MODEM stands for Multi-variable Optimization software driven by Design of       Experiments and Machine learning! \n ')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'This is a program to optimize the input parameters by efficiently construct a   grid of experiments and interpolate the data using diverse machine learning     algorithms. \n')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'The software was written in Python and Tkinter!  This is version v0.3 and I am  looking for any suggestions and reports of errors. \n')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'This is a free software and should not be used for commercial reasons. \n')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'If you have suggestions, concerns, or find errors, please send me an email: \n Jan.Pohls@UNB.ca \n ')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'Thank you for choosing MODEM. \n \n  --Jan-- \n \n')
        text.insert(INSERT,  '\xa9 Jan-Hendrik Carroll-Poehls, Assistant Professor, 2024')
        text.grid(row=0, column=0, padx=10, pady=(30, 10))



class EntryItem:
    """
    Combine different tkinter items with Label items
    """

    def __init__(self, parent, name, row=0, column=1, padx=10, pady=6, width=20, columnspan=1, state=NORMAL, ipadx=0, options=['0']):
        """
        Combine Entry/Menu items with Label items
        Input:
        -------------------------------------
        parent: class
        name: str
            Name of the Label
        row: int
            number of row
        column: int
            number of column
        padx: int
            space in x-direction of grid
        pady: int
            space in y-direction of grid
        width: int
            width of the Entry
        columnspan: int
            column span of Entry and Label
        state: NORMAL or DISABLED
        options: list
            List of options for OptionMenu
        initial_val: StringVar()
            initial value of OptionMenu
        var: StringVar()
            name and type of variable of Entry
        entry: Entry item
        label: Label item
        menu: OptionMenu item
        """
        self.parent = parent
        self.name = name
        self.row = row
        self.column = column
        self.padx = padx
        self.pady = pady
        self.width = width
        self.columnspan = columnspan
        self.state = state
        self.ipadx = ipadx
        self.options = options
        self.initial_val = StringVar()
        self.var = StringVar()
        self.entry = Entry(self.parent, textvariable=self.var, state=self.state, width=self.width)
        self.label = Label(self.parent, text=name, relief=RIDGE, anchor='w')
        self.menu = OptionMenu(self.parent, self.initial_val, *self.options)


    def create_EntryItem(self, padx_label=10, pady_label=6, ipadx_label=0):
        """
        Combine Label with Entry item next to each other
        Input:
        ------------------------------
        padx_label: int
            space in x-direction for the Label
        pady_label: int
            space in y-direction for the Label
        ipadx_label: int
            size of the Label
        """
        self.entry.grid(row=self.row, column=self.column, columnspan=self.columnspan, padx=self.padx, pady=self.pady, ipadx=self.ipadx)
        self.label.grid(row=self.row, column=self.column-1, columnspan=self.columnspan, padx=padx_label, pady=pady_label, ipadx=ipadx_label)


    def set_name(self, new_name='NaN'):
        """
        Change the name of the Entry
        Input:
        ------------------
        new_name: str
            Name of the Label
        """
        self.var.set(new_name)


    def get_name(self):
        """
        Get value of the Entry
        """
        return self.var.get()


    def delete(self):
        """
        Delete an Entry
        """
        self.entry.delete(0, END)

    
    def destroy(self):
        """
        Destroy an Entry
        """
        self.entry.destroy()
        self.label.destroy()


    def update(self, name):
        """
        Remove entry and insert a new entry with a new value
        Input:
        ----------------------
        name: str
            New value of Entry
        """
        self.delete()
        self.entry.insert(0, name)
        return


    def disable(self):
        """
        Disable an Entry widget
        """
        self.entry.config(state='disabled')


    def enable(self):
        """
        Enable Entry Widget
        """
        self.entry.config(state='normal')



class Table:
    """
    Create a table using an array of size (N, M) where N is the number of rows and columns
    """
     
    def __init__(self, parent, arr=np.array([[]]), labels=[], row=0, column=0, width=20, results=False):
        """
        parent: class
        arr: ndarray(N, M), dtype=float
            array of the parameters (columns, N) and the number of experiments (rows, M)
        labels: list (N)
            List of N parameter labels
        row: int
            number of row
        column: int
            number of column
        width: int
            width of the Entry
        """
        self.parent = parent
        self.arr = arr
        self.columns_table = len(arr) 
        self.rows_table = len(arr[0]) + 1
        self.labels = labels
        self.row = row
        self.column = column
        self.width = width
        self.results = results
        self.results_data = ''


    def _create_table(self):
        """
        Create a table of N+1 columns (parameters+result) and M+1 rows(labels+number of experiments)
        """
        self.header = list()
        for idx, p in enumerate(self.labels):
            self.header.append(Entry(self.parent, width=self.width))
            self.header[-1].grid(row=self.row, column=idx+self.column)
            self.header[-1].insert(0, p)
            #self.e.config(state= "disabled")

        if self.results:
            self.header.append(Entry(self.parent, width=self.width))
            self.header[-1].grid(row=self.row, column=self.column+len(self.labels))
            self.header[-1].insert(0, 'Results')
            #self.e.config(state= "disabled")
            self.columns_table += 1


        self.table = list()
        for r in range(1, self.rows_table):
            table_col = list()
            for c in range(self.columns_table):
                table_col.append(Entry(self.parent, width=self.width))
                table_col[-1].grid(row=r+self.row, column=c+self.column)
                
                if c < len(self.arr):
                    table_col[-1].insert(END, self.arr[c][r-1])
                
                else:
                    if len(self.results_data) > 0:
                        table_col[-1].insert(END, self.results_data[r-1])
            self.table.append(table_col)


    def _destroy_table(self):
        """
        Destroy the table 
        """
        for h in self.header:
            h.destroy()

        for r in range(len(self.table)):
            for c in range(len(self.table[r])):
                self.table[r][c].destroy()



class MainApplication:
    """
    Main window and functions to perform Design of Experiments and machine learning experiments
    """

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.parent.configure(bg = self._from_rgb((11, 165, 193)))
        self.title = self.parent.title('MODEM App')
        #self.icon = self.parent.iconbitmap('icon_band.ico')
        self.font_window = tkFont.Font(family='Helvetica', size= 10, weight='bold')

        self.app = FullScreenApp(self.parent)
        self.screenheight, self.screenwidth = self.app.screen_dim()
        self.size_x = DoubleVar(); self.size_y = DoubleVar()
        self.size_x.set(self.screenwidth / 1950. * 7)
        self.size_y.set(self.screenheight / 860. * 6)
        

        # Create Frame
        self.input = Frame(self.parent, height=368 * self.screenheight / 860., width=395, bg=self._from_rgb((11, 112, 141)))
        self.input.grid(row=0, column=0, columnspan=2, rowspan=12, pady=(10, 5))
        self.label_input = Label(self.parent, text='Perform Machine Learning')
        self.label_input.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        self.label_input['font'] = self.font_window
        self.output = Frame(self.parent, height=302 * self.screenheight / 860., width=395, bg=self._from_rgb((175, 188, 205)))
        self.output.grid(row=12, column=0, columnspan=2, rowspan=14, pady = (0, 5))
        self.label_DoE = Label(self.parent, text='Plot parameters - Machine Learning')
        self.label_DoE.grid(row=12, column=0, columnspan=2, pady=(0, 5))
        self.label_DoE['font'] = self.font_window

        # Create MenuBar
        my_Menu = Menu(self.parent)
        self.parent.config(menu=my_Menu)

        file_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New', command=self.clear)
        file_menu.add_command(label='Open File', command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.close_program)

        edit_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Edit Graph', command=self.Edit_graph)

        DoE_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='Design Of Experiments', menu=DoE_menu)
        DoE_menu.add_command(label='Create Design of Experiments', command=self.create_DoE)
        DoE_menu.add_command(label='Update Design of Experiments', command=self.update_DoE)
        
        upload_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='Upload', menu=upload_menu)
        upload_menu.add_command(label='Upload Table (.txt) for Machine Learning', command=self.upload_table_txt)
        upload_menu.add_command(label='Upload Table (.json) for Machine Learning', command=self.upload_table_json)
        upload_menu.add_command(label='Upload Table (.csv) for Machine Learning', command=self.upload_table_csv)
        upload_menu.add_command(label='Create Table for Machine Learning', command=self.create_table_ML)

        plot_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='Plot', menu=plot_menu)
        plot_menu.add_command(label='Replot Machine Learning', command=self.replot_ML_data)
        plot_menu.add_command(label='Upload Machine Learning', command=self._load_ML_file)

        help_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Welcome', command=self.welcome)
        help_menu.add_command(label='Documentations', command=self.documentary)
        help_menu.add_separator()
        help_menu.add_command(label='About', command=self.about)


        #Create Buttons
        self.file_options = [
            '.txt',
            '.json',
            '.csv',
        ]
        self.initial_file_ext = StringVar(); self.initial_file_ext.set(self.file_options[0])
        self.file_menu = OptionMenu(self.parent, self.initial_file_ext, *self.file_options)
        self.file_menu.grid(row=1, column=1, padx=10, pady=10, ipadx=40)
        self.kernel_options = ['rbf']
        self.initial_kernel_option = StringVar(); self.initial_kernel_option.set(self.kernel_options[0])
        self.kernel_menu = OptionMenu(self.parent, self.initial_kernel_option, *self.kernel_options)
        self.kernel_menu.grid(row=4, column=0, ipadx=47, padx=10, pady=10)
        self.ML_options = [
            'SVM - Classification',
            'SVM - Regression'
        ]
        self.initial_ML_options = StringVar(); self.initial_ML_options.set(self.ML_options[0])
        self.ML_menu = OptionMenu(self.parent, self.initial_ML_options, *self.ML_options)
        self.ML_menu.grid(row=4, column=1, padx=10, pady=10)
        self.parameter_options = ['Parameter 1']
        self.initial_parameter_x_option = StringVar(); self.initial_parameter_x_option.set(self.parameter_options[0])
        self.para_x_menu = OptionMenu(self.parent, self.initial_parameter_x_option, *self.parameter_options)
        self.para_x_menu.grid(row=14, column=1, padx=10, pady=10, ipadx=20)
        self.initial_parameter_y_option = StringVar(); self.initial_parameter_y_option.set(self.parameter_options[0])
        self.para_y_menu = OptionMenu(self.parent, self.initial_parameter_y_option, *self.parameter_options)
        self.para_y_menu.grid(row=15, column=1, padx=10, pady=10,ipadx=20)


        self.CheckResultVar = IntVar()
        self.check_results = Checkbutton(self.parent, text='Last column results', variable=self.CheckResultVar)
        self.check_results.grid(row=3, column=0, ipadx=10)
        self.load_button = Button(self.parent, text='Upload', command=self.load_DoE_file)
        self.load_button.grid(row=3, column=1, pady=10, ipadx=42)
        self.load_button['font'] = self.font_window
        self.run_ML_button = Button(self.parent, text='Run Machine Learning', command=self.run_ML, state=DISABLED)
        self.run_ML_button.grid(row=8, column=0, pady=10)
        self.run_ML_button['font'] = self.font_window
        self.save_ML_button = Button(self.parent, text='Save Machine Learning', command=self.save_ML, state=DISABLED)
        self.save_ML_button.grid(row=8, column=1, pady=10)
        self.save_ML_button['font'] = self.font_window
        self.upload_ML_button = Button(self.parent, text='Upload ML file', command=self._load_ML_file)
        self.upload_ML_button.grid(row=13, column=0, pady=10, ipadx=22)
        self.upload_ML_button['font'] = self.font_window
        self.replot_ML_button = Button(self.parent, text='Replot', command=self.replot_ML_data, state=DISABLED)
        self.replot_ML_button.grid(row=16, column=0, pady=10, ipadx=42)
        self.replot_ML_button['font'] = self.font_window
        self.save_MLPlot_button = Button(self.parent, text='Save ML Figure', command=self.save_ML_plot, state=DISABLED)
        self.save_MLPlot_button.grid(row=16, column=1, pady=10, ipadx=22)
        self.save_MLPlot_button['font'] = self.font_window
        self.fix_parameters_button = Button(self.parent, text='Fix other Parameters', command=self.fix_parameter_level, state=DISABLED)
        self.fix_parameters_button.grid(row=13, column=1, pady=10, ipadx=2)
        self.fix_parameters_button['font'] = self.font_window

        self.filename = EntryItem(self.parent, name='Filename', row=2, state=DISABLED)
        self.filename.create_EntryItem(ipadx_label=48)
        self.epsilon = EntryItem(self.parent, name='Epsilon', row=5)
        self.epsilon.create_EntryItem(ipadx_label=54); self.epsilon.set_name(0.1)
        self.gamma= EntryItem(self.parent, name='Gamma', row=6)
        self.gamma.create_EntryItem(ipadx_label=53); self.gamma.set_name('auto')
        self.regularization = EntryItem(self.parent, name='Regularization', row=7)
        self.regularization.create_EntryItem(ipadx_label=35); self.regularization.set_name(100)
        self.filetype = Label(self.parent, text='File type')
        self.filetype.grid( row=1, column=0, ipadx=50)
        self.plot_x = Label(self.parent, text='Parameter for x-axis')
        self.plot_x.grid( row=14, column=0, ipadx=18)
        self.plot_y = Label(self.parent, text='Parameter for y-axis')
        self.plot_y.grid( row=15, column=0, ipadx=18)

        #Create Plot Data
        self.font_size = DoubleVar(); self.font_size.set(self.screenheight / 860. * 16)
        
        self.size_x_space = DoubleVar(); self.size_x_space.set(0.18)
        self.size_x_length = DoubleVar(); self.size_x_length.set(0.78)
        self.size_y_space = DoubleVar(); self.size_y_space.set(0.23)
        self.size_y_length = DoubleVar(); self.size_y_length.set(0.68)
        self.font_options = [
            'sans-serif',
            'serif',
            'Times New Roman',
            'Arial',
            'Gabriola',
            'Courier New',
            'Cambria',
            'Calibri',    
        ]
        self.initial_font = StringVar(); self.initial_font.set(self.font_options[0])
        self.font_size = StringVar(); self.font_size.set(self.screenheight / 860. * 18)
        self.resolution_plot = 200

        self.parent.protocol('WM_DELETE_WINDOW', self.close_program)
        self.create_empty_plot()


    def clear(self):
        """
        Default values to start new project
        """   
        self.create_empty_plot()
        self.initial_file_ext.set(self.file_options[0])
        self.filename.set_name('')
        self.initial_ML_options.set(self.ML_options[0])
        self.epsilon.set_name(0.1)
        self.gamma.set_name("auto")
        self.regularization.set_name(100)
        self.parameter_options = ['Parameter 1']
        self.initial_parameter_x_option = StringVar(); self.initial_parameter_x_option.set(self.parameter_options[0])
        self.initial_parameter_y_option = StringVar(); self.initial_parameter_y_option.set(self.parameter_options[0])


    def Edit_graph(self):
        """
        Edit plot by changing size and font
        """
        self.Top = Toplevel()
        self.Top.configure(bg = self._from_rgb((11, 165, 193)))
        self.Top.geometry("600x300")
        #self.Top.iconbitmap('icon_spb.ico')

        self.font_size_entry = Entry(self.Top, textvariable=self.font_size, width=24)
        self.font_size_entry.grid(row=0, column=1, padx=10, pady=(50, 10))
        self.font_size_label = Label(self.Top, text='Font Size', relief=RIDGE, anchor='w')
        self.font_size_label.grid(row=0, column=0, padx=10, pady=(50, 10), ipadx=20)

        self.size_x_entry = Entry(self.Top, textvariable=self.size_x, width=24)
        self.size_x_entry.grid(row=0, column=3, padx=10, pady=(50, 10))
        self.size_x_label = Label(self.Top, text='Figure Width', relief=RIDGE, anchor='w')
        self.size_x_label.grid(row=0, column=2, padx=10, pady=(50, 10), ipadx=17)

        self.size_y_entry = Entry(self.Top, textvariable=self.size_y, width=24)
        self.size_y_entry.grid(row=1, column=3, padx=10, pady=10)
        self.size_y_label = Label(self.Top, text='Figure Height', relief=RIDGE, anchor='w')
        self.size_y_label.grid(row=1, column=2, padx=10, pady=10, ipadx=15)

        self.size_x_space_entry = Entry(self.Top, textvariable=self.size_x_space, width=24)
        self.size_x_space_entry.grid(row=2, column=1, padx=10, pady=10)
        self.size_x_space_label = Label(self.Top, text='Plot Start x', relief=RIDGE, anchor='w')
        self.size_x_space_label.grid(row=2, column=0, padx=10, pady=10, ipadx=16)

        self.size_y_space_entry = Entry(self.Top, textvariable=self.size_y_space, width=24)
        self.size_y_space_entry.grid(row=3, column=1, padx=10, pady=10)
        self.size_y_space_label = Label(self.Top, text='Plot Start y', relief=RIDGE, anchor='w')
        self.size_y_space_label.grid(row=3, column=0, padx=10, pady=10, ipadx=16)

        self.size_x_length_entry = Entry(self.Top, textvariable=self.size_x_length, width=24)
        self.size_x_length_entry.grid(row=2, column=3, padx=10, pady=10)
        self.size_x_length_label = Label(self.Top, text='Plot Width x', relief=RIDGE, anchor='w')
        self.size_x_length_label.grid(row=2, column=2, padx=10, pady=10, ipadx=20)

        self.size_y_length_entry = Entry(self.Top, textvariable=self.size_y_length, width=24)
        self.size_y_length_entry.grid(row=3, column=3, padx=10, pady=10)
        self.size_y_length_label = Label(self.Top, text='Plot Width y', relief=RIDGE, anchor='w')
        self.size_y_length_label.grid(row=3, column=2, padx=10, pady=10, ipadx=20)

        self.font_menu = OptionMenu(self.Top, self.initial_font, *self.font_options)
        self.font_menu.grid(row=1, column=1, padx=10, pady=10)
        self.font_label = Label(self.Top, text='Font', relief=RIDGE, anchor='w')
        self.font_label.grid(row=1, column=0, padx=10, pady=10, ipadx=32)

        btn_close = Button(self.Top, text='Close', command=self.close_update_graph)
        btn_close.grid(row=4, column=3, padx=10, pady=10, ipadx=35)


    def create_empty_plot(self):
        """
        Create an emplty plot at the start and when it is cleared
        """

        plt.rcParams["font.family"] = self.initial_font.get()
        plt.rcParams.update({'font.size': self.font_size.get()})

        self.fig_predict = Figure(figsize=(self.size_x.get(), self.size_y.get()), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig_predict, master=self.parent)
        self.canvas.draw()
        self.plot_widget_predict = self.canvas.get_tk_widget()
        self.plot_widget_predict.grid(row=0, column=2, columnspan=5, rowspan=16)

        self.fig_ML = Figure(figsize=(self.size_x.get(), self.size_y.get()), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig_ML, master=self.parent)
        self.canvas.draw()
        self.plot_widget_ML = self.canvas.get_tk_widget()
        self.plot_widget_ML.grid(row=0, column=8, columnspan=5, rowspan=16)

        self.ax2 = self.fig_predict.add_axes([self.size_x_space.get(), self.size_y_space.get(), self.size_x_length.get(), self.size_y_length.get()])
        self.ax2.set_xlabel('Experiment')
        self.ax2.set_xlim(1, 10)
        self.ax2.set_ylabel('Prediction')
        self.ax2.set_ylim(1, 10)

        ax1 = self.fig_ML.add_axes([self.size_x_space.get(), self.size_y_space.get(), self.size_x_length.get(), self.size_y_length.get()])
        ax1.set_xlabel('Parameter 1')
        ax1.set_xlim(1, 10)
        ax1.set_ylabel('Parameter 2')
        ax1.set_ylim(1, 10)

        self.toolbar_frame_predict = Frame(self.parent) 
        self.toolbar_frame_predict.grid(row=18,column=2,columnspan=4) 
        toolbar_predict = NavigationToolbar2Tk(self.canvas, self.toolbar_frame_predict)
        toolbar_predict.update()

        self.toolbar_frame_ML = Frame(self.parent) 
        self.toolbar_frame_ML.grid(row=18,column=8,columnspan=4) 
        toolbar_ML = NavigationToolbar2Tk(self.canvas, self.toolbar_frame_ML)
        toolbar_ML.update()


    def close_update_graph(self):
        """
        Close the Edit window and create an empty plot
        """
        self.plot_widget_ML.grid_forget()
        self.plot_widget_predict.grid_forget()
        self.create_empty_plot()
        self.Top.destroy()


    def open_file(self):
        """
        Open folder which needs to include the .json file
        """
        self._load_ML_file()


    def close_program(self):
        """
        Close the DoEML program
        """
        self.parent.quit()
        self.parent.destroy()


    def create_DoE(self):
        """
        Create a .csv and .json file using a Monte Carlo approach
        """
        self.DoE_mode = 'create'
        self.DoELevel = Toplevel()
        self.DoELevel.configure(bg=self._from_rgb((11, 165, 193)))
        self.DoELevel.geometry("1000x700")
        #self.DoELevel.iconbitmap('icon_band.ico')
        self.DoELevel.grab_set()

        #Texts
        self.DoE_input = Label(self.DoELevel, text='Input parameters for Design of Experiments')
        self.DoE_input.grid(row=0, column=0, columnspan=3, pady=(10, 5))
        self.DoE_input['font'] = self.font_window

        #Entries
        self.dimensions = EntryItem(self.DoELevel, name='Dimensions of Parameters', row=1, width=6)
        self.dimensions.create_EntryItem(ipadx_label=0); self.dimensions.initial_val = DoubleVar(); self.dimensions.set_name(2)
        self.Dimension_label = list(); self.Dimension_label_var = list(); self.Dimension_label_entry = list()
        self.Dimension_min_entry = list(); self.Dimension_max_entry = list(); self.Dimension_step_entry = list()

        #Buttons
        self.dimension_button = Button(self.DoELevel, text='Dimensions', command=self.create_dimension_entries)
        self.dimension_button.grid(row=1, column=2, pady=10, ipadx=4)
        self.dimension_button['font'] = self.font_window
        self.close_DoE_button = Button(self.DoELevel, text='Close', command=lambda:self.DoELevel.destroy())
        self.close_DoE_button.grid(row=20, column=5, pady=10, ipadx=4)
        self.close_DoE_button['font'] = self.font_window
        self.compute_DoE_button = Button(self.DoELevel, text='Compute', command=self.compute_DoE_elements)
        self.save_DoE_button = Button(self.DoELevel, text='Save', command=self.save_DoE)

        self.nmbExpDoE = EntryItem(self.DoELevel, name='Number of Experiments', row=3, width=6)
        self.nmbLoops = EntryItem(self.DoELevel, name='Number of Loops', row=3, width=6)

        self.periodic_var = BooleanVar(); self.center_var = BooleanVar()
        self.check_periodic = Checkbutton(self.DoELevel, text='Periodic?', variable=self.periodic_var)
        self.check_center = Checkbutton(self.DoELevel, text='Center atom?', variable=self.center_var)


    def upload_table_txt(self):
        """
        Upload table from a Text Document (*.txt)
        """
        self.initial_file_ext.set('.txt')
        self.load_DoE_file()


    def upload_table_json(self):
        """
        Upload table from a JSON File (*.json)
        """
        self.initial_file_ext.set('.json')
        self.load_DoE_file()


    def upload_table_csv(self):
        """
        Upload table from a CSV File (*.csv)
        """
        self.initial_file_ext.set('.csv')
        self.load_DoE_file()


    def create_table_ML(self):
        """
        Create a table with N rows and M parameters
        """
        self.CreateTableLevel = Toplevel()
        self.CreateTableLevel.configure(bg=self._from_rgb((11, 165, 193)))
        self.CreateTableLevel.geometry("1000x700")
        #self.CreateTableLevel.iconbitmap('icon_band.ico')
        self.CreateTableLevel.grab_set()
        self.table_created = False

        #Texts
        self.CreateTable_input = Label(self.CreateTableLevel, text='Input parameters for Design of Experiments')
        self.CreateTable_input.grid(row=0, column=0, columnspan=3, pady=(10, 5))
        self.CreateTable_input['font'] = self.font_window

        #Entries
        self.dimensionsTable = EntryItem(self.CreateTableLevel, name='Number of Parameters', row=1, width=6)
        self.dimensionsTable.create_EntryItem(ipadx_label=0); self.dimensionsTable.initial_val = DoubleVar(); self.dimensionsTable.set_name(2)
        self.dimensionsEntries = EntryItem(self.CreateTableLevel, name='Number of Experiments', row=1, column=4, width=6)
        self.dimensionsEntries.create_EntryItem(ipadx_label=0); self.dimensionsEntries.initial_val = DoubleVar(); self.dimensionsEntries.set_name(6)

        #Buttons
        self.createTable_button = Button(self.CreateTableLevel, text='Create table', command=self.create_table_empty)
        self.createTable_button.grid(row=1, column=5, pady=10, ipadx=4)
        self.createTable_button['font'] = self.font_window

        self.save_DoE_Table_button = Button(self.CreateTableLevel, text='Save data', command=self.save_table)
        self.save_DoE_Table_button.grid(row=20, column=1, pady=10, ipadx=4)
        self.save_DoE_Table_button.config(state='disabled')
        self.save_DoE_Table_button['font'] = self.font_window
        self.close_DoE_Table_button = Button(self.CreateTableLevel, text='Close', command=self.close_CreateTable)
        self.close_DoE_Table_button.grid(row=20, column=5, pady=10, ipadx=4)
        self.close_DoE_Table_button['font'] = self.font_window


    def create_table_empty(self):
        """
        Use the number of parameters and experiments to create an empty table which can be uploaded for experiments
        """
        if self.table_created:
            self.tab._destroy_table()
            self.tab2._destroy_table()

        nmb_para = self.dimensionsTable.get_name()
        nmb_exp = self.dimensionsEntries.get_name()
        self.labels = list()

        for idx in range(int(nmb_para)):
            self.labels.append(f'Parameter {idx+1}')

        self.arr_table = np.zeros((int(nmb_para), int(nmb_exp)), dtype=float)

        self.tab = Table(self.CreateTableLevel, arr=self.arr_table, labels=self.labels, row=3, results=True)
        self.tab._create_table()
        
        self.arr_table2 = np.zeros((4, int(nmb_para)), dtype=float)
        labels_table2 = ['Parameters', 'Minimum', 'Maximum', 'Steps']
        
        self.tab2 = Table(self.CreateTableLevel, arr=self.arr_table2, labels=labels_table2,row=len(self.arr_table[0]) + 5)
        self.tab2._create_table()
        self.table_created = True
        self.save_DoE_Table_button.config(state='normal')


    def close_CreateTable(self):
        """
        Close CreateTable toplevel of the table and save the data in a table
        """
        _check_table, check_parameters = self._get_data_table()              

        if _check_table and check_parameters:
            self.run_ML_button.config(state='normal')
            self.CreateTableLevel.destroy()

        else:
            answer = messagebox.askokcancel('Exit?', 'The table is not completelty filled or it includes non numbers (for example, strings). Are you sure you want to exit?', icon='warning')
            if answer:
                self.filename.set_name('')
                self.CreateTableLevel.destroy()


    def create_dimension_entries(self):
        """
        Create entries for N-dimensional Design of Experiments approach
        """
        for idx, c in enumerate(self.Dimension_label):
            c.destroy(); self.Dimension_label_entry[idx].destroy()
            self.Dimension_min_entry[idx].destroy(); self.Dimension_max_entry[idx].destroy()
            self.Dimension_step_entry[idx].destroy()
            
        self.check_center.destroy(); self.check_periodic.destroy(); self.save_DoE_button.destroy()
        self.nmbExpDoE.destroy(); self.nmbLoops.destroy(); self.compute_DoE_button.destroy()

        self.Dimension_label = list(); self.Dimension_label_var = list(); self.Dimension_label_entry = list()
        self.Dimension_min_entry = list(); self.Dimension_max_entry = list(); self.Dimension_step_entry = list()
        self.Dimension_label_var = list(); self.Dimension_min_var = list(); self.Dimension_max_var = list()
        self.Dimension_step_var = list()

        nmb = 2
        for idx in range(int(self.dimensions.get_name())):
            self.Dimension_label.append(Label(self.DoELevel, text='Dimension {}'.format(idx+1)))
            self.Dimension_label[-1].grid(row=nmb, column=0, ipadx=26, pady=(10, 5))
            self.Dimension_label[-1]['font'] = self.font_window
            self.Dimension_label_var.append(DoubleVar())
            self.Dimension_label_entry.append(EntryItem(self.DoELevel, name='Label', row=nmb, column=2, width=15))
            self.Dimension_label_entry[-1].create_EntryItem(ipadx_label=5); self.Dimension_label_entry[-1].set_name(f"Parameter{idx +1}")
            self.Dimension_min_var.append(DoubleVar())
            self.Dimension_min_entry.append(EntryItem(self.DoELevel, name='Minimum', row=nmb, column=4, width=8))
            self.Dimension_min_entry[-1].create_EntryItem(ipadx_label=5); self.Dimension_min_entry[-1].set_name(0.9)
            self.Dimension_max_var.append(DoubleVar())
            self.Dimension_max_entry.append(EntryItem(self.DoELevel, name='Maximum', row=nmb, column=6, width=8))
            self.Dimension_max_entry[-1].create_EntryItem(ipadx_label=5); self.Dimension_max_entry[-1].set_name(1.1)
            self.Dimension_step_var.append(DoubleVar())
            self.Dimension_step_entry.append(EntryItem(self.DoELevel, name='Step size', row=nmb, column=8, width=8))
            self.Dimension_step_entry[-1].create_EntryItem(ipadx_label=5); self.Dimension_step_entry[-1].set_name(0.01)
            nmb += 1

        self.nmbExpDoE = EntryItem(self.DoELevel, name='Number of Experiments', row=nmb, width=6)
        self.nmbExpDoE.create_EntryItem(ipadx_label=0); self.nmbExpDoE.initial_val = DoubleVar(); self.nmbExpDoE.set_name(3*int(self.dimensions.get_name()))
        self.nmbLoops = EntryItem(self.DoELevel, name='Number of Loops', row=nmb, column=3, width=10)
        self.nmbLoops.create_EntryItem(ipadx_label=0); self.nmbLoops.initial_val = DoubleVar(); self.nmbLoops.set_name(10000)

        self.compute_DoE_button = Button(self.DoELevel, text='Compute', command=self.compute_DoE_elements)
        self.compute_DoE_button.grid(row=nmb, column=8,  pady=10, ipadx=4)
        self.compute_DoE_button['font'] = self.font_window
        self.save_DoE_button = Button(self.DoELevel, text='Save', command=self.save_DoE)
        self.save_DoE_button.grid(row=nmb+1, column=0, columnspan=2, pady=10, ipadx=4)
        self.save_DoE_button['font'] = self.font_window
        self.save_DoE_button.config(state= 'disabled')
       
        if self.DoE_mode == 'create':
            self.periodic_var = BooleanVar(); self.center_var = BooleanVar()
            self.check_periodic = Checkbutton(self.DoELevel, text='Periodic?', variable=self.periodic_var)
            self.check_periodic.grid(row=nmb, column=4, columnspan=2, ipadx=20)
            self.check_center = Checkbutton(self.DoELevel, text='Center atom?', variable=self.center_var)
            self.check_center.grid(row=nmb, column=6, columnspan=2, ipadx=28)


    def save_DoE_manual(self):  #Not sure if we need this
        """
        Close the toplevel of the table and save the data in a table
        """
        _check_table, check_parameters = self._get_data_table()              

        if _check_table and check_parameters:
            self.run_ML_button.config(state='normal')
            self.TableLevel.destroy()

        else:
            answer = messagebox.askokcancel('Exit?', 'The table is not completelty filled or it includes non numbers (for example, strings). Are you sure you want to exit?', icon='warning')
            if answer:
                self.filename.set_name('')
                self.TableLevel.destroy()


    def save_DoE(self):
        """
        Open folder and save the DoE data as .txt file and .json file
        """
        files = [('All Files', '*.*'), 
             ('JSON Files', '*.json'),
             ('Text Documents', '*.txt')]
        filename = filedialog.asksaveasfilename(title='Save file', defaultextension="*.*", filetypes=files)
        if filename == '':
            return

        path = filename.split('.')[0]
        arr_data = self.LS.array_min
        
        dic = {}
        for idx, lab in enumerate(self.labels):
            dic.update({lab: arr_data[idx].tolist()})

        dic.update({'minimum': self.arr_min.tolist()})
        dic.update({'maximum': self.arr_max.tolist()})
        dic.update({'steps': self.arr_step.tolist()})

        with open(f'{path}.json', 'w') as fil:
            json.dump(dic, fil)

        with open(f'{path}.txt', 'w') as fil:
            for lab in self.labels:
                fil.write(lab + " ")
            fil.write(" \n")

            for x in range(len(arr_data[0])):
                for y in range(len(arr_data)):
                    fil.write(str(arr_data[y][x]) + " ")
                fil.write(" \n")


    def compute_DoE_elements(self):
        """
        Compute the elements for each parameter and save the results
        """
        self.labels = np.zeros(len(self.Dimension_label_entry), dtype=np.dtype('U100'))
        self.arr_min = np.zeros(len(self.Dimension_min_entry), dtype=float)
        self.arr_max = np.zeros_like(self.arr_min); self.arr_step = np.zeros_like(self.arr_min)

        for idx, lab in enumerate(self.Dimension_label_entry):
            self.labels[idx] = lab.get_name()
            self.arr_min[idx] = self.Dimension_min_entry[idx].get_name()
            self.arr_max[idx] = self.Dimension_max_entry[idx].get_name()
            self.arr_step[idx] = self.Dimension_step_entry[idx].get_name()

        nmbExp = int(self.nmbExpDoE.get_name()); nmbLoop = int(self.nmbLoops.get_name())
        self.LS = DesignOfExperiments(
            arr_min=self.arr_min,
            arr_max=self.arr_max,
            arr_step=self.arr_step,
            nmb_exp=nmbExp,
            run_nmb=nmbLoop, 
        )

        self.LS.center = self.center_var.get()
        self.LS.period = self.periodic_var.get()

        self.LS._run_DoE()
        self._plot_DoE()
        self.save_DoE_button.config(state='normal')
        

    def _plot_DoE(self):
        """
        If data is two or three dimension, plot data
        """
        check_figure = True
        if len(self.arr_min) == 2:
            self.LS._plot_2D(xlabel=self.labels[0], ylabel=self.labels[1])

        elif len(self.arr_min) == 3:
            self.LS._plot_3D(xlabel=self.labels[0], ylabel=self.labels[1], zlabel=self.labels[2])
        
        else:
            check_figure = False
        
        if check_figure:
            self.DoE_FigureLevel = Toplevel()
            self.DoE_FigureLevel.configure(bg=self._from_rgb((11, 165, 193)))
            self.DoE_FigureLevel.geometry("1000x700")
            #self.TableLevel.iconbitmap('icon_band.ico')
            self.DoE_FigureLevel.grab_set()

            self.canvas_DoE = FigureCanvasTkAgg(self.LS.fig, master=self.DoE_FigureLevel)
            self.canvas_DoE.draw()
            self.plot_widget = self.canvas_DoE.get_tk_widget()
            self.plot_widget.grid(row=1, column=1, columnspan=11, rowspan=11)

            toolbar_frame = Frame(self.DoE_FigureLevel) 
            toolbar_frame.grid(row=13,column=2,columnspan=4) 
            toolbar = NavigationToolbar2Tk(self.canvas_DoE, toolbar_frame)
            toolbar.update()

            self.close_DoE_Plot_button = Button(self.DoE_FigureLevel, text='Close', command=self._close_DoE_Plot)
            self.close_DoE_Plot_button.grid(row=20, column=5, pady=10, ipadx=4)
            self.close_DoE_Plot_button['font'] = self.font_window
            self.save_DoE_Plot_button = Button(self.DoE_FigureLevel, text='Save', command=self.save_DoE_Plot)
            self.save_DoE_Plot_button.grid(row=20, column=4, pady=10, ipadx=8)
            self.save_DoE_Plot_button['font'] = self.font_window


    def _close_DoE_Plot(self):
        """
        Close the plot window
        """
        self.plot_widget.destroy()
        self.DoE_FigureLevel.destroy()


    def save_DoE_Plot(self):
        """
        Save DoE figure with a different resolution and size
        """
        files = [
             ('PNG Files', '*.png'),
             ('JPG Files', '*.jpg')
             ]
        filename = filedialog.asksaveasfilename(title='Save figure', defaultextension="*.*", filetypes=files)
        self.LS.fig.set_size_inches(12, 8)
        self.LS.fig.savefig(filename, dpi=600)

        
    def update_DoE(self):
        """
        Upload machine learning file to update the DoE approach with a new constraint that only the highest, lowest or desired values will be used
        """
        self.create_DoE()
        self.dimension_button.config(state = 'disabled')

        self.upload_classification_button = Button(self.DoELevel, text='Upload Classification', command=self._upload_classification)
        self.upload_classification_button.grid(row=1, column=3, pady=10, ipadx=4)
        self.upload_classification_button['font'] = self.font_window


    def nmb_decimal(self, lst):
        """
        Find the number of decimal numbers

        Input:
        ----------------
        lst: list of floats

        Output:
        -----------------
        step: float
        """
        nmb = 0; five = False
        for l in lst:
            if len(str(l).split('.')[1]) > nmb or (len(str(l).split('.')[1]) == nmb and str(l)[-1] != '5'):
                nmb = len(str(l).split('.')[1])
                if str(l)[-1] == '5':
                    five = True
                else:
                    five = False
        step = '0.'
        for i in range(nmb-1):
            step += '0'
        if five:
            return float(step + '5')
        else:
            return float(step + '1')


    def _upload_classification(self): 
        """
        Upload a classification file which has new restriction which depends on the preference:
            - maximum
            - minimum
            - specific value

        JSON file needs to be a classification file
        """
        file = filedialog.askopenfile(mode ='r', filetypes =[('JSON File', '*.json')])
        if file is None:
            return

        with open(file.name) as fil:
            data_json = json.load(fil)

        if 'algorithm' not in data_json:
            return

        if data_json['algorithm'] != 'Classification':
            print(data_json['algorithm'])
            return
        
        self.DoE_mode = 'Update'

        self.dimensions.disable()
        self.dimensions.set_name(len(data_json['minimum']))
        self.create_dimension_entries()
        nmb = 2; self.previous_pts = list()
        for idx, para in enumerate(data_json['labels']):
            self.Dimension_label_entry[idx].set_name(para)
            self.Dimension_min_entry[idx].set_name(data_json['minimum'][idx])
            self.Dimension_max_entry[idx].set_name(data_json['maximum'][idx])
            steps = (data_json['maximum'][idx] - data_json['minimum'][idx]) / 10
            self.previous_pts.append(data_json[para])
            self.Dimension_step_entry[idx].set_name(f'{self.nmb_decimal(data_json[para])}')
            nmb += 1

        self.dimensions_class = data_json['axis_ML']
        self.intensity_class = np.array(data_json['slice_intensity'])
        self.expected_value_label = Label(self.DoELevel, text='Expected Value')
        self.expected_value_label.grid(row=nmb+1, column=2, columnspan=1, pady=(10, 5))

        self.val_classification = data_json['pred_results'] 
        min_exp_value = np.min(np.array(self.val_classification))
        max_exp_value = np.max(np.array(self.val_classification))
        
        self.desired_value_label = Label(self.DoELevel, text=f'Choose a value between {min_exp_value} and {max_exp_value} for the desired value.')
        self.desired_value_label.grid(row=nmb+2, column=3, columnspan=3, pady=(10, 5))
        self.expected_value_options = ["Maximum", "Minimum",  "Desired"]
        self.initial_expected_val = StringVar(); self.initial_expected_val.set(self.expected_value_options[0])
        self.expected_value_menu = OptionMenu(self.DoELevel, self.initial_expected_val, *self.expected_value_options)
        self.expected_value_menu.grid(row=nmb+1, column=3, columnspan=1, ipadx=20)
        self.compute_upd_DoE_button = Button(self.DoELevel, text='Compute', command=self._compute_updated_DoE)
        self.compute_upd_DoE_button.grid(row=nmb+1, column=8,  pady=10, ipadx=4)
        self.compute_upd_DoE_button['font'] = self.font_window
        self.compute_DoE_button.grid_forget()
        
        self.uncertainty_exp_val = EntryItem(self.DoELevel, name='Desired Value', row=nmb+1, column=5, width=6)
        self.uncertainty_exp_val.create_EntryItem(ipadx_label=0); self.uncertainty_exp_val.initial_val = DoubleVar(); self.uncertainty_exp_val.set_name((min_exp_value + max_exp_value) / 2)


    def _compute_updated_DoE(self):
        """
        Compute the updated DoE including the classification as restriction
        """
        self.labels = np.zeros(len(self.Dimension_label_entry), dtype=np.dtype('U100'))
        self.arr_min = np.zeros(len(self.Dimension_min_entry), dtype=float)
        self.arr_max = np.zeros_like(self.arr_min); self.arr_step = np.zeros_like(self.arr_min)
        
        if self.initial_expected_val.get() == self.expected_value_options[0]:
            expected_val = [np.max(self.val_classification)]
        
        elif self.initial_expected_val.get() == self.expected_value_options[1]:
            expected_val = [np.min(self.val_classification)]
        
        elif self.initial_expected_val.get() == self.expected_value_options[2]:
        
            if float(self.uncertainty_exp_val.get_name()) in self.val_classification:
                expected_val = self.uncertainty_exp_val.get_name()
        
            else:
                min_x = -1E100; max_x = 1E100
                for x in self.val_classification:
                    if x - float(self.uncertainty_exp_val.get_name()) < 0 and np.abs(x - float(self.uncertainty_exp_val.get_name())) < float(self.uncertainty_exp_val.get_name()) - min_x:
                        min_x = x
                    if x - float(self.uncertainty_exp_val.get_name()) > 0 and np.abs(x - float(self.uncertainty_exp_val.get_name())) < max_x - float(self.uncertainty_exp_val.get_name()):
                        max_x = x
                expected_val = [min_x, max_x]

        nmbExp = int(self.nmbExpDoE.get_name()); nmbLoop = int(self.nmbLoops.get_name())
        for idx, lab in enumerate(self.Dimension_label_entry):
            self.labels[idx] = lab.get_name()
            self.arr_min[idx] = self.Dimension_min_entry[idx].get_name()
            self.arr_max[idx] = self.Dimension_max_entry[idx].get_name()
            self.arr_step[idx] = self.Dimension_step_entry[idx].get_name()

        print(self.labels)
        self.LS = DesignOfExperiments(
            arr_min=self.arr_min,
            arr_max=self.arr_max,
            arr_step=self.arr_step,
            nmb_exp=nmbExp,
            run_nmb=nmbLoop, 
        )

        self.LS._set_range()
        dimensions = list()
        for idx, d in enumerate(self.LS.max_step):
            arr = np.arange(d+1) * self.arr_step[idx] + self.arr_min[idx]
            dimensions.append(arr.tolist())
        compare_dim = list(); index_list = list(); previous_pt_list = np.zeros((len(self.previous_pts), len(self.previous_pts[0])), dtype=float)
        for idx, d in enumerate(dimensions): #d = 0 --> x, d = 1 --> y
            err = np.abs(float(self.dimensions_class[idx][0]) - float(self.dimensions_class[idx][1])) / 2
            compare_dim1 = list(); index_list1 = list()
            for i, v in enumerate(d): # v = steps in x or y
                for idx2, x in enumerate(self.dimensions_class[idx]): #x steps in x or y
                    if np.abs(v - x) < err and v not in self.previous_pts[idx]:
                        compare_dim1.append(idx2); index_list1.append(i)

                    if np.abs(v - x) < err and v in self.previous_pts[idx]:
                        for pp in range(len(self.previous_pts[idx])):
                            if self.previous_pts[idx][pp] == v:
                                previous_pt_list[idx][pp] = float(i)    
            compare_dim.append(compare_dim1); index_list.append(index_list1)

        constraint_params = list()
        constraint_index = np.array(np.meshgrid(*index_list)).T.reshape(-1, len(index_list))
        vx = np.array(np.meshgrid(*compare_dim)).T.reshape(-1, len(compare_dim))
        arr_row_col = zip(vx.T)

        constraint_params = np.argwhere(np.array(self.intensity_class).T[*arr_row_col][0] == expected_val[0])
        indeces_list = constraint_index[constraint_params.reshape(len(constraint_params))]
        int_list = vx[constraint_params.reshape(len(constraint_params))]
        #print(indeces_list, 'il')
        
        if len(self.arr_min) == 2:
            constraint2 = np.array(indeces_list, dtype=float).T
        elif len(self.arr_min) > 2:
            indeces_list2 = indeces_list[:, ::-1]
            constraint2 = np.array(indeces_list2, dtype=float).T
            """
            fig = plt.figure(figsize = (10, 7))
            ax = plt.axes(projection ="3d")
            ax.scatter3D(*constraint2, color = "green")
            ax.set_xlabel('X-axis', fontweight ='bold') 
            ax.set_ylabel('Y-axis', fontweight ='bold') 
            ax.set_zlabel('Z-axis', fontweight ='bold')
            ax.set_xlim(0, 40)
            ax.set_ylim(0, 40)
            ax.set_zlim(0, 40)
            plt.show()
            for idx, x in enumerate(indeces_list2):
                print(f'{x}, Te: {dimensions[0][x[0]]}, Sb: {dimensions[1][x[1]]}, Ag: {dimensions[2][x[2]]}, int: {self.intensity_class.T[*int_list[idx]]}')
        print(constraint2)
        print(indeces_list, indeces_list.shape, int_list, int_list.shape, self.intensity_class.shape)
        """
 
        update_data = True
        for idx, lst in enumerate(constraint2):
            if len(set(lst)) < 2 * int(nmbExp):
                messagebox.showerror("Too less data points", f"For {self.labels[idx]}, there are only {len(set(lst))} datapoints but {int(nmbExp)} experiments. Shift the steps by one decimal place!")
                update_data = False

        if update_data:
            self.LS.update_list = constraint2
            self.LS.previous_pts = previous_pt_list.tolist()
            self.LS._run_DoE()
            self._plot_DoE()


    def _loop_arr(self, arr, idx):
        """
        Loop through n-dimensional array

        Input:
        -------------------------
        arr: ndarray
            n-dimensional array
        idx: int
            index of the array
        """
        return arr[idx]


    def _load_txt_file(self):
        """
        Load data from a .txt file

        Output:
        -----------------------
        load_file: Boolean
            True if there is a file, False if not
        """
        file = filedialog.askopenfile(mode ='r', filetypes =[('Text Document', '*.txt')])
        if file is None:
            return False

        else:
            with open(file.name) as fil:
                data_txt = fil.readlines()
            
            self.name = file.name
            file_ext = 'txt'

            self.labels = []; self.arr_table = np.zeros((len(data_txt[0].split()), len(data_txt)-1), dtype=float)
            
            for r in range(len(data_txt)):
                for c in range(len(data_txt[0].split())):
                    if r == 0:
                        self.labels.append(data_txt[r].split()[c])
                    else:
                        self.arr_table[c][r-1] = data_txt[r].split()[c]

            if self.CheckResultVar.get():
                self.arr_table2 = np.zeros((4, len(data_txt[0].split())-1), dtype=np.dtype('U100'))
                
            else:
                self.arr_table2 = np.zeros((4, len(data_txt[0].split())), dtype=np.dtype('U100'))

            for r in range(len(self.arr_table2[0])):
                self.arr_table2[0][r] = self.labels[r]

            return True


    def _load_json_file(self):
        """
        Load data from a .json file

        Output:
        ----------------------
        result_data: ndarray, dtype: float
            Array of results (if given in JSON file)
        load_file: Boolean
            True if there is a file, False if not
        """
        result_data = []
        file = filedialog.askopenfile(mode ='r', filetypes =[('JSON File', '*.json')])
        if file is None:
            return [], False

        else:
            with open(file.name) as fil:
                data_json = json.load(fil)

            self.name = file.name 
            file_ext = 'json'

            keys = list(data_json.keys()); para = len(keys)-3
            if 'results' in keys:
                result_data = np.array(data_json['results'])
                para -= 1

            max_length = 0
            for key in keys:
                if len(data_json[key]) > max_length:
                    max_length = len(data_json[key])

            self.labels = []; self.arr_table = np.zeros((para, max_length), dtype=float)
            
            self.arr_table2 = np.zeros((4, para), dtype=np.dtype('U100'))
            count = 0
            for key in data_json.keys():
                
                if key not in ['minimum', 'maximum', 'steps', 'results']:
                    self.labels.append(key); self.arr_table2[0][count] = key
                    for r in range(len(data_json[key])):                      
                        self.arr_table[count][r] = data_json[key][r]
                    count += 1

                else:
                    for idx in range(para):
                        if key == 'minimum':    
                            self.arr_table2[1][idx] = data_json[key][idx]
                        elif key == 'maximum':
                            self.arr_table2[2][idx] = data_json[key][idx]
                        elif key == 'steps':
                            self.arr_table2[3][idx] = data_json[key][idx]
            
            return result_data,True


    def _load_csv_file(self):
        """
        Load data from a .csv file
        
        Output:
        ----------------------------
        load_file: Boolean
            True if there is a file, False if not
        """
        file = filedialog.askopenfile(mode ='r', filetypes =[('Comma Delimited File', '*.csv')])
        if file is None:
            return False

        else:
            with open(file.name) as fil:
                data_txt = fil.readlines()
            
            self.name = file.name
            file_ext = 'csv'

            self.labels = []; self.arr_table = np.zeros((len(data_txt[0].split(',')), len(data_txt)-1), dtype=float)
         
            for r in range(len(data_txt)):
                for c in range(len(data_txt[0].split(','))):
                    if r == 0:
                        self.labels.append(data_txt[r].split(',')[c])
                    else:
                        self.arr_table[c][r-1] = data_txt[r].split(',')[c]

            if self.CheckResultVar.get():
                self.arr_table2 = np.zeros((4, len(data_txt[0].split(','))-1), dtype=np.dtype('U100'))
                
            else:
                self.arr_table2 = np.zeros((4, len(data_txt[0].split(','))), dtype=np.dtype('U100'))

            for r in range(len(self.arr_table2[0])):
                self.arr_table2[0][r] = self.labels[r]

            return True


    def load_DoE_file(self):
        """
        Load DoE file (.txt or .json or .csv) to create a table and perform machine learning on it
        """
        load_file = False; result_data = []
        if self.initial_file_ext.get() == '.txt':
            load_file = self._load_txt_file()

        elif self.initial_file_ext.get() == '.json':
            result_data, load_file = self._load_json_file()

        elif self.initial_file_ext.get() == '.csv':
            load_file = self._load_csv_file()                

        if load_file:
            self.TableLevel = Toplevel()
            self.TableLevel.configure(bg=self._from_rgb((11, 165, 193)))
            self.TableLevel.geometry("1000x700")
            #self.TableLevel.iconbitmap('icon_band.ico')
            self.TableLevel.grab_set()

            self.tab = Table(self.TableLevel, arr=self.arr_table, labels=self.labels, column=0, results=True)
            if self.initial_file_ext.get() == '.json':
                if len(result_data) > 0:
                    self.tab.results_data = result_data
            
            else:
                if self.CheckResultVar.get():
                    self.tab.results = False

            self.tab._create_table()
            
            labels_table2 = ['Parameters', 'Minimum', 'Maximum', 'Steps']
            
            self.tab2 = Table(self.TableLevel, arr=self.arr_table2, labels=labels_table2, column=0, row=len(self.arr_table[0]) + 2)
            self.tab2._create_table()

            self.save_DoE_Table_button = Button(self.TableLevel, text='Save data', command=self.save_table)
            self.save_DoE_Table_button.grid(row=20, column=0, pady=10, ipadx=4)
            self.save_DoE_Table_button['font'] = self.font_window
            self.close_DoE_Table_button = Button(self.TableLevel, text='Close', command=self.close_table)
            self.close_DoE_Table_button.grid(row=20, column=2, pady=10, ipadx=4)
            self.close_DoE_Table_button['font'] = self.font_window


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


    def _get_data_table(self):
        """
        Get data from table for machine learning and dimensions

        Output:
        ------------------------------
        _check_table, check_parameters: Boolean
            If all values in the table are floats, value = True
        """
        _check_table = True; check_parameters = True
        self.table_data = np.zeros((len(self.tab.table), len(self.tab.table[0])), dtype=float)
        for c in range(len(self.tab.table)):
            for r in range(len(self.tab.table[c])):
                
                if self.is_float(self.tab.table[c][r].get()):
                    self.table_data[c][r] = self.tab.table[c][r].get()
                else:
                    _check_table = False

        self.para_labels = list(); self.para_min = np.zeros(len(self.tab2.table), dtype=float)
        self.para_max = np.zeros_like(self.para_min); self.para_steps = np.zeros_like(self.para_min)
    
        for c in range(len(self.tab2.table)):
            for r in range(len(self.tab2.table[c])):

                if r == 0:
                    self.para_labels.append(self.tab2.table[c][r].get())
                else:
                    if self.is_float(self.tab2.table[c][r].get()):
                        
                        if r == 1:
                            self.para_min[c] = self.tab2.table[c][r].get()
                        elif r == 2:
                            self.para_max[c] = self.tab2.table[c][r].get()
                        elif r == 3:
                            self.para_steps[c] = self.tab2.table[c][r].get()
                    else:
                        check_parameters = False

        return _check_table, check_parameters


    def close_table(self):
        """
        Close the toplevel of the table and save the data in a table
        """
        _check_table, check_parameters = self._get_data_table()              

        if _check_table and check_parameters:
            self.run_ML_button.config(state='normal')
            self.save_ML_button.config(state='disable')
            self.replot_ML_button.config(state='disable')
            self.save_MLPlot_button.config(state='disable')
            self.fix_parameters_button.config(state='disable')
            self.filename.set_name(self.name)
            self.TableLevel.destroy()

        else:
            answer = messagebox.askokcancel('Exit?', 'The table is not completelty filled or it includes non numbers (for example, strings). Are you sure you want to exit?', icon='warning')
            if answer:
                self.filename.set_name('')
                self.TableLevel.destroy()


    def save_table(self):
        """
        Save data into a .json file (update .json file when it is exists in the same folder)
        """
        _check_table, check_parameters = self._get_data_table()

        if _check_table and check_parameters:
            
            files = [('JSON Files', '*.json')]
            filename = filedialog.asksaveasfilename(title='Save file', defaultextension="*.*", filetypes=files)
            
            if filename == '':
                return
            
            path = filename.split('.')[0]

            results = np.transpose(self.table_data)[-1]
            data = np.transpose(self.table_data)[:-1]
            dic = {'minimum': self.para_min.tolist(), 'maximum': self.para_max.tolist(), 'steps': self.para_steps.tolist(), 'results': results.tolist()}
            for idx, p in enumerate(data):
                dic.update({self.para_labels[idx]: p.tolist()})

            with open(f'{path}.json', 'w') as fil:
                json.dump(dic, fil)          

        else:
            answer = messagebox.showerror('Save', 'Data cannot be saved. The table is not completelty filled or it includes non numbers (for example, strings).', icon='warning')
            

    def run_ML(self):
        """
        Perform a specific machine learning approach
        """
        data = deepcopy(self.table_data)
        self.MLrun = MachineLearning(arr=data, para_min=self.para_min, para_max=self.para_max, para_steps=self.para_steps, labels=self.para_labels, epsilon=self.epsilon.get_name(), gamma=self.gamma.get_name(), regularization=self.regularization.get_name())
        self.MLrun._get_data_arr()
        if self.initial_ML_options.get() == self.ML_options[0]:
            self.MLrun._svmc()
            self.ML_program = 'Classification'
        elif self.initial_ML_options.get() == self.ML_options[1]:
            self.MLrun._svmr()
            self.ML_program = 'Regression'
    
        self.MLrun.font_label_size = 1.1 * float(self.font_size.get())
        self.MLrun.font_size = self.font_size.get()
        self._plot_pre_exp()
        self._plot_slice()
        self.para_x_menu.destroy(); self.para_y_menu.destroy()
        self.parameter_options = self.para_labels
        self.initial_parameter_x_option = StringVar(); self.initial_parameter_x_option.set(self.parameter_options[0])
        self.para_x_menu = OptionMenu(self.parent, self.initial_parameter_x_option, *self.parameter_options)
        self.para_x_menu.grid(row=14, column=1, padx=10, pady=10, ipadx=20)
        self.initial_parameter_y_option = StringVar(); self.initial_parameter_y_option.set(self.parameter_options[1])
        self.para_y_menu = OptionMenu(self.parent, self.initial_parameter_y_option, *self.parameter_options)
        self.para_y_menu.grid(row=15, column=1, padx=10, pady=10, ipadx=20)
        self.save_ML_button.config(state='normal')
        self.replot_ML_button.config(state='normal')
        self.save_MLPlot_button.config(state='normal')
        if len(self.para_min) > 2:
            self.fix_parameters_button.config(state='normal')
        else:
            self.fix_parameters_button.config(state='disable')


    def save_ML(self):
        """
        Save machine learning data
        """
        files = [('JSON Files', '*.json')]
        filename = filedialog.asksaveasfilename(title='Save file', defaultextension="*.*", filetypes=files)
        
        if filename == '':
            return

        axis_ML = list()
        for x in range(len(self.para_min)):
            axis_ML.append(np.linspace(self.para_min[x], self.para_max[x], self.MLrun.steps[x]).tolist())

        predicted_results = self.MLrun.predicted_results / self.MLrun._scale_float2int
        prediction = self.prediction / self.MLrun._scale_float2int
        dic = {
            'minimum': self.para_min.tolist(), 
            'maximum': self.para_max.tolist(), 
            'steps': self.MLrun.steps.tolist(), 
            'labels': self.para_labels,
            'results': self.MLrun.arr_results.tolist(),
            'exp_results': self.MLrun.arr_results.tolist(),
            'pred_results': predicted_results.tolist(),
            'algorithm' : self.ML_program,
            'axis_ML' : axis_ML,
            'slice_intensity' : prediction.tolist(),
            }
        for idx, p in enumerate(self.MLrun.arr[:-1]):
            dic.update({self.para_labels[idx]: p.tolist()})

        with open(filename, 'w') as fil:
            json.dump(dic, fil)  
        

    def _load_ML_file(self):
        """
        Load Machine learning file (.json)
        """
        files = [('JSON Files', '*.json')]
        filename = filedialog.askopenfilename(title='Save file', defaultextension="*.*", filetypes=files)
        
        if filename == '':
            return

        with open(filename) as fil:
            dic_ML = json.load(fil)

        self.para_min = dic_ML['minimum'] 
        self.para_max = dic_ML['maximum'] 
        self.para_steps = list()
        for idx in range(len(self.para_min)):
            self.para_steps.append((dic_ML['maximum'][idx] - dic_ML['minimum'][idx]) / dic_ML['steps'][idx])
        self.para_labels = dic_ML['labels']
        experiment_results = dic_ML['exp_results']
        predicted_results = dic_ML['pred_results']
        axis_ML = dic_ML['axis_ML']
        prediction = dic_ML['slice_intensity']
        self.ML_program = dic_ML['algorithm']
        arr = list()
        for p in self.para_labels:
            arr.append(dic_ML[p])
        arr.append(experiment_results)
        self.table_data = np.array(arr).T

        if self.ML_program == 'Classification':
            self.initial_ML_options.set(self.ML_options[0])

        if self.ML_program == 'Regression':
            self.initial_ML_options.set(self.ML_options[0])

        self.MLrun = MachineLearning(arr=self.table_data, para_min=self.para_min, para_max=self.para_max, para_steps=self.para_steps, labels=self.para_labels, epsilon=self.epsilon.get_name(), gamma=self.gamma.get_name(), regularization=self.regularization.get_name())
        self.prediction = np.array(prediction) * self.MLrun._scale_float2int
        self.MLrun.predicted_results = np.array(predicted_results) * self.MLrun._scale_float2int
        self.MLrun.arr_results = experiment_results
       
        self.idx_max = np.unravel_index(np.argmax(self.prediction, axis=None), self.prediction.shape)
        self.idx_min = np.unravel_index(np.argmin(self.prediction, axis=None), self.prediction.shape)

        self._plot_pre_exp()
        self._plot_slice(replot=True)

        self.para_x_menu.destroy(); self.para_y_menu.destroy()
        self.parameter_options = self.para_labels
        self.initial_parameter_x_option = StringVar(); self.initial_parameter_x_option.set(self.parameter_options[0])
        self.para_x_menu = OptionMenu(self.parent, self.initial_parameter_x_option, *self.parameter_options)
        self.para_x_menu.grid(row=14, column=1, padx=10, pady=10, ipadx=20)
        self.initial_parameter_y_option = StringVar(); self.initial_parameter_y_option.set(self.parameter_options[1])
        self.para_y_menu = OptionMenu(self.parent, self.initial_parameter_y_option, *self.parameter_options)
        self.para_y_menu.grid(row=15, column=1, padx=10, pady=10, ipadx=20)
        self.run_ML_button.config(state='normal')
        self.save_ML_button.config(state='normal')
        self.replot_ML_button.config(state='normal')
        self.save_MLPlot_button.config(state='normal')
        if len(self.para_min) > 2:
            self.fix_parameters_button.config(state='normal')
        else:
            self.fix_parameters_button.config(state='disable')
        

    def replot_ML_data(self):
        """
        Replot data with new dimensions
        """
        x_axis = self.initial_parameter_x_option.get()
        y_axis = self.initial_parameter_y_option.get()
        if x_axis == y_axis:
            messagebox.showerror('Same parameter', 'The same parameter was chosen for the x- and y-axis. Please choose a different one for one of the axes.')
            return    
        dim = np.zeros(2, dtype=int)
        for idx, opt in enumerate(self.parameter_options):
            if opt == x_axis:
                dim[0] = idx
            elif opt == y_axis:
                dim[1] = idx

        self._plot_pre_exp()
        self._plot_slice(dim, replot=True)
        self.para_x_menu.destroy(); self.para_y_menu.destroy()
        self.parameter_options = self.para_labels   
        self.initial_parameter_x_option = StringVar(); self.initial_parameter_x_option.set(x_axis)
        self.para_x_menu = OptionMenu(self.parent, self.initial_parameter_x_option, *self.parameter_options)
        self.para_x_menu.grid(row=14, column=1, padx=10, pady=10, ipadx=20)
        self.initial_parameter_y_option = StringVar(); self.initial_parameter_y_option.set(y_axis)
        self.para_y_menu = OptionMenu(self.parent, self.initial_parameter_y_option, *self.parameter_options)
        self.para_y_menu.grid(row=15, column=1, padx=10, pady=10, ipadx=20)
      

    def save_ML_plot(self):
        """
        Save the experiment-prediction and the regression/classification plots
        """
        files = [('PNG Files', '*.png'), ('JPEG Files', '*.jpg') ]
        filename = filedialog.asksaveasfilename(title='Save file', defaultextension="*.*", filetypes=files)
        
        if filename == '':
            return

        exp_result = self.MLrun.arr_results
        pred_result = self.MLrun.predicted_results / self.MLrun._scale_float2int

        plt.rcParams["font.family"] = self.initial_font.get()
        plt.rcParams.update({'font.size': self.font_size.get()})
        fig_predict = Figure(figsize=(self.size_x.get(), self.size_y.get()), dpi=self.resolution_plot)
        ax2 = fig_predict.add_axes([self.size_x_space.get(), self.size_y_space.get(), self.size_x_length.get(), self.size_y_length.get()])
        
        ax2.scatter(
            exp_result, 
            pred_result, 
            edgecolor='k')
        ax2.plot([np.min(exp_result) - 100, np.max(exp_result) + 100], [np.min(exp_result) - 100, np.max(exp_result) + 100], ls="--", c=".3")
        ax2.set_xlabel('Experiments')
        ax2.set_ylabel('Prediction')
        ax2.set_xlim(np.min(exp_result) - 0.15 * np.abs(np.min(exp_result)), np.max(exp_result) * 1.15)
        ax2.set_ylim(np.min(pred_result) - 0.15 * np.abs(np.min(pred_result)), np.max(pred_result) * 1.15)
        plt.gcf()
        fig_predict.savefig(filename)

        labels = self.para_labels
        real_indeces = np.arange(0, len(labels))

        for idx, l in enumerate(labels):
            if l == self.initial_parameter_x_option.get():
                if (real_indeces[0] == 1 and real_indeces[1] == 0 and idx == 1):
                    pass
                else:
                    real_indeces[0], real_indeces[idx] = real_indeces[idx], real_indeces[0]
   
            elif l == self.initial_parameter_y_option.get():
       
                real_indeces[1], real_indeces[idx] = real_indeces[idx], real_indeces[1]
      
        fig_ML = Figure(figsize=(self.size_x.get(), self.size_y.get()), dpi=100)
        ax = fig_ML.add_axes([self.size_x_space.get(), self.size_y_space.get(), self.size_x_length.get(), self.size_y_length.get()])
        cm = ax.pcolormesh(self.xs, self.ys, self.prediction2 / self.MLrun._scale_float2int, shading='auto', cmap='viridis')
        cs = ax.contour(self.xs, self.ys, self.prediction2 / self.MLrun._scale_float2int, origin='lower', extend='both', colors='k',
                linewidths=2)
        if self.MLrun.label_con:
            ax.clabel(cs, inline=5, fontsize=self.font_size.get())
        ax.set_xlabel(self.para_labels[real_indeces[0]], fontsize=self.MLrun.font_label_size)
        ax.set_ylabel(self.para_labels[real_indeces[1]], fontsize=self.MLrun.font_label_size)
        ax.scatter(self.MLrun.arr[real_indeces[0]], self.MLrun.arr[real_indeces[1]], marker='*', c='white', edgecolor='red', s=300)
        ax.set_xlim(self.para_min[real_indeces[0]], self.para_max[real_indeces[0]])
        ax.set_ylim(self.para_min[real_indeces[1]], self.para_max[real_indeces[1]])
        
        plt.gcf()
        fil = filename.split('.')[0] + '_ML.' + filename.split('.')[1]
        fig_ML.savefig(fil)


    def _plot_pre_exp(self):
        """
        Plot experimental values versus predicted values
        """
        exp_result = self.MLrun.arr_results
        pred_result = self.MLrun.predicted_results / self.MLrun._scale_float2int

        plt.rcParams["font.family"] = self.initial_font.get()
        plt.rcParams.update({'font.size': self.font_size.get()})

        fig_predict = Figure(figsize=(self.size_x.get(), self.size_y.get()), dpi=100)
        self.canvas = FigureCanvasTkAgg(fig_predict, master=self.parent)
        self.canvas.draw()
        self.plot_widget_predict = self.canvas.get_tk_widget()
        self.plot_widget_predict.grid(row=0, column=2, columnspan=5, rowspan=16)

        ax2 = fig_predict.add_axes([self.size_x_space.get(), self.size_y_space.get(), self.size_x_length.get(), self.size_y_length.get()])
        
        ax2.scatter(
            exp_result, 
            pred_result, 
            edgecolor='k')
        ax2.plot([np.min(exp_result) - 100, np.max(exp_result) + 100], [np.min(exp_result) - 100, np.max(exp_result) + 100], ls="--", c=".3")
        
        ax2.set_xlabel('Experiments')
        ax2.set_ylabel('Prediction')
        ax2.set_xlim(np.min(exp_result) - 0.15 * np.abs(np.min(exp_result)), np.max(exp_result) * 1.15)
        ax2.set_ylim(np.min(pred_result) - 0.15 * np.abs(np.min(pred_result)), np.max(pred_result) * 1.15)

        self.toolbar_frame_predict = Frame(self.parent) 
        self.toolbar_frame_predict.grid(row=18,column=2,columnspan=4) 
        toolbar_predict = NavigationToolbar2Tk(self.canvas, self.toolbar_frame_predict)
        toolbar_predict.update()


    def fix_parameter_level(self):
        """
        If there are more than two parameters, other parameters need to be set to a fixed value
        """
        if self.initial_parameter_x_option.get() == self.initial_parameter_y_option.get():
            messagebox.showerror('Same parameter', 'The same parameter was chosen for the x- and y-axis. Please choose a different one for one of the axes.')
            return   

        self.FixParamLevel = Toplevel()
        self.FixParamLevel.configure(bg=self._from_rgb((11, 165, 193)))
        self.FixParamLevel.geometry("1000x700")
        #self.FixParamLevel.iconbitmap('icon_band.ico')
        self.FixParamLevel.grab_set()

        labels = self.para_labels
        real_indeces = np.arange(0, len(labels))

        for idx, l in enumerate(labels):
            if l == self.initial_parameter_x_option.get():
                if (real_indeces[0] == 1 and real_indeces[1] == 0 and idx == 1):
                    pass
                else:
                    real_indeces[0], real_indeces[idx] = real_indeces[idx], real_indeces[0]
   
            elif l == self.initial_parameter_y_option.get():
       
                real_indeces[1], real_indeces[idx] = real_indeces[idx], real_indeces[1]
            
        #Texts
        self.FixParam_input = Label(self.FixParamLevel, text='Input parameters to fixed the remaining axis (more than two variables)')
        self.FixParam_input.grid(row=0, column=0, columnspan=3, pady=(10, 5))
        self.FixParam_input['font'] = self.font_window
        self.FixParam_result_input = Label(self.FixParamLevel, text='Choose the maximum, minimum, or a desired predicted value')
        self.FixParam_result_input.grid(row=1, column=0, columnspan=3, pady=(10, 5))
        self.FixParam_result_input['font'] = self.font_window
        self.FixParam_item_input = Label(self.FixParamLevel, text='Choose the step(s) for the remaining variables')
        self.FixParam_item_input.grid(row=1, column=3, columnspan=3, pady=(10, 5))
        self.FixParam_item_input['font'] = self.font_window

        self.FixParam_desired_val_label = Label(self.FixParamLevel, text='Desired Value')
        self.FixParam_desired_val_label.grid(row=3, column=1, ipadx=20, pady=(10,5))

        #Entries
        self.spin_FixParam_box = list(); self.entry_label_FixParam = list(); self.spin_value = list()
        for nmb in range(2, len(self.para_min)):
            self.entry_label_FixParam.append(EntryItem(self.FixParamLevel, name=f'Axis {nmb+1}', row=1+nmb, column=4, width=16, pady=(10,5), state=DISABLED))
            self.entry_label_FixParam[-1].create_EntryItem(pady_label=(10,5), ipadx_label=14)
            self.entry_label_FixParam[-1].set_name(self.para_labels[real_indeces[nmb]])
            spin_value = self.para_min[real_indeces[nmb]] + self.para_steps[real_indeces[nmb]] * self.idx_max[real_indeces[nmb]]
            self.spin_value.append(StringVar()); self.spin_value[-1].set(spin_value)
            self.spin_FixParam_box.append(Spinbox(self.FixParamLevel, from_=self.para_min[real_indeces[nmb]], to=self.para_max[real_indeces[nmb]]-self.para_steps[real_indeces[nmb]], increment=self.para_steps[real_indeces[nmb]], textvariable=self.spin_value[-1], state=DISABLED))
            self.spin_FixParam_box[-1].grid(row=1+nmb, column=5, pady=(10,5))

        #Button
        self.close_FixParam_button = Button(self.FixParamLevel, text='Close', command=lambda:self.FixParamLevel.destroy())
        self.close_FixParam_button.grid(row=20, column=5, pady=10, ipadx=4)
        self.close_FixParam_button['font'] = self.font_window
        self.plot_FixParam_button = Button(self.FixParamLevel, text='Plot', command=lambda:self.plot_FixParam(real_indeces))
        self.plot_FixParam_button.grid(row=20, column=0, pady=10, ipadx=4)
        self.plot_FixParam_button['font'] = self.font_window
        self.change_FixParam_button = Button(self.FixParamLevel, text='Change', command=self.change_FixParam)
        self.change_FixParam_button.grid(row=2, column=5, pady=10, ipadx=4)
        self.change_FixParam_button['font'] = self.font_window
        self.module_fix = IntVar()
        self.fix_predict_radiobutton = Radiobutton(self.FixParamLevel, text='Predicted value', variable=self.module_fix, value=0, state=DISABLED)
        self.fix_predict_radiobutton.grid(row=2, column=0, pady=(10,5))
        self.fix_step_radiobutton = Radiobutton(self.FixParamLevel, text='Step(s)', variable=self.module_fix, value=1, state=DISABLED)
        self.fix_step_radiobutton.grid(row=2, column=3, pady=(10,5))
        self.expected_value_options = ["Maximum", "Minimum",  "Desired"]
        self.initial_expected_FixParam = StringVar(); self.initial_expected_FixParam.set(self.expected_value_options[0])
        self.expected_FixParam_menu = OptionMenu(self.FixParamLevel, self.initial_expected_FixParam, *self.expected_value_options)
        self.expected_FixParam_menu.grid(row=3, column=0, ipadx=5)
        if self.ML_program == 'Classification':    
            self.desired_value_options = np.unique(self.prediction / self.MLrun._scale_float2int)
            self.initial_desired_FixParam = StringVar(); self.initial_desired_FixParam.set(self.desired_value_options[0])
            self.desired_FixParam_menu = OptionMenu(self.FixParamLevel, self.initial_desired_FixParam, *self.desired_value_options)
            self.desired_FixParam_menu.grid(row=4, column=1, ipadx=25)
        
        else:
            self.desired_FixParam_entry = EntryItem(self.FixParamLevel, name='Desired value', row=4, column=1)
            self.desired_FixParam_entry.create_EntryItem(ipadx_label=15)


    def change_FixParam(self):
        """
        Change from predicted values to the steps
        """
        if self.module_fix.get() == 0:
            self.module_fix.set(1)
            for sb in self.spin_FixParam_box:
                sb.config(state=NORMAL)
            
            self.expected_FixParam_menu.config(state=DISABLED)
            if self.ML_program == 'Classification':
                self.desired_FixParam_menu.config(state=DISABLED)
            else:
                self.desired_FixParam_entry.config(state=DISABLED)
            
        else:
            self.module_fix.set(0)
            for sb in self.spin_FixParam_box:
                sb.config(state=DISABLED)

            self.expected_FixParam_menu.config(state=NORMAL)
            if self.ML_program == 'Classification':
                self.desired_FixParam_menu.config(state=NORMAL)
            else:
                self.desired_FixParam_entry.config(state=NORMAL)


    def plot_FixParam(self, real_indeces):
        """
        Replot the data with fixing the parameters

        Input:
        --------------
        real_indeces: ndarray, dtype: int
            Indexes if the parameters are changed
        """
        pred = np.swapaxes(self.prediction, 0, real_indeces[0])
        if real_indeces[0] == 1 and real_indeces[1] == 0:
            pred2 = pred                
        else:
            if real_indeces[1] == 0:
                pred2 = np.swapaxes(pred, 1, real_indeces[0])
            else:
                pred2 = np.swapaxes(pred, 1, real_indeces[1])
        
        if self.module_fix.get() == 0:
            if self.initial_expected_FixParam.get() == 'Maximum':
                idx_list = self.idx_max
            elif self.initial_expected_FixParam.get() == 'Minimum':
                idx_list = self.idx_min
            elif self.initial_expected_FixParam.get() == 'Desired':
      
                if self.ML_program == 'Classification':
                    val = float(self.initial_desired_FixParam.get()) * self.MLrun._scale_float2int
                    idx_list = np.argwhere(self.prediction == val)[0]
                
                else:
                    val = float(self.desired_FixParam_entry.get_name())
                    prediction = np.around(self.prediction, decimals=3)
                    idx_list = np.argwhere(prediction == val)
                    max_desired = np.max(prediction); min_desired = np.min(prediction)
                    if len(idx_list) == 0:
                        messagebox.showerror('No value', f'The desired value was not predicted. Choose a slight different value between {min_desired} and {max_desired}.')
                        return   
                    elif len(idx_list) > 1:
                        idx_list = idx_list[0]
    
        pred_new = pred2.T
        for x in range(len(self.para_min)-1, 1, -1):
            if self.module_fix.get() == 0:
                spin_value = self.para_min[real_indeces[x]] + self.para_steps[real_indeces[x]] * idx_list[real_indeces[x]]
                self.spin_value[x-2].set(spin_value)
                idx = int(idx_list[real_indeces[x]])
            else:
                val = float(self.spin_value[x-2].get())
                idx = round((val - self.para_min[real_indeces[x]]) / self.para_steps[real_indeces[x]])
            pred_new = pred_new[idx]
    

        self.xs = self.para_min[real_indeces[0]] + np.arange(0, self.MLrun.steps[real_indeces[0]] + 2) * self.para_steps[real_indeces[0]]
        self.ys = self.para_min[real_indeces[1]] + np.arange(0, self.MLrun.steps[real_indeces[1]] + 2) * self.para_steps[real_indeces[1]]
        self.MLrun.axis1 = real_indeces[0]; self.MLrun.axis2 = real_indeces[1]
        self.prediction2 = pred_new
        self._plot_ML_data()
        self.MLrun.axis1 = 0; self.MLrun.axis2 = 1


    def _create_matrix_prediction(self):
        """
        Create a matrix of predicted values for N dimensions 

        Output:
        -------------------
        prediction: ndarray(N, M)
            N and M matrix of predicted values
        """
        xm,	ym = np.meshgrid(self.xs, self.ys)
        render = np.c_[xm.flatten(), ym.flatten()]
               
        if len(self.para_min) == 2:
            self.prediction =  self.MLrun.pipe.predict(render).reshape(self.MLrun.steps[self.MLrun.axis1]+2, self.MLrun.steps[self.MLrun.axis2]+2)
        
        else:
            for x in range(2, len(self.para_min)):
                render = np.c_[render, np.zeros(len(render))+ self.para_min[x]]

            self.prediction = self._create_arr()
           
            for st3 in range(int(self.MLrun.steps[2])+2):
                if st3 == 0:
                    render = render
                
                else:
                    render2 = render.T
                    render2[2] = render2[2] + self.para_steps[2]
                    render = render2.T
                
                if len(self.para_min) == 3:
                    self.prediction[st3] = self.MLrun.pipe.predict(render).reshape(self.MLrun.steps[self.MLrun.axis2]+2, self.MLrun.steps[self.MLrun.axis1]+2)
                
                else:
                    for st4 in range(int(self.MLrun.steps[3])+2):
                        if st3 == 0 and st4 == 0:
                            render = render
                        elif st3 > 0 and st4 == 0:
                            render2 = render.T
                            render2[3] = render2[3] - (int(self.MLrun.steps[3])-1) * self.para_steps[3]
                            render = render2.T
                        else:
                            render2 = render.T
                            render2[3] = render2[3] + self.para_steps[3]
                            render = render2.T

                        if len(self.para_min) == 4:
                            self.prediction[st4][st3] = self.MLrun.pipe.predict(render).reshape(self.MLrun.steps[self.MLrun.axis2]+2, self.MLrun.steps[self.MLrun.axis1]+2)

                        else:
                            for st5 in range(int(self.MLrun.steps[4])+2):
                                if st3 == 0 and st4 == 0 and st5 == 0:
                                    render = render
                                elif st3 > 0 and st4 > 0 and st5 == 0:
                                    render2 = render.T
                                    render2[4] = render2[4] - (int(self.MLrun.steps[4])-1) * self.para_steps[4]
                                    render = render2.T
                                else:
                                    render2 = render.T
                                    render2[4] = render2[4] + self.para_steps[4]
                                    render = render2.T
                                    
                                if len(self.para_min) == 5:
                                    self.prediction[st5][st4][st3] = self.MLrun.pipe.predict(render).reshape(self.MLrun.steps[self.MLrun.axis2]+2, self.MLrun.steps[self.MLrun.axis1]+2)

                                else:
                                    for st6 in range(int(self.MLrun.steps[5])+2):
                                        if st3 == 0 and st4 == 0 and st5 == 0 and st6 == 0:
                                            render = render
                                        if st3 > 0 and st4 > 0 and st5 > 0 and st6 == 0:
                                            render2 = render.T
                                            render2[5] = render2[5] - (int(self.MLrun.steps[5])-1) * self.para_steps[5]
                                            render = render2.T
                                        else:
                                            render2 = render.T
                                            render2[5] = render2[5] + self.para_steps[5]
                                            render = render2.T
                                            
                                        if len(self.para_min) == 6:
                                            self.prediction[st6][st5][st4][st3] = self.MLrun.pipe.predict(render).reshape(self.MLrun.steps[self.MLrun.axis2]+2, self.MLrun.steps[self.MLrun.axis1]+2)

                                        else:
                                            for st7 in range(int(self.MLrun.steps[6])+2):
                                                if st3 == 0 and st4 == 0 and st5 == 0 and st6 == 0 and st7 == 0:
                                                    render = render
                                                elif st3 > 0 and st4 > 0 and st5 > 0 and st6 > 0 and st7 == 0:
                                                    render2 = render.T
                                                    render2[6] = render2[6] - (int(self.MLrun.steps[6])-1) * self.para_steps[6]
                                                    render = render2.T
                                                else:
                                                    render2 = render.T
                                                    render2[6] = render2[6] + self.para_steps[6]
                                                    render = render2.T
                                                    
                                                if len(self.para_min) == 7:
                                                    self.prediction[st7][st6][st5][st4][st3] = self.MLrun.pipe.predict(render).reshape(self.MLrun.steps[self.MLrun.axis2]+2, self.MLrun.steps[self.MLrun.axis1]+2)
                                                else:
                                                    for st8 in range(int(self.MLrun.steps[7])+2):
                                                        if st3 == 0 and st4 == 0 and st5 == 0 and st6 == 0 and st7 == 0 and st8 == 0:
                                                            render = render
                                                        elif st3 > 0 and st4 > 0 and st5 > 0 and st6 > 0 and st7 > 0 and st8 == 0:
                                                            render2 = render.T
                                                            render2[7] = render2[7] - (int(self.MLrun.steps[7])-1) * self.para_steps[7]
                                                            render = render2.T
                                                        else:
                                                            render2 = render.T
                                                            render2[7] = render2[7] + self.para_steps[7]
                                                            render = render2.T
                                                            
                                                        self.prediction[st8][st7][st6][st5][st4][st3] = self.MLrun.pipe.predict(render).reshape(self.MLrun.steps[self.MLrun.axis2]+2, self.MLrun.steps[self.MLrun.axis1]+2)
         
            self.prediction = self.prediction.T            


    def _create_arr(self):
        """
        Create a numpy array with a defined shape according to MLrun.steps

        Output:
        -------------------
        arr: numpy arr, dtype: float
            Array which has a defined number of dimensions
        """
        dim = list()
        for x in range(len(self.MLrun.steps)):
            dim.append(self.MLrun.steps[x]+2)

        return np.zeros(dim, dtype=float)


    def recursive_loop(self, render, dim, nmb, start=list(), st_val = 0): #does not work --> needs to be replaced with a nested class
   
        for st in range(st_val, int(self.MLrun.steps[nmb-1])):
            render2 = render.T
            render2[nmb-1] += self.para_steps[nmb-1]
            render = render2.T
            dim[nmb-3] = st
            
            if nmb == len(self.MLrun.steps):
                dimension = dim.T
                self.prediction[*dimension] = self.MLrun.pipe.predict(render).reshape(self.MLrun.steps[self.MLrun.axis2], self.MLrun.steps[self.MLrun.axis1])
                for x in range(3, len(self.para_min)):
                    #if start[2-x] != int(self.MLrun.steps[2-x]):
                        st_val = start[2-x]
                        self.recursive_loop(render, dim, x, start=start, st_val=st_val)
            else:
                start[nmb-3] = st + 1
                self.recursive_loop(render, dim, nmb + 1, start=start)                


    def _plot_slice(self, dim=[0, 1], replot=False):
        """
        Plot slice through the N-dimensional data

        Input:
        -------------------
        dim: list
            List of the dimensions used for the slice; default: [0, 1] meaning 0th and 1st dimension
        replot: Boolean
            True, if the data is reploted (avoiding long recalculation of the prediction matrix)
        """

        if replot:
            self.MLrun.axis1 = dim[0]; self.MLrun.axis2 = dim[1]
            self.xs = self.para_min[self.MLrun.axis1] + np.arange(0, self.MLrun.steps[self.MLrun.axis1] + 2) * self.para_steps[self.MLrun.axis1]
            self.ys = self.para_min[self.MLrun.axis2] + np.arange(0, self.MLrun.steps[self.MLrun.axis2] + 2) * self.para_steps[self.MLrun.axis2]
            
            pred = np.swapaxes(self.prediction, 0, dim[0])
            
            if len(self.para_min) > 2:
         
                idx_max = np.array(deepcopy(self.idx_max))
                if ((dim[0] == 1) and (dim[1] == 0)):
                    idx_max[0], idx_max[1] = self.idx_max[1], self.idx_max[0]

                else:
                    idx_max[0], idx_max[dim[0]] = self.idx_max[dim[0]], self.idx_max[0]
                    if dim[1] == 0:
                        idx_max[1], idx_max[dim[0]] = idx_max[dim[0]], idx_max[1]
                    else:
                        idx_max[1], idx_max[dim[1]] = idx_max[dim[1]], idx_max[1]
            
            if dim[0] == 1 and dim[1] == 0:
                pred2 = pred
            else:
                if dim[1] == 0:
                    pred2 = np.swapaxes(pred, 1, dim[0])
                else:
                    pred2 = np.swapaxes(pred, 1, dim[1])

            pred_new = pred2.T
            for x in range(2, len(self.para_min)):
                pred_new = pred_new[idx_max[x]]
            
            if len(self.para_min) == 2:
                self.prediction2 = pred_new.T
       
            elif len(self.para_min) > 2:
                self.prediction2 = pred_new

        else:
            self.xs = self.para_min[self.MLrun.axis1] + np.arange(0, self.MLrun.steps[self.MLrun.axis1] + 2) * self.para_steps[self.MLrun.axis1]
            self.ys = self.para_min[self.MLrun.axis2] + np.arange(0, self.MLrun.steps[self.MLrun.axis2] + 2) * self.para_steps[self.MLrun.axis2]

            self._create_matrix_prediction()
            
            if len(self.para_min) > 2:
                self.idx_max = np.unravel_index(np.argmax(self.prediction, axis=None), self.prediction.shape)
                self.idx_min = np.unravel_index(np.argmin(self.prediction, axis=None), self.prediction.shape)

                pred = self.prediction.T
                for x in range(2, len(self.para_min)):
                    pred = pred[self.idx_max[x]]
                
                self.prediction2 = pred
            
            else:
                self.prediction2 = self.prediction

        self._plot_ML_data()
        self.MLrun.axis1 = 0; self.MLrun.axis2 = 1


    def _plot_ML_data(self):
        """
        Plot predicted data
        """
        plt.rcParams["font.family"] = self.initial_font.get()
        plt.rcParams.update({'font.size': self.font_size.get()})
        plt.rcParams['contour.negative_linestyle'] = 'solid'
        self.MLrun.font_label_size = self.font_size.get()
        
        fig_ML = Figure(figsize=(self.size_x.get(), self.size_y.get()), dpi=100)
        self.canvas = FigureCanvasTkAgg(fig_ML, master=self.parent)
        self.canvas.draw()
        self.plot_widget_ML = self.canvas.get_tk_widget()
        self.plot_widget_ML.grid(row=0, column=8, columnspan=5, rowspan=16)
        ax = fig_ML.add_axes([self.size_x_space.get(), self.size_y_space.get(), self.size_x_length.get(), self.size_y_length.get()])
        cm = ax.pcolormesh(self.xs, self.ys, self.prediction2 / self.MLrun._scale_float2int, shading='auto', cmap='viridis')
        cs = ax.contour(self.xs, self.ys, self.prediction2 / self.MLrun._scale_float2int, origin='lower', extend='both', colors='k',
                linewidths=2)
        if self.MLrun.label_con:
            ax.clabel(cs, inline=5, fontsize=self.font_size.get())
        ax.set_xlabel(self.para_labels[self.MLrun.axis1], fontsize=self.MLrun.font_label_size)
        ax.set_ylabel(self.para_labels[self.MLrun.axis2], fontsize=self.MLrun.font_label_size)
        ax.scatter(self.MLrun.arr[self.MLrun.axis1], self.MLrun.arr[self.MLrun.axis2], marker='*', c='white', edgecolor='red', s=300)
        ax.set_xlim(self.para_min[self.MLrun.axis1], self.para_max[self.MLrun.axis1])
        ax.set_ylim(self.para_min[self.MLrun.axis2], self.para_max[self.MLrun.axis2])
        plt.colorbar(cm)	

        self.toolbar_frame_ML= Frame(self.parent) 
        self.toolbar_frame_ML.grid(row=18, column=8, columnspan=4) 
        toolbar_ML = NavigationToolbar2Tk(self.canvas, self.toolbar_frame_ML)
        toolbar_ML.update()

    
    def _from_rgb(self, rgb):
        """
        translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb


    def welcome(self):
        """
        Create a welcome window in the Help menu
        """
        welcome = Help()
        welcome.welcome()


    def documentary(self):
        """
        Create a documentary in the Help menu
        """

        documentary = Help()
        documentary.documentary()


    def about(self):
        """
        Create an about window in the Help menu
        """

        about = Help()
        about.screen_help.geometry('700x450')
        about.about()




if __name__ == "__main__":
    root = Tk()
    MainApplication(root)
    root.mainloop()
