import sys
from DMCpy import DataFile, _tools, DataSet
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

try:
    import IPython
    shell = IPython.get_ipython()
    shell.enable_matplotlib(gui='qt')
except ImportError:
    pass


class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("DMCSpy")

        # Variables for storing input values
        self.scanNumbers_var = tk.StringVar()
        self.dataFolder_var = tk.StringVar()
        self.year_var = tk.StringVar()

        self.a = tk.StringVar()
        self.b = tk.StringVar()
        self.c = tk.StringVar()
        self.alpha = tk.StringVar()
        self.beta = tk.StringVar()
        self.gamma = tk.StringVar()

        self.Q1x = tk.StringVar()
        self.Q2x = tk.StringVar()
        self.Q1y = tk.StringVar()
        self.Q2y = tk.StringVar()
        self.Q1z = tk.StringVar()
        self.Q2z = tk.StringVar()

        self.H1 = tk.StringVar()
        self.H2 = tk.StringVar()
        self.K1 = tk.StringVar()
        self.K2 = tk.StringVar()
        self.L1 = tk.StringVar()
        self.L2 = tk.StringVar()

        self.hkl = tk.IntVar()

        # Create input widgets
        tk.Label(master, text="Scan Numbers:").grid(row=1, column=0)
        tk.Entry(master, textvariable=self.scanNumbers_var).grid(
            row=1, column=1)

        tk.Label(master, text="Data Folder:").grid(row=2, column=0)
        tk.Entry(master, textvariable=self.dataFolder_var).grid(
            row=2, column=1)
        tk.Button(master, text="Browse", command=self.browse_data_folder).grid(
            row=2, column=2)

        tk.Label(master, text="Year:").grid(row=3, column=0)
        tk.Entry(master, textvariable=self.year_var).grid(row=3, column=1)

        # Create buttons
        tk.Button(master, text="Initialise Data",
                  command=self.initialise_data).grid(
            row=5, column=0, columnspan=2, rowspan=2)
        tk.Button(master, text="Interactive Viewer",
                  command=self.plot_interactive_viewer).grid(
            row=5, column=2, columnspan=2, rowspan=2)

        tk.Button(master, text="Load Transform",
                  command=self.intialize_transformation).grid(
            row=8, column=0, columnspan=2, rowspan=2)

        tk.Button(master, text="3D Viewer",
                  command=self.plot_3D_viewer).grid(
            row=8, column=2, columnspan=2, rowspan=2)

        tk.Checkbutton(master, text='HKL On', variable=self.hkl,
                       onvalue=1, offvalue=0,
                       command=None).grid(row=10, column=2)

        tk.Label(master, text='Unit Cell').grid(row=0, column=6)
        tk.Label(master, text='a').grid(row=1, column=4)
        tk.Label(master, text='b').grid(row=2, column=4)
        tk.Label(master, text='c').grid(row=3, column=4)
        tk.Label(master, text=r'\alpha').grid(row=1, column=6)
        tk.Label(master, text=r'\beta').grid(row=2, column=6)
        tk.Label(master, text=r'\gamma').grid(row=3, column=6)

        tk.Entry(master, textvariable=self.a).grid(row=1, column=5)
        tk.Entry(master, textvariable=self.b).grid(row=2, column=5)
        tk.Entry(master, textvariable=self.c).grid(row=3, column=5)
        tk.Entry(master, textvariable=self.alpha).grid(row=1, column=7)
        tk.Entry(master, textvariable=self.beta).grid(row=2, column=7)
        tk.Entry(master, textvariable=self.gamma).grid(row=3, column=7)

        tk.Label(master, text='').grid(
            row=4, column=6)

        tk.Label(master, text='Coordinate Transformation').grid(
            row=5, column=6)
        tk.Label(master, text='Q1x').grid(row=6, column=5)
        tk.Label(master, text='Q1y').grid(row=6, column=6)
        tk.Label(master, text='Q1z').grid(row=6, column=7)

        tk.Entry(master, textvariable=self.Q1x).grid(row=7, column=5)
        tk.Entry(master, textvariable=self.Q1y).grid(row=7, column=6)
        tk.Entry(master, textvariable=self.Q1z).grid(row=7, column=7)

        tk.Label(master, text='Q2x').grid(row=8, column=5)
        tk.Label(master, text='Q2y').grid(row=8, column=6)
        tk.Label(master, text='Q2z').grid(row=8, column=7)

        tk.Entry(master, textvariable=self.Q2x).grid(row=9, column=5)
        tk.Entry(master, textvariable=self.Q2y).grid(row=9, column=6)
        tk.Entry(master, textvariable=self.Q2z).grid(row=9, column=7)

        tk.Label(master, text='H1').grid(row=10, column=5)
        tk.Label(master, text='K1').grid(row=10, column=6)
        tk.Label(master, text='L1').grid(row=10, column=7)

        tk.Entry(master, textvariable=self.Q2x).grid(row=11, column=5)
        tk.Entry(master, textvariable=self.Q2y).grid(row=11, column=6)
        tk.Entry(master, textvariable=self.Q2z).grid(row=11, column=7)

        tk.Label(master, text='H2').grid(row=12, column=5)
        tk.Label(master, text='K2').grid(row=12, column=6)
        tk.Label(master, text='L2').grid(row=12, column=7)

        tk.Entry(master, textvariable=self.Q2x).grid(row=13, column=5)
        tk.Entry(master, textvariable=self.Q2y).grid(row=13, column=6)
        tk.Entry(master, textvariable=self.Q2z).grid(row=13, column=7)

    def initialise_data(self):
        # Get input values from the GUI
        scanNumbers = self.scanNumbers_var.get()
        dataFolder = self.dataFolder_var.get()
        year = int(self.year_var.get())

        a = self.a.get()
        b = self.b.get()
        c = self.c.get()
        al = self.alpha.get()
        be = self.beta.get()
        ga = self.gamma.get()
        filePath = _tools.fileListGenerator(scanNumbers,
                                            dataFolder,
                                            year=year)

        if a == '':
            print('No Unit Cell Information, continuing generically')
            unitCell = np.array([1,
                                 1,
                                 1,
                                 1,
                                 1,
                                 1])
            self.unitcelled = False
        else:
            unitCell = np.array([
                                float(a),
                                float(b),
                                float(c),
                                float(al),
                                float(be),
                                float(ga)])
            self.unitcelled = True
            print('Unit Cell:', unitCell)

        dataFiles = [DataFile.loadDataFile(
            dFP, unitCell=unitCell) for dFP in filePath]
        self.ds = DataSet.DataSet(dataFiles)
        print('Initalised {} Datasets'.format(len(self.ds)))

    def browse_data_folder(self):
        folder_path = filedialog.askdirectory()
        self.dataFolder_var.set(folder_path)

    def plot_interactive_viewer(self):
        for i in range(len(self.ds)):
            print(i)
            IA = self.ds[i].InteractiveViewer()
            IA.set_clim(0, 2)
            IA.set_clim_zIntegrated(0, 100)
            plt.title(i)
            plt.show()

    def plot_3D_viewer(self):
        print(self.hkl)
        print('Binning the data... Be Patient (: ')
        Viewer = self.ds.Viewer3D(0.015, 0.015, 0.1, rlu=self.hkl,
                                  steps=151)
        Viewer.ax.axis('equal')
        Viewer.set_clim(0, 0.005)
        plt.show()

    def intialize_transformation(self):
        self.q1 = [float(self.Q1x), float(self.Q1x), float(self.Q1x)]
        self.q2 = [float(self.Q2x), float(self.Q2x), float(self.Q2x)]
        self.HKL1 = [float(self.H1), float(self.K1), float(self.L1)]
        self.HKL2 = [float(self.H2), float(self.K2), float(self.L2)]

        self.ds.alignToRefs(q1=self.q1, q2=self.q2,
                            HKL1=self.HKL1, HKL2=self.HKL2)

    def run_script(self):
        # Insert the rest of your script here

        width = 0.1
        points = np.array([[-0.0, 0.0, 0.0],
                           [-0.0, 0.0, 1.0],
                           [-0.0, 1.0, 0.0]])

        kwargs = {
            'dQx': 0.005,
            'dQy': 0.005,
            'steps': 151,
            'rlu': True,
            'rmcFile': True,
            'colorbar': True,
        }

        ax, returndata, bins = ds.plotQPlane(
            points=points, width=width, **kwargs)
        ax.set_clim(0, 0.0001)
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    gui = MyGUI(root)
    root.mainloop()
