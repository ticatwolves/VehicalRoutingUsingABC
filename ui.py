import Tkinter as tk
from Tkinter import *
from tkFileDialog import askopenfilename
from tkMessageBox import showerror

import matplotlib
#from abc import ABCVRP

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import pandas as pd

FONT = ('Verdana',12)
TITLE = ('Verdana',22)
ABSTRACT_FONT = ('Verdana',18)

import scipy as sp
import numpy as np
import bee
import localsearch as ls

import sklearn.metrics.pairwise as pairwise
import numpy as np
import time

bilol = []
title = "Welcome to the Capacitated Vehicle Routing Problem Application."
content = "Please select  Capacity, Iteration and Population and click  Browse  button for inputting the locations and demands.\n Click on Run button for computing and results."
abstract = """The Vehicle Routing Problem is the basic problem of distribution planning
which seeks to find the best route with minimum displacement cost
considering the number of customers, their constraints and number
of capacity of the available vehicles.\n
The software allows you to-\n
1. Add number of points on the map.\n
2. Set the number of vehicles( from ont to
maximum number of points on the map)\n
3.Save the graph.\n
4.Find the optimized path."""

class ABCGUI(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self, *args,**kwargs)
        try:
            tk.Tk.iconbitmap(self,default="favicon.ico")
        except:
            pass
        tk.Tk.wm_title(self,"CVRP")
        tk.Tk.wm_minsize(self,1000,400)
        tk.Tk.wm_maxsize(self,1001,641)
        #tk.Tk.wm_resizable(self,1500,800)
        container = tk.Frame(self,bg="#555555")
        container.pack(side="top",fill="both",expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        container.configure(background='black')

        self.menubar = Menu(self)
        menu_one = Menu(self.menubar, tearoff=0)
        menu_two = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu_one)
        self.menubar.add_cascade(label="Help", menu=menu_two)
        menu_one.add_command(label="Home",command=lambda:self.show_frame(ABCFrame))
        menu_one.add_command(label="Exit",command=quit)
        menu_two.add_command(label="About Project",command=lambda:self.show_frame(AboutABC))
        menu_two.add_command(label="About Developers",command=lambda:self.show_frame(AboutDevelopers))

        try:
            tk.Tk.config(self,menu=self.menubar)
        except AttributeError as p:
            print(str(p))
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            #tk.Tk.call(master, "config", "-menu", self.menubar)

        self.frames = {}
        for F in (AboutDevelopers,AboutABC,ABCFrame):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column = 0,sticky = "Nsew")
        self.show_frame(ABCFrame)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()    
"""
Anam Noori- anamnoori786@gmail.com
Sonali Verma- sonaliv398@gmail.com
Vidhi Agarwal- agarwalvidhi09@gmail.com
Vidushi Tandon- vidushitandon29@gmail.com
"""
names = ['Anam Noori','Sonali Verma','Vidhi Agarwal','Vidushi Tandon']
emails = ['anamnoori786@gmail.com','sonaliv398@gmail.com','agarwalvidhi09@gmail.com','vidushitandon29@gmail.com']

class AboutDevelopers(tk.Frame):
    def __init__(self,parent,control):
        tk.Frame.__init__(self,parent)
        Label(self, text="About Developers", font=TITLE,fg="blue").grid(row=0,column=0,columnspan=2,pady=10, padx=10)
        Label(self, text=names[0],font=("Helvetica", 32),fg="blue").grid(row=1,column=0)
        Label(self, text=emails[0],font=("Helvetica", 32),fg="blue").grid(row=1,column=1)
        Label(self, text=names[1],font=("Helvetica", 32),fg="blue").grid(row=2,column=0)
        Label(self, text=emails[1],font=("Helvetica", 32),fg="blue").grid(row=2,column=1)
        Label(self, text=names[2],font=("Helvetica", 32),fg="blue").grid(row=3,column=0)
        Label(self, text=emails[2],font=("Helvetica", 32),fg="blue").grid(row=3,column=1)
        Label(self, text=names[3],font=("Helvetica", 32),fg="blue").grid(row=4,column=0)
        Label(self, text=emails[3],font=("Helvetica", 32),fg="blue").grid(row=4,column=1)

class AboutABC(tk.Frame):
    def __init__(self, parent, control):
        tk.Frame.__init__(self, parent)
        Label(self, text="About ABC", font=TITLE,fg="blue").pack(pady=10, padx=10)
        label = Label(self, text=abstract, font=ABSTRACT_FONT,fg="blue").pack(pady=10, padx=10)        

