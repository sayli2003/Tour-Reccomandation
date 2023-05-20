import pandas as pd
import mysql.connector
from . import user as user
from . import RecommendationSystem as rs
import csv

class DBConn:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sayli",
            database="Travel"
        )


    def insert_into_destination(self,DID,Name,City,State,Type,Description):
        mycursor = self.mydb.cursor()
        query = "INSERT INTO destination (DID,Name,City,State,Type,Description) VALUES (%s, %s, %s, %s, %s, %s)"
        values=(DID,Name,City,State,Type,Description)
        mycursor.execute(query,values)
        self.mydb.commit()
        mycursor.close()


    def user_recommendation(self):
        pack_list=rs.RecSystem(user.userdets["CID"])
        mycursor = self.mydb.cursor()
        result=[]
        for j in range(len(pack_list)):
            query = "Select * from Packages where PID = {}".format(pack_list[j])
            mycursor.execute(query)
            res=mycursor.fetchall()
            desc=[i[0] for i in mycursor.description]
            rec={}
            for i in range(len(desc)):
                rec[desc[i]]=res[0][i]
            result.append(rec)
        return result


    def insertCity_State(self):
        file=pd.read_csv("..\static\DataBase - City_State.csv")
        mycursor=self.mydb.cursor()
        for i in file.values:
            query="insert into City_State(City,State) values(%s,%s)"
            values=(i[0],i[1])
            mycursor.execute(query,values)
            print(i)
        self.mydb.commit()


    def insertSearchHistory(self):
        file=pd.read_csv("..\static\DataBase - SearchHistory.csv")
        mycursor=self.mydb.cursor()
        for i in file.values:
            query="insert into SearchHistory( SH_ID, CID, PID, Date, NumPsg, Bought, Rating) values('{}',{},{},STR_TO_DATE('{}', '%d/%m/%Y'),{},{},{});".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6])
            print(query)
            mycursor.execute(query)
        self.mydb.commit()


    def get_dest(self,state):
        mycursor = self.mydb.cursor()
        query = "Select * from destination where State = '{}' ".format(state)
        mycursor.execute(query)
        res = mycursor.fetchall()
        desc=[i[0] for i in mycursor.description]
        pack_list=[]
        for j in range(len(res)):
            rec={}
            for i in range(len(desc)):
                rec[desc[i]]=res[j][i]
            pack_list.append(rec)
        
        self.mydb.commit()
        mycursor.close()
        return pack_list

    def get_dest_searched(self,state,type=None):
        mycursor = self.mydb.cursor()
        query = "Select * from destination where State = '{}' and Type = '{}'".format(state,type)
        mycursor.execute(query)
        res = mycursor.fetchall()
        desc=[i[0] for i in mycursor.description]
        pack_list=[]
        for j in range(len(res)):
            rec={}
            for i in range(len(desc)):
                rec[desc[i]]=res[j][i]
            pack_list.append(rec)
        
        self.mydb.commit()
        mycursor.close()
        return pack_list


    def add_to_searched(self,PID,numpsg=0,Bought=0,rating=0):
        mycursor=self.mydb.cursor()
        mycursor.execute("select count(*) from SearchHistory")
        Shid="C"+str(mycursor.fetchone()[0]+101)
        query="insert into SearchHistory( SH_ID, CID, PID, Date, NumPsg, Bought, Rating) values('{}',{},{},CURDATE(),{},{},{});".format(Shid,user.userdets,PID,numpsg,Bought,rating)
        mycursor.execute(query)
        self.mydb.commit()

            
    def update_to_bought(self,PID):
        mycursor=self.mydb.cursor()
        mycursor.execute("select count(*) from SearchHistory")
        Shid="C"+str(mycursor.fetchone()[0]+101)
        query="update SearchHistory set Bought = 1 where PID={} and CID={}".format(PID,user.userdets["CID"])
        mycursor.execute(query)
        self.mydb.commit()


    def user_recommendation_rating_based(self):
        pack_list=rs.R_System(user.userdets["CID"])
        mycursor = self.mydb.cursor()
        result=[]
        for j in range(len(pack_list)):
            query = "Select * from Packages where PID = {}".format(pack_list[j])
            mycursor.execute(query)
            res=mycursor.fetchall()
            desc=[i[0] for i in mycursor.description]
            rec={}
            for i in range(len(desc)):
                rec[desc[i]]=res[0][i]
            result.append(rec)
        self.mydb.commit()
        return result

        


    def signupuser(self,name, phno, email, addr):
        mycursor = self.mydb.cursor()
        print("adding to database")
        query = "select count(*) from customers"
        mycursor.execute(query)
        result=mycursor.fetchone()
        desc=[i[0] for i in mycursor.description]
        CID=result[0]+1
        query = "INSERT INTO Customers (CID, CName,CAddr,PhNo,Email_ID) VALUES (%s,%s, %s, %s, %s)"
        values = (CID,name, addr, phno, email)
        mycursor.execute(query, values)
        self.mydb.commit()


    def getpackage(self,PackageId):
        mycursor=self.mydb.cursor()
        query = "Select * from Packages where PID = {}".format(PackageId)
        mycursor.execute(query)
        res=mycursor.fetchone()
        rec={}
        desc=[i[0] for i in mycursor.description]
        for i in range(len(desc)):
            rec[desc[i]]=res[i]
        return rec
        

    def get_searched(self,from_dest,to_dest):
        mycursor = self.mydb.cursor()
        query = "Select * from Packages where From_City like '%{}%' and Dest like '%{}%'".format(from_dest,to_dest)
        mycursor.execute(query)
        result=mycursor.fetchall()
        desc=[i[0] for i in mycursor.description]
        pack_list=[]
        for j in range(len(result)):
            rec={}
            for i in range(len(desc)):
                rec[desc[i]]=result[j][i]
            pack_list.append(rec)
        
        self.mydb.commit()
        mycursor.close()
        return pack_list


    def collect_all_destinations(self):
        mycursor = self.mydb.cursor()
        query = "Select * from Destination"
        mycursor.execute(query)
        result=mycursor.fetchall()
        for i in result:
            print(i)
        self.mydb.commit()
        mycursor.close()
    

    def get_close_packages(self):
        mycursor = self.mydb.cursor()
        li=user.userdets["CAddr"].split(",")
        query = "Select * from Packages where From_City like '%{}%'".format(li[len(li)-1].strip())
        mycursor.execute(query)
        result=mycursor.fetchall()
        desc=[i[0] for i in mycursor.description]
        pack_list=[]
        for j in range(len(result)):
            rec={}
            for i in range(len(desc)):
                rec[desc[i]]=result[j][i]
            pack_list.append(rec)
        
        self.mydb.commit()
        mycursor.close()
        return pack_list


    def get_customer_verification(self,name,pwd):
        mycursor = self.mydb.cursor()
        c="Select * from customers where CName='{}' and PhNo={}".format(name,pwd)
        mycursor.execute(c)
        t=tuple(mycursor.fetchall())
        
        if t!=():
            desc=[i[0] for i in mycursor.description]
            for i in range(len(desc)):
                user.userdets[desc[i]]=t[0][i]
            return True
        else:
            return False
        mycursor.close()
        self.mydb.commit()
    # def get_recommendations(self):


    def insert_packages(self):
        mycursor = self.mydb.cursor()
        file = pd.read_csv("../static\DataBase - Packages.csv")
        for i in file.values:
            query="update Packages set Season = '{}' where PID={}".format(i[5],i[0])
            mycursor.execute(query)
        # PID,From_City,From_State,Dest,NoOfDays,Season,Rating 
        self.mydb.commit()


    def get_user_Search_History(self):
        mycursor = self.mydb.cursor()
        query = "select SH_ID,CID, searchHistory.PID,From_City, Dest,NumPsg,Bought  from searchHistory inner join packages on packages.PID=searchHistory.PID where CID = {}".format(user.userdets["CID"])
        mycursor.execute(query)
        result=mycursor.fetchall()
        desc=[i[0] for i in mycursor.description]
        pack_list=[]
        for j in range(len(result)):
            rec={}
            for i in range(len(desc)):
                rec[desc[i]]=result[j][i]
            pack_list.append(rec)
        mycursor.close()
        return pack_list

    def gettransport(self, pkid):
        mycursor=self.mydb.cursor()
        query = "Select * from Transport where PID = {}".format(pkid)
        mycursor.execute(query)
        res=mycursor.fetchone()
        desc=[i[0] for i in mycursor.description]
        pack_list=[]
        rec={}
        for i in range(len(desc)):
            rec[desc[i]]=res[i]
        pack_list.append(rec)
        mycursor.close()
        return pack_list
    def get_hotels(self, state):
        mycursor=self.mydb.cursor()
        query = "Select * from Hotel inner join City_State on Hotel.City=City_State.City where City_State.State = '{}'".format(state)
        mycursor.execute(query)
        res=mycursor.fetchall()
        desc=[i[0] for i in mycursor.description]
        pack_list=[]
        for j in range(len(res)):
            rec={}
            for i in range(len(desc)):
                rec[desc[i]]=res[j][i]
            pack_list.append(rec)
        mycursor.close()
        return pack_list
    def Update_pack(self):
        mycursor = self.mydb.cursor()
        file = pd.read_csv("../static\DataBase - Packages.csv")
        for i in file.values:
            query="update Packages set Dest = '{}' where PID={}".format(i[3],i[0])
            mycursor.execute(query)
        # PID,From_City,From_State,Dest,NoOfDays,Season,Rating 
        self.mydb.commit()




