import tkinter as tk
from tkinter import ttk
from tkinter import *
from aidfunction import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import  FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches


LARGE_FONT= ("Verdana", 16)
NORMAL_FONT= ("Verdana", 14)
SMALL_FONT = ("Verdana", 8)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text= msg, font=NORMAL_FONT)
    label.pack(side="top", fill= "x", pady= 10)
    button1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    button1.pack()
    popup.mainloop()


Start_List = [""]
plan = []
Gepland = dict()



def new_plan(apparaat,deadline):
    Start_List.append([apparaat,deadline])


dynamic_list_list = []
apparaten_list = []


class EnergyGridApp(tk.Tk):
    #*args = pass variables, **kwargs= key-word arguments = pass dictionaries
    def __init__(self, *args, **kwargs):
        #initieer tkinter
        tk.Tk.__init__(self, *args, **kwargs)

        #stijl
        tk.Tk.iconbitmap(self, default="Industry Solar panel icon.ico")
        tk.Tk.wm_title(self, "EnergyVille Smart Grid Monitor")
        tk.Tk.geometry(self, "1200x600")
        tk.Tk.configure(self, background="#b6cd32")
        #intitieer mainframe
        framecontainer = tk.Frame(self)
        framecontainer.place(x=10, y=10, width=1920 , height = 1080)
        framecontainer.grid_rowconfigure(0,weight=1)
        framecontainer.grid_columnconfigure(0, weight=1)

        #Menubar
        menubar = tk.Menu(self)

        ##filemenu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        ##hulpmenu
        helpmenu = tk.Menu(menubar, tearoff=1)
        helpmenu.add_command(label="Hoe apparaat instellen", command = lambda: popupmsg("In progress!"))
        menubar.add_cascade(label="Help", menu=helpmenu)


        tk.Tk.config(self, menu=menubar)


        #dictionary met alle tabbladen
        self.frames = {}

        for F in (StartPage, AppPlannen, AppBeheer, Graph):
            frame = F(parent=framecontainer, controller=self)

            self.frames[F] = frame

            frame.place(x=10, y=10, height=1040, width=1880)

        self.show_frame(StartPage)

    def show_frame(self, key):
        #tkraise (ingebouwde methode) brengt gekozen tabblad naar boven
        #key is tabblad dat naar boven wordt gebracht

        frame = self.frames[key]
        frame.tkraise()