class ABCFrame(tk.Frame):
    def __init__(self, parent, control):
        self.filename = None
        #self.con = control
        bc = tk.Frame.__init__(self, parent)

        Label(self, text="Run ABC",font=("Helvetica", 32),fg="blue").grid(row=0,pady=10,padx=10,columnspan=3)

        Label(self, text=title, font=FONT,fg="blue").grid(row=1,pady=10,padx=10,columnspan=3)
        self.con = Label(self, text=content, font=FONT,fg="blue")
        self.con.grid(row=2,pady=10,padx=10,columnspan=3)


        Label(self, text="Population", font=FONT,fg="blue").grid(row=3,column=0,pady=10,padx=10)
        Label(self, text="Capacity", font=FONT,fg="blue").grid(row=3,column=1,pady=10,padx=10)
        Label(self, text="Iteration", font=FONT,fg="blue").grid(row=3,column=2,pady=10,padx=10)
        
        self.population = Entry(self,font=FONT)
        self.population.grid(row=4,column=0,pady=10,padx=10)        

        self.capacity = Entry(self,font=FONT)
        self.capacity.grid(row=4,column=1,pady=10,padx=10)

        self.iteration = Entry(self,font=FONT)
        self.iteration.grid(row=4,column=2,pady=10,padx=10)

        Button(self, text="Browse", command=self.load_file, width=50, fg="blue").grid(row=5,columnspan=3,pady=10,padx=10)
        Button(self, text="Run", command=self.run_algo,width=50, fg="blue").grid(row=6,pady=10,padx=10,columnspan=3)
        #self.capacity.grid_forget()

    def run_algo(self):
        capacity = self.capacity.get()
        filename = self.filename
        iteration = self.iteration.get()
        population = self.population.get()
        if capacity and iteration and population and filename:
            #print("Do work")
            #abc = ABCVRP()
            self.vrp(int(population),int(capacity),int(iteration),filename)
        else:
            showerror("Error", "Please fill all the information")

    def load_file(self):
        fname = askopenfilename(filetypes=(("CSV FILES", "*.csv*"),("All files", "*.*")))
        if fname:
            try:
                self.filename = fname
                #print(str(fname))
            except Exception as e:
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
                showerror(e)
            return
    def vrp(self,population,capacity,iterations,filename):
	depot=[0]
	lamada=2
	nn=1
	headers = ["Sno","x","y","demand"]

        data = pd.read_csv(filename,names = headers)
        local_search="on"

        '''generate demandlist,citylist,citylist_tabu'''
        demandlist = data.iloc[:,3].values

        if (capacity < demandlist.min()+3):
            showerror("Capacity should be greater then minimun demand")
            return

	citylist=sp.linspace(0,len(demandlist)-1,len(demandlist))
        citylist_tabu=list(sp.copy(citylist))

	'''Generate cordinates'''
	length = len(data.iloc[:,0].values)
        cordinate = data.iloc[:,[1,2]].values

	'''Generate distance matrix'''
	reverse_distance_matrix,distance_matrix=self.Distance_Matrix(cordinate,length)
	'''Generate initial_fitness_matrix'''
	fitness_matrix=reverse_distance_matrix
	'''Solve VRP using ABC-Meta-Heuristic'''
	compare_result=9999999
	waggle_dance=0
	for iter in range(iterations):
	    '''run with multi replications to determine the iteration best result'''
	    result_iter,tour_set_iter=bee.iteration(compare_result,depot,length,demandlist,capacity,citylist,citylist_tabu,distance_matrix,fitness_matrix,population,nn)

	    if result_iter<compare_result:
		compare_result=result_iter
		compare_set=tour_set_iter
	    else:
		pass
	    print("iteration %i: "%iter,compare_result)

	    '''waggle_dance'''
	    for i in tour_set_iter:
		for count in range(len(tour_set_iter[i])-1):
		    fitness_matrix[tour_set_iter[i][count]][tour_set_iter[i][count+1]] *=lamada #updata delta_tao matrix
	    waggle_dance+=1
	    if waggle_dance>200:
		fitness_matrix=reverse_distance_matrix
		waggle_dance=0
	    else:
		pass
	'''3-opt local search improvement to the final result'''
	final_set = {}
	final_result = 0
	if local_search=="on":
	    for i in compare_set:
		compare_tour=compare_set[i]
		length=len(compare_tour)
		improve=ls.TwoOptSwap(compare_tour,i,distance_matrix)
		final_set[improve.result]=improve.tour
		final_result+=improve.result
	else:
	    pass

	print(final_result,"\n",final_set)
	'''plot'''
        self.plotgraph(final_set,cordinate,depot, "abc")

    def plotgraph(self,compare_set,cordinates,depot,filename):
        trucks = len(compare_set)
        print(trucks)
        print("I'll print graph")
        f = Figure(figsize=(10, 5), dpi=100)
	ax = f.add_subplot(111)
        for i in compare_set:
    	    tour = compare_set[i]
    	    x = []
    	    y = []
    	    for j in tour:
    	        x.append(cordinates[j][0])
    	        y.append(cordinates[j][1])
    	        ax.scatter(x, y)
    	        ax.plot(x, y)
                #time.sleep(1)
    	z = []
    	w = []
    	for i in depot:
            z.append(cordinates[i][0])
            w.append(cordinates[i][1])
    	#ax.title(filename)
    	ax.scatter(z, w, s = 0, c = "r", marker ="o", label = "Depot")
   	ax.legend()
        ax.grid()

        #self.emptygraph(filename)

        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.show()
        self.canvas._tkcanvas.grid(row=0,column=0,columnspan=3)#side=tk.TOP,fill=tk.BOTH,expand=True)
        self.canvas.get_tk_widget().grid(row=1,column=0,columnspan=3)#side=tk.TOP, fill=tk.BOTH, expand=1)
        """try:
            print("Error here")
            toolbar = NavigationToolbar2TkAgg(self.canvas,self)
            toolbar.update()
        except Exception as e:
            print(str(e))"""
        self.con.grid_forget()
        self.left = Button(self, text="Node Graph", command=self.nodesFrame, width=10, fg="blue")
        self.right = Button(self, text="Path Graph", command=self.showFrame, width=10, fg="blue")
        self.reset = Button(self, text="Reset", command=self.resetFrame, width=10, fg="blue")
        self.left.grid(row=2,column=0,pady=20)
        self.right.grid(row=2,column=1,pady=20)
        self.reset.grid(row=2,column=2,pady=20)

    def resetFrame(self):
        print("Erase it")
        self.canvas._tkcanvas.grid_forget()
        self.canvas.get_tk_widget().grid_forget()
        self.right.destroy()
        self.left.destroy()
        self.reset.destroy()
        self.con = Label(self, text=content, font=FONT,fg="blue")
        self.con.grid(row=2,pady=10,padx=10,columnspan=3)
        self.nodescanvas._tkcanvas.grid_forget()
        self.nodescanvas.get_tk_widget().grid_forget()

        #Label(self, text=content, font=FONT,fg="blue").grid(row=2,pady=10,padx=10,columnspan=3)
        #Button(self, text="Left", command=self.clearframe, width=50, fg="blue").grid(row=2).grid_forget()

    def nodesFrame(self):
        print("Erase it")
        self.left = Button(self, text="Node Graph", command=self.nodesFrame, width=10, fg="blue")
        self.right = Button(self, text="Path Graph", command=self.showFrame, width=10, fg="blue")
        self.reset = Button(self, text="Reset", command=self.resetFrame, width=10, fg="blue")
        self.left.grid(row=2,column=0)
        self.right.grid(row=2,column=1)
        self.reset.grid(row=2,column=2)
        self.canvas._tkcanvas.grid_forget()
        self.canvas.get_tk_widget().grid_forget()

        headers = ["Sno","x","y","demand"]
        filename = self.filename
        print(filename)
        data = pd.read_csv(filename,names = headers)
        X = data.iloc[:,1].values
        Y = data.iloc[:,2].values
        f = Figure(figsize=(10, 5), dpi=100)
	ax = f.add_subplot(111)
        ax.set_ylim([0,80])
        z = data.iloc[:,3].values
        mini = z.min()
        print("Minimun value should be = "+str(mini))
        ax.scatter(X,Y,s=80)
   	ax.legend()
        ax.grid()
        try:
            self.canvas._tkcanvas.grid_forget()
            self.canvas.get_tk_widget().grid_forget()
            self.nodescanvas._tkcanvas.grid_forget()
            self.nodescanvas.get_tk_widget().grid_forget()
        except:
            pass
        self.nodescanvas = FigureCanvasTkAgg(f, self)
        self.nodescanvas.show()
        self.nodescanvas._tkcanvas.grid(row=0,column=0,columnspan=3)#side=tk.TOP,fill=tk.BOTH,expand=True)
        self.nodescanvas.get_tk_widget().grid(row=1,column=0,columnspan=3)#side=tk.TOP, fill=tk.BOTH, expand=1)

    def showFrame(self):
        self.left = Button(self, text="Node Graph", command=self.nodesFrame, width=10, fg="blue")
        self.right = Button(self, text="Path Graph", command=self.showFrame, width=10, fg="blue")
        self.reset = Button(self, text="Reset", command=self.resetFrame, width=10, fg="blue")
        self.left.grid(row=2,column=0)
        self.right.grid(row=2,column=1)
        self.reset.grid(row=2,column=2)
        try:
            self.canvas._tkcanvas.grid_forget()
            self.canvas.get_tk_widget().grid_forget()
        except:
            pass
        try:
            self.nodescanvas._tkcanvas.grid_forget()
            self.nodescanvas.get_tk_widget().grid_forget()
        except:
            pass
        self.canvas.show()
        self.canvas._tkcanvas.grid(row=0,column=0,columnspan=3)#side=tk.TOP,fill=tk.BOTH,expand=True)
        self.canvas.get_tk_widget().grid(row=1,column=0,columnspan=3)#side=tk.TOP, fill=tk.BOTH, expand=1)


    '''Distance Matrix Generator'''
    def Distance_Matrix(self,cordinate,length):
        Matrix1=pairwise.pairwise_distances(cordinate, Y=None, metric='euclidean', n_jobs=1) #use to calculate Distance_Pheromone_Matrix. no round up in case 0 division occurs
        Matrix=np.around(Matrix1) #use to calculate the integer solution distance.
        for i in range(length):
            Matrix1[i][i]+=999999999
        Reverse_Matrix=(1/Matrix1)     #reverse distance
        Reverse_Matrix=np.array(Reverse_Matrix,float)
        return  Reverse_Matrix,Matrix



app = ABCGUI()
#app.configure(bg="blue") 
app.mainloop()

