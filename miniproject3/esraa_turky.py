from tkinter import *

from PIL import ImageTk

from clusters import *
from tkinter import filedialog
import xlrd as xlrd

class Country:

    def __init__(self,name,total_cases,total_death,total_recovered,active_cases,serious_cases,total_cases_perM):
        self.name=name
        self.total_cases=total_cases
        self.total_death=total_death
        self.total_recovered=total_recovered
        self.active_cases=active_cases
        self.serious_cases=serious_cases
        self.total_cases_perM=total_cases_perM
        self.total_test=0
        self.positive_results=0
        self.test_perM=0
        self.positive_perK=0


    #add the test info to the object
    def add_test_info(self,total_test,positive_results,test_perM,positive_perK):
        self.total_test=total_test
        self.positive_results=positive_results
        self.test_perM=test_perM
        self.positive_perK=positive_perK

    #returen data of specific criteria
    def get_chooise(self,num="  "):
        self.choosies = {0: self.total_cases, 1: self.total_death, 2: self.total_recovered, 3: self.active_cases,
                         4: self.serious_cases, 5: self.total_cases_perM,6: self.total_test
            , 7: self.positive_results, 8: self.test_perM, 9: self.positive_perK}

        return self.choosies[num]
    #returen the numbers of the criterias
    def returnallcriteries(self):
        criteries=[0,1,2,3,4,5,6,7,8,9]
        return criteries
    #returen the list of criterias names
    def returnallcriteriesnames(self):
        names=['total_cases','total_death', 'total_recovered','active_cases',
                         'serious_cases', 'total_cases_perM', 'total_test'
            ,  'positive_results', ' test_perM',  'positive_perK']
        return names
class Data:
    def __init__(self):
        self.countries={}
    #insert new country
    def insertcountry(self, name, total_cases, total_death, total_recovered, active_cases, serious_cases, total_cases_perM):
        self.countries[name]=Country(name,total_cases,total_death,total_recovered,active_cases,serious_cases,total_cases_perM)
    #inseart the test info
    def add_test_info_data(self,name,total_test,positive_results,test_perM,positive_perK):
        for i in self.countries.values():
            if name == i.name:
                self.countries[name].add_test_info(total_test,positive_results,test_perM,positive_perK)