class StartPage(tk.Frame):
    def __init__(self, parent, controller):

        font11 = "-family Verdana -size 30 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font9 = "-family Verdana -size 20 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        tk.Frame.__init__(self, parent)




        self.configure(borderwidth="2")
        self.configure(background="#ffffff")
        self.configure(width=555)

        self.Label1 = Label(self)
        self.Label1.place(relx=0.3, rely=0.09, height=150, width=900)
        self.Label1.configure(background="#ffffff")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font11)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Welkom op de Smart Grid Monitor''')
        self.Label1.configure(width=500)

        self.Button1 = Button(self)
        self.Button1.place(relx=0.2, rely=0.27, height=150, width=400)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#00ffff")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font9)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#00cccc")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(relief=RIDGE)
        self.Button1.configure(text='''Apparaten beheren''')
        self.Button1.configure(width=287)
        self.Button1.configure(overrelief="flat")
        self.Button1.configure(command= lambda : controller.show_frame(AppBeheer))


        self.Button2 = Button(self)
        self.Button2.place(relx=0.55, rely=0.27, height=150, width=400)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#00ffff")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font9)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#00cccc")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(relief=RIDGE)
        self.Button2.configure(text='''Grafiek''')
        self.Button2.configure(width=287)
        self.Button2.configure(overrelief="flat")
        self.Button2.configure(command = lambda : controller.show_frame(Graph))


        self.Button3 = Button(self)
        self.Button3.place(relx=0.2, rely=0.55, height=150, width=400)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#00ffff")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(font=font9)
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#00cccc")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(overrelief="flat")
        self.Button3.configure(pady="0")
        self.Button3.configure(relief=RIDGE)
        self.Button3.configure(text='''Apparaten plannen''')
        self.Button3.configure(width=287)
        self.Button3.configure(command=lambda: controller.show_frame(AppPlannen))

        self.Button4 = Button(self)
        self.Button4.place(relx=0.55, rely=0.55, height=150, width=400)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#00ffff")
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(font=font9)
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#00cccc")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(relief=RIDGE)
        self.Button4.configure(text='''Verbuiksstatistieken''')
        self.Button4.configure(width=287)
        self.Button4.configure(overrelief="flat")

class AppPlannen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        font11 = "-family Verdana -size 16 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font12 = "-family Verdana -size 15 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font13 = "-family Verdana -size 14 -weight bold -slant italic "  \
            "-underline 0 -overstrike 0"
        font14 = "-family Verdana -size 14 -weight normal -slant "  \
            "italic -underline 0 -overstrike 0"
        font15 = "-family Verdana -size 16 -weight normal -slant "  \
            "italic -underline 0 -overstrike 0"
        font16 = "-family Verdana -size 18 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font17 = "-family {Times New Roman} -size 15 -weight normal "  \
            "-slant italic -underline 0 -overstrike 0"
        font9 = "-family Verdana -size 20 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font20 = "-family Arial -size 13 -weight bold -slant roman " \
                 "-underline 0 -overstrike 0"

        self.plan_list = StringVar(value=plan)
        self.app_List = StringVar(value = Start_List)



        self.configure(borderwidth="2")
        self.configure(background="#ffffff")
        self.configure(highlightbackground="#ffffff")
        self.configure(highlightcolor="black")
        self.configure(width=125)

        self.Label1 = Label(self)
        self.Label1.place(relx=0.36, rely=0.04, height=71, width=500)
        self.Label1.configure(background="#ffffff")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font9)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Plannen van Apparaten''')
        self.Label1.configure(width=314)

        self.Label2 = Label(self)
        self.Label2.place(relx=0.03, rely=0.18, height=41, width=400)
        self.Label2.configure(background="#ffffff")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font11)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Huidig geplande apparaten''')
        self.Label2.configure(width=274)

        self.Label3 = Label(self)
        self.Label3.place(relx=0.01, rely=0.52, height=41, width=450)
        self.Label3.configure(background="#ffffff")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font13)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Welk apparaat zou u graag plannen?''')
        self.Label3.configure(width=324)

        self.Label4 = Label(self)
        self.Label4.place(relx=0.02, rely=0.61, height=31, width=450)
        self.Label4.configure(background="#ffffff")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(font=font13)
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''Deadline voor het apparaat?''')
        self.Label4.configure(width=274)

        self.Label5 = Label(self)
        self.Label5.place(relx=0.43, rely=0.61, height=70, width=74)
        self.Label5.configure(background="#ffffff")
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(font=font15)
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(text='''Uur''')
        self.Label5.configure(width=74)

        self.Label6 = Label(self)
        self.Label6.place(relx=0.55, rely=0.61, height=41, width=300)
        self.Label6.configure(background="#ffffff")
        self.Label6.configure(disabledforeground="#a3a3a3")
        self.Label6.configure(font=font15)
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(text='''Apparaat gepland!''')
        self.Label6.configure(width=184)

        self.Canvas1 = Canvas(self)
        self.Canvas1.place(relx=0.03, rely=0.48, relheight=0.02, relwidth=0.94)
        self.Canvas1.configure(background="#72ba5c")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief=RIDGE)
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")
        self.Canvas1.configure(width=1086)


        self.optionvar = StringVar()
        self.optionvar.set("")
        self.optionmenu = OptionMenu(self, self.optionvar, *Start_List)
        self.optionmenu.place(relx=0.34, rely=0.54, relheight=0.05, relwidth=0.14)
        self.optionmenu.configure(activebackground="#f9f9f9")
        self.optionmenu.configure(background="white")
        self.optionmenu.configure(disabledforeground="#a3a3a3")
        self.optionmenu.configure(font=font14)
        self.optionmenu.configure(foreground="black")
        self.optionmenu.configure(highlightbackground="black")
        self.optionmenu.configure(highlightcolor="black")
        self.optionmenu.configure(width=400)




        self.Button1 = Button(self)
        self.Button1.place(relx=0.32, rely=0.7, height=54, width=400)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#72ba5c")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font16)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(relief=GROOVE)
        self.Button1.configure(text='''Apparaat plannen''')
        self.Button1.configure(width=227)
        self.Button1.configure(command= lambda: self.new_planning())
        self.Button1.configure(overrelief="flat")

        self.Button2 = Button(self)
        self.Button2.place(relx=0.79, rely=0.88, height=44, width=400)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(overrelief="flat")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#72ba5c")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font12)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(relief=GROOVE)
        self.Button2.configure(text='''Terug naar hoofdmenu''')
        self.Button2.configure(width=217)
        self.Button2.configure(command=lambda: controller.show_frame(StartPage))

        self.Button3 = Button(self)
        self.Button3.place(relx=0.50, rely=0.54, height=40, width=160)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#72ba5c")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(font=font20)
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''Update menu''')
        self.Button3.configure(width=97)
        self.Button3.configure(command = lambda: self.refresh())
        self.Button3.configure(overrelief="flat")

        self.Entry1 = Entry(self)
        self.Entry1.place(relx=0.34, rely=0.61, relheight=0.05, relwidth=0.09)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font=font15)
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(width=104)

        self.Listbox1 = Listbox(self)
        self.Listbox1.place(relx=0.28, rely=0.18, relheight=0.27, relwidth=0.22)
        self.Listbox1.configure(background="white")
        self.Listbox1.configure(disabledforeground="#a3a3a3")
        self.Listbox1.configure(font=font17)
        self.Listbox1.configure(foreground="#000000")
        self.Listbox1.configure(width=254)




    def new_planning(self):
        app = self.optionvar.get()
        deadline = self.Entry1.get()

        if app not in Gepland and app is not None:
            self.Listbox1.insert(END, app + " met deadline om: " + deadline + "uur")
            for x in apparaten_list:
                if x[0] == app:
                    app_list = x
                    app_list.append(deadline)
                    #dynamic_list_list.append(app_list)
            Gepland[app]=deadline
            plan.append(app)

            print(dynamic_list_list)
            print("Gepland", Gepland)
        else:
            popupmsg("Apparaat al gepland!")

    def refresh(self):
        # Reset var and delete all old options
        self.optionvar.set('')
        self.optionmenu['menu'].delete(0, 'end')

        # Insert list of new options (tk._setit hooks them up to var)
        new_choices = Start_List
        for choice in new_choices:
            self.optionmenu['menu'].add_command(label=choice, command=tk._setit(self.optionvar, choice))


