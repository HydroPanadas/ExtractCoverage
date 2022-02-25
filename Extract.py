from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import subprocess as S

class Application(Frame):
    """ A GUI application that creates project folder structure """

    def __init__(self, master):
        """ Initialize the Frame """
        Frame.__init__(self, master)
        self.grid()
        self.app_widgets()


    def app_widgets(self):

        G1 = LabelFrame(self, foreground="blue")
        G1.grid(row=1, column=0, sticky=W)

        self.HOB = StringVar()
        self.HOB_f = Entry(G1, width=38, textvariable=self.HOB)
        self.HOB_text = Label(G1, text="Select Extracting Feature")
        self.HOB_text.grid(row=1, column=0, sticky=W)
        self.HOB_f.grid(row=1, column=1, sticky=W)
        self.Button1 = Button(G1, text="...", height=0,
                              command=self.Search_hob)
        self.Button1.grid(row=1, column=2, sticky=W, padx=2)

        self.CSAR = StringVar()
        self.CSAR_f = Entry(G1, width=38, textvariable=self.CSAR)
        self.CSAR_text = Label(G1, text="Select Surface to Extract")
        self.CSAR_text.grid(row=2, column=0, sticky=W)
        self.CSAR_f.grid(row=2, column=1, sticky=W)
        self.Button2 = Button(G1, text="...", height=0,
                              command=self.Search_csar)
        self.Button2.grid(row=2, column=2, sticky=W, padx=2)

##        self.Bands = ['Depth', 'Shoal', 'Source']
##        self.Lstbox = Listbox(G1, selectmode=MULTIPLE, width=10, height=5)
##        self.Lstbox.grid(row=4, column=1, columnspan=2, stick=W, padx=2)
##        for item in self.Bands:
##            self.Lstbox.insert(END, item)
##        self.band_text = Label(G1, text="Select Bands")
##        self.band_text.grid(row=4, column=0, sticky=N+W)

        self.out = StringVar()
        self.out1 = Entry(G1, width=38, textvariable=self.out)
        self.out_text = Label(G1, text="Output Folder")
        self.out_text.grid(row=3, column=0, sticky=W)
        self.out1.grid(row=3, column=1, sticky=W)
        self.Button3 = Button(G1, text="...", height=0,
                              command=self.Search_out)
        self.Button3.grid(row=3, column=2, sticky=W, padx=2)

        G2 = LabelFrame(self, foreground="blue")
        G2.grid(row=2, column=0, sticky=W)

        self.Button4 = Button(G2, text="Extract Coverage", width=35,
                              command=self.Extract_Coverage)
        self.Button4.grid(row=0, column=0, columnspan=2, sticky=W, padx=2)


    def Search_hob(self):
        
        self.Hob_f = filedialog.askopenfilename(initialdir = "/", title = "Select Feature file",
                                   filetypes = (("Hob Files","*.hob"),("all files","*.*")))
        self.HOB.set(self.Hob_f)

    def Search_csar(self):

        self.Csar_f = filedialog.askopenfilename(initialdir = "/", title = "Select Csar File",
                               filetypes = (("Surface","*.csar"),("all files","*.*")))
        self.CSAR.set(self.Csar_f)
        
         
    def Search_out(self):

        self.OutFolder = filedialog.askdirectory(initialdir = "/", title = "Select Output Directory")
        self.out.set(self.OutFolder)


    def Extract_Coverage(self):
##        selected_Bands = [self.Lstbox.get(i) for i in self.Lstbox.curselection()]
##        print (selected_Bands)
        print ('Process is Running')
        s = self.CSAR.get()
        Out = s.strip('.csar')
        
        CARIS = 'C:\Program Files\CARIS\\BASE Editor\\4.4\\bin'
        with open("Extract_Coverage.bat", "w") as bath:
            bath.write('@ECHO OFF' + '\n')
            bath.write('C:' +'\n')
            bath.write('cd '+ str(CARIS) + '\n')
            bath.write('carisbatch --run ExportToWKT --feature-catalogue "Bathy DataBASE" ' +
                   str(self.Hob_f) + ' '  + str(self.OutFolder) + '/' + 'Geo_Feature.wkt' + '\n')
            bath.write('carisbatch --run ExtractCoverage --include-band ALL --extract-type INCLUSIVE ' +
                       '--geometry-file ' + str(self.OutFolder) + '/' + 'Geo_Feature.wkt ' + str(self.Csar_f) + ' ' + Out + '_SUP.csar' + '\n')
            bath.write('carisbatch --run ExtractCoverage --include-band ALL --extract-type EXCLUSIVE ' +
                       '--geometry-file ' + str(self.OutFolder) + '/' + 'Geo_Feature.wkt ' + str(self.Csar_f) + ' ' + Out + '_BL.csar' + '\n')            
            bath.write('pause')

        p = S.Popen(['Extract_Coverage.bat'])
        p.communicate()
        
        print ('Process is Complete')

root = Tk()
root.title("CHS Extract Coverage Tool")
root.geometry("450x100")
menu = Menu(root)
root.config(menu=menu)
submenu = Menu(menu)
app = Application(root)
root.mainloop()
