import mysql.connector


class DBConn:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sayli",
            database="Travel"
        )


    def add_new_package(self,From_City,State,to_dest,Numdays,season,budget):
        cursor = self.mydb.cursor()
        cursor.execute("select PID from Packages order by PID desc limit 1")
        PID = cursor.fetchone()[0]+1
        cursor.execute("call addPack({},'{}','{}','{}',{},'{}',{})".format(PID,From_City,State,to_dest,Numdays,season,budget))
        result= cursor.fetchone()
        return result[0]

    

# ob=DBConn()