class AppBeheer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        font10 = "-family Verdana -size 16 -weight bold -slant roman " \
                 "-underline 0 -overstrike 0"
        font12 = "-family {Times New Roman} -size 16 -weight normal " \
                 "-slant italic -underline 0 -overstrike 0"
        font13 = "-family Verdana -size 24 -weight bold -slant roman " \
                 "-underline 0 -overstrike 0"
        font15 = "-family Verdana -size 15 -weight bold -slant roman " \
                 "-underline 0 -overstrike 0"
        font16 = "-family Verdana -size 15 -weight normal -slant roman" \
                 " -underline 0 -overstrike 0"
        font11 = "-family Verdana -size 15 -weight normal -slant roman" \
                 " -underline 0 -overstrike 0"

        self.current = None
        List = StringVar(value=Start_List)

        self.v= StringVar()
        self.v.set("")

        self.configure(borderwidth="2")
        self.configure(background="#ffffff")
        self.configure(highlightbackground="#ffffff")
        self.configure(highlightcolor="black")
        self.configure(width=125)

        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0.28, rely=0.48, relheight=0.31, relwidth=0.35)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#d1edc5")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=405)

        self.Label1 = Label(self)
        self.Label1.place(relx=0.39, rely=0.05, height=100, width=600)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#ffffff")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font13)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Huishoudtoestellen beheren''')

        self.Label2 = Label(self)
        self.Label2.place(relx=0.02, rely=0.16, height=51, width=350)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#ffffff")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Ingeschreven toestellen''')

        self.Label3 = Label(self)
        self.Label3.place(relx=0.41, rely=0.16, height=51, width=450)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#ffffff")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font10)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Huidig geplande toestellen''')

        self.Label4 = Label(self)
        self.Label4.place(relx=0.87, rely=0.18, height=51, width=400)
        self.Label4.configure(background="#ffffff")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(font=font16)
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(textvariable= self.v)
        self.Label4.configure(width=144)

        self.Label5 = Label(self.Frame1)
        self.Label5.place(relx=0.05, rely=0.11, height=31, width=180)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(activeforeground="black")
        self.Label5.configure(background="#d1edc5")
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(font=font11)
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(highlightbackground="#d9d9d9")
        self.Label5.configure(highlightcolor="black")
        self.Label5.configure(text='''Naam toestel?''')

        self.Label6 = Label(self.Frame1)
        self.Label6.place(relx=0.01, rely=0.34, height=31, width=350)
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(activeforeground="black")
        self.Label6.configure(background="#d1edc5")
        self.Label6.configure(disabledforeground="#a3a3a3")
        self.Label6.configure(font=font11)
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(highlightbackground="#d9d9d9")
        self.Label6.configure(highlightcolor="black")
        self.Label6.configure(text='''Vermogen toestel? (In Watt)''')

        self.Label7 = Label(self)
        self.Label7.place(relx=0.76, rely=0.18, height=51, width=150)
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(activeforeground="black")
        self.Label7.configure(background="#ffffff")
        self.Label7.configure(disabledforeground="#a3a3a3")
        self.Label7.configure(font=font12)
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(highlightbackground="#d9d9d9")
        self.Label7.configure(highlightcolor="black")
        self.Label7.configure(text='''Deadline op''')

        self.Label8 = Label(self.Frame1)
        self.Label8.place(relx=0.05, rely=0.57, height=31, width=250)
        self.Label8.configure(background="#d1edc5")
        self.Label8.configure(disabledforeground="#a3a3a3")
        self.Label8.configure(font=font11)
        self.Label8.configure(foreground="#000000")
        self.Label8.configure(text='''Duratie? (In minuten)''')
        self.Label8.configure(width=214)

        self.Entry1 = Entry(self.Frame1)
        self.Entry1.place(relx=0.44, rely=0.11, relheight=0.17, relwidth=0.4)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font=font11)
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(highlightbackground="#d9d9d9")
        self.Entry1.configure(highlightcolor="black")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(selectbackground="#c4c4c4")
        self.Entry1.configure(selectforeground="black")

        self.Entry2 = Entry(self.Frame1)
        self.Entry2.place(relx=0.64, rely=0.34, relheight=0.17, relwidth=0.21)
        self.Entry2.configure(background="white")
        self.Entry2.configure(disabledforeground="#a3a3a3")
        self.Entry2.configure(font=font11)
        self.Entry2.configure(foreground="#000000")
        self.Entry2.configure(highlightbackground="#d9d9d9")
        self.Entry2.configure(highlightcolor="black")
        self.Entry2.configure(insertbackground="black")
        self.Entry2.configure(selectbackground="#c4c4c4")
        self.Entry2.configure(selectforeground="black")

        self.Entry3 = Entry(self.Frame1)
        self.Entry3.place(relx=0.64, rely=0.57, relheight=0.17, relwidth=0.21)
        self.Entry3.configure(background="white")
        self.Entry3.configure(disabledforeground="#a3a3a3")
        self.Entry3.configure(font=font11)
        self.Entry3.configure(foreground="#000000")
        self.Entry3.configure(insertbackground="black")
        self.Entry3.configure(width=84)



        self.Button1 = Button(self)
        self.Button1.place(relx=0.03, rely=0.48, height=44, width=400)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#00c462")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font10)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(relief=GROOVE)
        self.Button1.configure(text='''Nieuw toestel instellen?''')
        self.Button1.configure(width=237)
        self.Button1.configure(overrelief="flat")

        self.Button2 = Button(self)
        self.Button2.place(relx=0.79, rely=0.84, height=44, width=350)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#00c462")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font15)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(relief=GROOVE)
        self.Button2.configure(text='''Terug naar menu''')
        self.Button2.configure(width=167)
        self.Button2.configure(command=lambda: controller.show_frame(StartPage))
        self.Button2.configure(overrelief="flat")


        self.Button3 = Button(self.Frame1)
        self.Button3.place(relx=0.35, rely=0.74, height=50, width=350)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#ffffff")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(font=font13)
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(relief=GROOVE)
        self.Button3.configure(text='''Toestel toevoegen''')
        self.Button3.configure(command = lambda: self.insert_item())
        self.Button3.configure(overrelief="flat")

        self.Listbox1 = Listbox(self)
        self.Listbox1.place(relx=0.66, rely=0.18, relheight=0.22, relwidth=0.09)
        self.Listbox1.configure(background="white")
        self.Listbox1.configure(disabledforeground="#a3a3a3")
        self.Listbox1.configure(font=font12)
        self.Listbox1.configure(foreground="#000000")
        self.Listbox1.configure(highlightbackground="#d9d9d9")
        self.Listbox1.configure(highlightcolor="black")
        self.Listbox1.configure(selectbackground="#c4c4c4")
        self.Listbox1.configure(selectforeground="black")
        self.Listbox1.configure(selectmode=EXTENDED)
        self.Listbox1.configure(width=104)




        self.Listbox2 = Listbox(self)
        self.Listbox2.place(relx=0.23, rely=0.18, relheight=0.22, relwidth=0.09)
        self.Listbox2.configure(background="white")
        self.Listbox2.configure(disabledforeground="#a3a3a3")
        self.Listbox2.configure(font=font12)
        self.Listbox2.configure(foreground="#000000")
        self.Listbox2.configure(selectbackground="#c2ec46")
        self.Listbox2.configure(width=104)
        self.Listbox2.configure(listvariable = List)

        self.poll()


    def insert_item(self):
        new_item = self.Entry1.get()
        duration =  self.Entry3.get()
        wattage = self.Entry2.get()
        i=0
        if new_item is None or len(new_item) ==0:
            return None
        else:
            if new_item in Start_List:
               return None
            else:
                Start_List.append(new_item)
                dynamic_list_list.append([new_item,duration,wattage])
                self.Listbox2.insert(END, new_item)

    def poll(self):
        now = self.Listbox1.curselection()
        if now!= self.current and now != ():
            self.list_has_changed(now)
            self.current = now
        for item in Gepland:
            list = self.Listbox1.get(0, END)
            if item not in list:
                self.Listbox1.insert(END, item)

        self.after(250, self.poll)

    def list_has_changed(self, selection):
            app = plan[selection[0]]
            print(app, Gepland)
            self.v.set(Gepland[app] + " uur")