class GUI(Frame,Scrollbar):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        #Scrollbar.__init__(self,parent)
        self.data=Data()
        self.titlebar()
        self.clustring()
        self.add_info()
        self.control()
        self.info=[]
        self.pack()
    #creat title bar
    def titlebar(self):
        frame0 = Frame(self, borderwidth=0, height=10, width=500,highlightbackground="dark gray")
        frame0.pack(expand=TRUE, fill=BOTH)
        Label(frame0, text="Coronavirus Data Analysis Tool ", bg="red", width=500, font=8,
              fg="white").pack(expand=TRUE,fill=BOTH, padx=5, pady=5)
    #show the clustring results
    def clustring(self):
        self.frame1=Frame(self,highlightthickness=0.5,width=600,height=300,highlightbackground="dark gray")
        self.frame1.pack(expand=TRUE,fill=BOTH,padx=5,pady=5)
        self.scrollbar1 = Scrollbar(self.frame1)
        self.scrollbar1.pack(side=RIGHT, fill=Y)
        self.scrollbar2 = Scrollbar(self.frame1,orient='horizontal',highlightbackground="dark gray")
        self.scrollbar2.pack(side=BOTTOM, fill=X)
        self.canvas = Canvas(self.frame1, width=600, height=300,yscrollcommand=self.scrollbar1.set,xscrollcommand =self.scrollbar2.set,highlightbackground="dark gray")
        self.canvas.pack(expand=TRUE,fill=BOTH)
        self.scrollbar1.config(command=self.canvas.yview)
        self.scrollbar2.config(command=self.canvas.xview)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    #add files to the app
    def add_info(self):
        self.frame2=Frame(self,borderwidth=0, height=10, width=100)
        self.frame2.pack(expand=TRUE, fill="none",side=TOP)
        #add the excel sheet of countries
        add_country=Button(self.frame2,text="Upload Country Data",command=self.get_country_info,highlightbackground="dark gray")
        add_country.grid(column=0,row=0,padx=5,pady=5)
        #add the excel sheet of test info
        add_test_info = Button(self.frame2, text="Upload Test Statistics",command=self.iffree,highlightbackground="dark gray")
        add_test_info.grid(column=1,row=0,pady=5)
    #control the clustering process
    def control(self):
        farme3=Frame(self,height=300,width=700)
        farme3.pack(expand=TRUE,fill="none")
        #frame of sort buttons
        sub_frame1=Frame(farme3,highlightthickness=0.5,width=200,height=300,highlightbackground="dark gray")
        sub_frame1.pack(fill='x',expand=TRUE ,pady=5,side='left')
        lable1=Label(sub_frame1,text="Sort Countries")
        lable1.grid(column=0,row=0,padx=5,pady=5)
        sort1=Button(sub_frame1,text='Sort By Name',command=lambda: self.sort(1),highlightbackground="dark gray")
        sort1.grid(column=0,row=1,padx=5,pady=5)
        sort2 = Button(sub_frame1, text='Sort By Total Cases', command=lambda: self.sort(2),highlightbackground="dark gray")
        sort2.grid(column=0, row=2, padx=5, pady=5)
        ##########
        #list of countries and criterias
        title1=Label(farme3,text="Countries:").pack(expand=TRUE,fill='x', padx=5, pady=5,side='left')
        sub_frame0=Frame(farme3,highlightthickness=0.5,width=200,height=300,highlightbackground="dark gray")
        sub_frame0.pack(fill='x', expand=TRUE, pady=5, side='left', padx=5)
        scrollbar1 = Scrollbar(sub_frame0,highlightbackground="dark gray")
        scrollbar1.pack(side=RIGHT, fill=Y)
        self.listofcountries=Listbox(sub_frame0,width=40,height=300,yscrollcommand=scrollbar1.set,selectmode='multiple',exportselection=0,highlightbackground="dark gray")
        self.listofcountries.pack(expand=TRUE,fill='x', padx=5, pady=5,side='left')
        scrollbar1.config( command =self.listofcountries.yview)
        title2=Label(farme3,text="Criterias:").pack(expand=TRUE,fill='x', padx=5, pady=5,side='left')
        sub_frame00 = Frame(farme3, highlightthickness=0.5, width=200, height=300,highlightbackground="dark gray")
        sub_frame00.pack(fill='x', expand=TRUE, pady=5, side='left', padx=5)
        scrollbar2 = Scrollbar(sub_frame00)
        scrollbar2.pack(side=RIGHT, fill=Y)
        self.listofcriteries=Listbox(sub_frame00,width=40,height=300,highlightbackground="dark gray",selectmode='multiple',exportselection=0,yscrollcommand=scrollbar2.set)
        self.listofcriteries.pack(expand=TRUE,fill='x', padx=5, pady=5,side='left')
        scrollbar2.config(command=self.listofcriteries.yview)
       #frame of the clustering buttons
        sub_frame2=Frame(farme3,highlightthickness=0.5,width=200,height=300,highlightbackground="dark gray")
        sub_frame2.pack(fill='x',expand=TRUE ,pady=5,side='left',padx=5)
        lable2 = Label(sub_frame2, text="Clustering")
        lable2.grid(column=0, row=0, padx=5, pady=5)
        sort1 = Button(sub_frame2, text='Clustering By Countries', command=self.clustring_by_countries,highlightbackground="dark gray")
        sort1.grid(column=0, row=1, padx=5, pady=5)
        sort2 = Button(sub_frame2, text='Clustering By Criterias',command= self.clustring_by_cariteras,highlightbackground="dark gray")
        sort2.grid(column=0, row=2, padx=5, pady=5)
    #check if the file of the countries uplouded before the test file
    def iffree(self):
        if len(self.data.countries)==0:
            label=Label(self.frame2, text="please enter the countries file first!  ",
                               bg="Red")
            label.grid(column=2, row=0, pady=5)
            label.after(3000, lambda: label.destroy())
        else:
            self.get_test_info()
    #check if the cell is empty
    def ifempty(self,number):
        if number=='':
            return 0
        else:
            return number
    # add the list of the countries to the list box
    def updatelist(self, list):
        self.listofcountries.delete(0,'end')
        for i, y in list:
            self.listofcountries.insert('end', i + ' ' + str(y))
    # get the information from the countries excel sheet and save it as country object
    def get_country_info(self):
        filename=filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("exel files","*.xlsx"),("all files","*.*")))
        f = xlrd.open_workbook(filename)
        sheet = f.sheet_by_index(0)
        self.names=list(tuple())
        #get every country informations and add it as object of country class
        for i in range(2,sheet.nrows-1):
            self.data.insertcountry(sheet.cell_value(i, 0).strip(), self.ifempty(sheet.cell_value(i, 1)), self.ifempty(sheet.cell_value(i, 2)),
                                        self.ifempty(sheet.cell_value(i,3)),
                                        self.ifempty(sheet.cell_value(i,4)), self.ifempty(sheet.cell_value(i,5)), self.ifempty(sheet.cell_value(i,6)))
            self.names.append((sheet.cell_value(i, 0).strip(),self.ifempty( sheet.cell_value(i,1))))
        #update the listbox of countries
        self.updatelist(self.names)
        #update the craitera listbox
        for i in range(1,sheet.ncols):
            self.listofcriteries.insert('end',sheet.cell_value(0,i))

    # get the test info from excel sheet and save it in the country object with the same name
    def get_test_info(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("exel files", "*.xlsx"), ("all files", "*.*")))
        f = xlrd.open_workbook(filename)
        sheet = f.sheet_by_index(0)
        #read the test info and add it to the same object of the country
        for i in range(1, sheet.nrows):
            self.data.add_test_info_data(sheet.cell_value(i, 0).strip(), self.ifempty(sheet.cell_value(i, 1)),self.ifempty( sheet.cell_value(i, 2)),
                                         self.ifempty( sheet.cell_value(i, 4)), self.ifempty(sheet.cell_value(i, 5)))

        # update the craitera list
        for i in range(1, sheet.ncols):
            # ignore 'as of column'
            if i == 3:
                pass
            else:
                self.listofcriteries.insert('end', sheet.cell_value(0, i))
    #sort the list of countries
    def sort(self,num):
        #sort by names
        if num==1:
            sort = sorted(self.names, key=lambda tup: tup[0])
            self.updatelist(sort)
        #sort by number of cases
        elif num==2:
            sort = sorted(self.names, key=lambda tup: tup[1],reverse=True)
            self.updatelist(sort)

    #returen lists of the selected countries and creiterias
    def get_list_of_clustring(self):
        save = [self.listofcountries.get(i).split(" ") for i in self.listofcountries.curselection()]
        clustring_country_list=[i[0] for i in save ]
        clustring_criteria_list = [i for i in self.listofcriteries.curselection()]
        criteria_names=[self.listofcriteries.get(i) for i in self.listofcriteries.curselection()]
        return clustring_country_list,clustring_criteria_list,criteria_names
    #clustring by countries
    def clustring_by_countries(self):
        #clustring if the user choose the criterias and the countries they want to clustring depend on it
        if  self.listofcountries.curselection()and self.listofcriteries.curselection():
            country,criteria,criterianame=self.get_list_of_clustring()
            self.info.clear()
            #matrix of the data will cluster
            self.info=[[self.data.countries[i].get_chooise(j) for j in criteria] for i in country if i in self.data.countries.keys()]
            cluster = hcluster(self.info,sim_distance)
            drawdendrogram(cluster, country, 'cl.jpg')
            #update the photo of clustering
            img = ImageTk.PhotoImage(Image.open("cl.jpg"))
            self.canvas.create_image(20, 20, anchor=NW, image=img)
            self.canvas.image = img
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        #clustering by all countries and criterias if the user doesn't choose any of them
        elif not self.listofcriteries.curselection() and not self.listofcountries.curselection():
            self.info.clear()
            # matrix of the data will cluster
            self.info=[[i.get_chooise(j) for j in i.returnallcriteries()]for i in self.data.countries.values()]
            clust = hcluster(self.info, sim_distance)
            drawdendrogram(clust, [i for i in self.data.countries.keys()], 'cl.jpg')
            # update the photo of clustering
            img = ImageTk.PhotoImage(Image.open("cl.jpg"))
            self.canvas.create_image(20, 20, anchor=NW, image=img)
            self.canvas.image = img
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            #clustring by all countries with selected criterias
        elif not self.listofcountries.curselection():
            country, criteria,criterianame = self.get_list_of_clustring()
            self.info.clear()
            # matrix of the data will cluster
            self.info=[[i.get_chooise(j)for j in criteria]for i in self.data.countries.values()]
            clust=hcluster(self.info,sim_distance)
            drawdendrogram(clust, [i for i in self.data.countries.keys()], 'cl.jpg')
            # update the photo of clustering
            img = ImageTk.PhotoImage(Image.open("cl.jpg"))
            self.canvas.create_image(20, 20, anchor=NW, image=img)
            self.canvas.image = img
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        #clustering by all criterias with choosen countries
        elif not self.listofcriteries.curselection():
             country, criteria,criterianame = self.get_list_of_clustring()
             # matrix of the data will cluster
             self.info= [[self.data.countries[i].get_chooise(j) for j in self.data.countries[i].returnallcriteries()]for i in country]
             cluster = hcluster(self.info,sim_distance)
             drawdendrogram(cluster, country, 'cl.jpg')
             # update the photo of clustering
             img = ImageTk.PhotoImage(Image.open("cl.jpg"))
             self.canvas.create_image(20, 20, anchor=NW, image=img)
             self.canvas.image = img
             self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    #clustering by criterias
    def clustring_by_cariteras(self):
       #clustring if the user choose the criterias and the countries they want to clustring depend on it
        if  self.listofcountries.curselection() and self.listofcriteries.curselection():
            country, criteria,criterianame = self.get_list_of_clustring()
            self.info.clear()
            # matrix of the data will cluster
            self.info=[[self.data.countries[j].get_chooise(i) for j in country]for i in criteria]
            cluste = hcluster(self.info,sim_distance)
            drawdendrogram(cluste,criterianame, 'cl.jpg')
            # update the photo of clustering
            img = ImageTk.PhotoImage(Image.open("cl.jpg"))
            self.canvas.create_image(20, 20, anchor=NW, image=img)
            self.canvas.image = img
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # clustering by all countries and criterias if the user doesn't choose any of them
        elif not self.listofcriteries.curselection() and not self.listofcountries.curselection():
            self.info.clear()
            # matrix of the data will cluster
            self.info=[[j.get_chooise(i)for j in self.data.countries.values()]for i in self.data.countries['Egypt'].returnallcriteries()]
            cluser = hcluster(self.info, sim_distance)
            drawdendrogram(cluser,self.data.countries['Egypt'].returnallcriteriesnames() , 'cl.jpg')
            # update the photo of clustering
            img = ImageTk.PhotoImage(Image.open("cl.jpg"))
            self.canvas.create_image(20, 20, anchor=NW, image=img)
            self.canvas.image = img
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # clustring by all countries with selected criterias
        elif not self.listofcountries.curselection():
            country, criteria,criterianame = self.get_list_of_clustring()
            self.info.clear()
            # matrix of the data will cluster
            self.info=[[i.get_chooise(j) for i in self.data.countries.values()] for j in criteria]
            cluser = hcluster(self.info,sim_distance)
            drawdendrogram(cluser,criterianame, 'cl.jpg')
            # update the photo of clustering
            img = ImageTk.PhotoImage(Image.open("cl.jpg"))
            self.canvas.create_image(20, 20, anchor=NW, image=img)
            self.canvas.image = img
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # clustering by all criterias with choosen countries
        elif not self.listofcriteries.curselection():
            country, criteria, criterianame = self.get_list_of_clustring()
            self.info.clear()
            # matrix of the data will cluster
            self.info = [[self.data.countries[j].get_chooise(i) for j in country]for i in self.data.countries['Egypt'].returnallcriteries()]
            cluser = hcluster(self.info,sim_distance)
            drawdendrogram(cluser,self.data.countries['Egypt'].returnallcriteriesnames(), 'cl.jpg')
            # update the photo of clustering
            img = ImageTk.PhotoImage(Image.open("cl.jpg"))
            self.canvas.create_image(20, 20, anchor=NW, image=img)
            self.canvas.image = img
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

def main():
    root=Tk()
    root.title("Coronavirus Analysis Tool")
    root.configure()
    root.geometry("1100x600+300+100")
    app=GUI(root)
    root.mainloop()
main()