# ob=DBConn()
# ob.collect_all_destinations()
# ob.insert_into_destination("D131","ABC","ABC","ABC","ABC","ABC")
# ob.collect_all_destinations()
# ob.collect_packages
# ob.get_close_packages()
# ob.insertSearchHistory()
# ob.insert_packages()
# ob.Update_pack()

# ob.add_to_searched(1002)

































  
    
    
    # def insert_hotels
    # def collect_packages(self):
    #     mycursor = self.mydb.cursor()
    #     file=pd.read_csv("DBMS Projects  - Customers.csv")
    #     for i in file.values:
    #         query = "INSERT INTO Customers (CID, CName, CAddr, PhNo, Email_ID) VALUES (%s, %s, %s, %s, %s)"
    #         values = (i[0],i[1],i[2],i[3],i[4])
    #         mycursor.execute(query, values)
    #         self.mydb.commit()
    #         print(i)
    # def get_cos(self):
    #     mycursor = self.mydb.cursor()
    #     query = "select * from Customers"
    #     mycursor.execute(query)

    #     try:
    #         result = mycursor.fetchall()
    #         for i in result:
    #             print(i)
    #     except mysql.connector.errors.InternalError as ie:
    #             pass
    #     mycursor.execute(query)
    #     self.mydb.commit()