class Graph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(borderwidth="2")
        self.configure(background="#ffffff")
        self.configure(highlightbackground="#ffffff")
        self.configure(highlightcolor="black")
        self.configure(width=125)

        font15 = "-family Verdana -size 15 -weight bold -slant roman " \
                 "-underline 0 -overstrike 0"


        self.Button2 = Button(self)
        self.Button2.place(relx=0.79, rely=0.84, height=44, width=350)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#00c462")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font15)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(relief=GROOVE)
        self.Button2.configure(text='''Terug naar menu''')
        self.Button2.configure(width=167)
        self.Button2.configure(command=lambda: controller.show_frame(StartPage))
        self.Button2.configure(overrelief="flat")

        self.Button1 = Button(self)
        self.Button1.place(relx=0.40, rely=0.05, height=44, width=350)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#00c462")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font15)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(relief=GROOVE)
        self.Button1.configure(text='''Load optimalisation''')
        self.Button1.configure(width=167)
        self.Button1.configure(command=lambda: self.display_graph())
        self.Button1.configure(overrelief="flat")



        #Grafiek maken
        #Subplot: 1 bij 1, voor plot 1 =111

        #Grafiek zichtbaar maken
        # f = Figure(figsize=(5,5), dpi=100)
        # a = f.add_subplot(111)
        # a.plot(lijst[0], lijst[1])
        # canvas =  FigureCanvasTkAgg(f, self)
        # canvas.show()
        # canvas.get_tk_widget().pack(side=tk.TOP, fill= tk.BOTH, expand = True)

        # #Toolbar
        # toolbar = NavigationToolbar2TkAgg(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill= tk.BOTH, expand = True)

    def display_graph(self):

        y= simulation("dag1","gem",3000, self.insert_devices())
        f = Figure(figsize=(5,5), dpi = 100)
        a = f.add_subplot(111)
        a.plot(y[1],"#183A54", label= "Optimalisatie")
        a.plot(y[2],"#FFD700", label = "Zonneproductie")
        a.legend()
        title = "Maximalisatie van zelfopgewekte zonne-energie"
        a.set_title(title)


        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().place(relx=0.03, rely=0.10, height=700, width=1300)

    def insert_devices(self):
        y=[]
        for x in dynamic_list_list:
             y.append(dynamic_device(x[0],int(x[1]),watt=int(x[2])))
        return y




app = EnergyGridApp()
app.geometry("1200x600")
#animatie
#ani = animation.FuncAnimation(f, animate, interval=10000)
app.mainloop()


