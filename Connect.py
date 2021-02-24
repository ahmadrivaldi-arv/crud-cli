import mysql.connector
from mysql.connector import errorcode
import argparse
import json
from tabulate import tabulate
from os import system







config_file = open("config.json")
conf = json.loads(config_file.read())
bulid = conf['build']
conf = conf['database-config']


db_username = conf['username']
db_password = conf['password']
db_host = conf['host']
db_auth_plugin = conf['auth_plugin']
db_name = conf['database']

try:
    mysql.connector.connect(
        host=db_host,
        user = db_username, 
        password = db_password,
        auth_plugin = db_auth_plugin)
except mysql.connector.errors.ProgrammingError as e: 
    print(e)   


class DB:

    """
    program crud berbasis CLI

    """
    def __init__(self,host=None,user=None,password=None,database=None,auth_plugin=None):
        self.host = host
        self.user = user
        self.password = password
        self.auth_plugin = auth_plugin
        self.db_name = database
        self.db = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            auth_plugin = self.auth_plugin,
            database = self.db_name)
        self.cursor = self.db.cursor()

        


    def status(self):
        """
        untuk cek koneksi ke database akan mengembalikan nilai True jika tehubung
        
        """
        try:
            if not self.db.is_connected():
                return "[INFO]: Gagal terhubung ke database"
            else:
                return "[INFO]: Berhasil terhubung ke database HOST: %s" % conf['host']
        except mysql.connector.errors.ProgrammingError as e:
            return e

    def create_DB(self,db_name):

        """
        membuat database baru

        @db_name: nama database baru

        """
        

        try:
            self.cursor.execute("CREATE DATABASE %s" % db_name)

            print("Database %s berhasil dibuat" % db_name)
        
        except mysql.connector.errors.DatabaseError as e:
            print(e)

    def drop_DB(self,db_name):

        """
        membuat database baru

        @db_name: nama database yang akan dihapus

        """

        try:

            self.cursor.execute("DROP DATABASE %s" % db_name)
            print("DATABASE %s berhasil dihapus" % db_name)

        except mysql.connector.errors.DatabaseError as e:
            print(e)

    def insert_data(self):

        """
        menambahkan data baru

        """
        name = input("enter name: ")
        while not name:
            system('clear')
            name = input("enter name: ")

        address = input("enter address: ")
        while not address:
            system('clear')
            address = input("enter address: ")

        phone_num = input("phone number: ")
        if phone_num == '':
            system('clear')
            phone_num = None

        val = (name,address,phone_num)
        sql = "INSERT INTO customers (name,address,phone_num) VALUES (%s,%s,%s)" 

        try:
            self.cursor.execute(sql,val)
            self.db.commit()
            print(f"{self.cursor.rowcount} data berhasil ditambahkan")

        except mysql.connector.errors.DatabaseError as e:
            print(e)
    
    def show_data(self):

        """
        menampilkan data

        """

        try:
            self.cursor.execute("SELECT * FROM customers")
            result  = self.cursor.fetchall()
            jsonObj = json.dumps(result)
            jsonArr = json.loads(jsonObj)


            if self.cursor.rowcount < 0:
                print("tidak ada data")
            else:
                query = [data for data in jsonArr]
                print(tabulate(query,["ID","NAME","ADDRESS","PHONE NUMBER"], tablefmt="fancy_grid"))                                 
        except mysql.connector.errors.DatabaseError as e:
            print(f"[INFO]: something went wrong {e}")

    def delete_data(self):

        """
        menghapus data

        """
        
        try:
            customers_id = input("enter customers id to delete: ")
            while not customers_id:
                system('clear')
                customers_id = input("enter customers id to delete: ")
            sql = "DELETE FROM customers WHERE customers_id=%s"
            val = (customers_id,)
            self.cursor.execute(sql,val)
            self.db.commit()
            print(f"[INFO]: {self.cursor.rowcount} data berhasil dihapus")
        except mysql.connector.errors.DatabaseError as e:
            print(f"[INFO]: something wrong {e}")
    def search_data(self):
        """
        
        method untuk mencari data berdasarkan name,address,atau customers_id

        """

        try:
            search_word = input("enter keyword: ")
            while not search_word:
                system('clear')
                search_word = input("enter keyword: ")

            sql = "SELECT * FROM customers WHERE name LIKE %s OR address LIKE %s OR phone_num LIKE %s OR customers_id LIKE %s"
            val = (search_word,search_word,search_word,search_word)

            self.cursor.execute(sql,val)
            result = self.cursor.fetchall()
            jsonObj = json.dumps(result)
            jsonArr = json.loads(jsonObj)

            if self.cursor.rowcount < 0:
                print("tidak ada data")
            else:
                query = [data for data in jsonArr]
                print(tabulate(query,["ID","NAME","ADDRESS","PHONE NUMBER"], tablefmt="fancy_grid"))                                 
        except mysql.connector.errors.DatabaseError as e:
                print(f"[INFO]: something wrong {e}")
    def update_data(self):
        
        """
        method update data
        
        """
        print("pass question to default value\n")
        customers_id = input("enter customers id: ")
        while not customers_id:
            system('clear')
            customers_id = input("enter customers id: ")

        try:

            name = input("enter new name: ")
            if name == '':
                try:
                    command = 'SELECT name FROM customers WHERE customers_id=%s'
                    value = (customers_id,)
                    self.cursor.execute(command,value)
                    result = self.cursor.fetchall()
                    for i in result:
                        for j in i:
                            name = j
                except Exception as e:
                    print(e)
            address = input("enter new address: ")
            if address == '':
                try:
                    command = 'SELECT address FROM customers WHERE customers_id=%s'
                    value = (customers_id,)
                    self.cursor.execute(command,value)
                    result = self.cursor.fetchall()
                    for i in result:
                        for j in i:
                            address = j
                except Exception as e:
                    print(e)   
            phone_num = input("enter new phone number: ")
            if phone_num == '':
                try:
                    command = 'SELECT phone_num FROM customers WHERE customers_id=%s'
                    value = (customers_id,)
                    self.cursor.execute(command,value)
                    result = self.cursor.fetchall()
                    for i in result:
                        for j in i:
                            phone_num = j
                except Exception as e:
                    print(e)   
            sql = "UPDATE customers SET name=%s, address=%s, phone_num=%s WHERE customers_id=%s"
            val = (name,address,phone_num,customers_id)
            self.cursor.execute(sql,val)
            self.db.commit()
            print(f"[INFO]: {self.cursor.rowcount} data updated")
        except mysql.connector.errors.DatabaseError as e:
            print(f"[INFO]: something wrong {e}")



if __name__ == '__main__':

        parser = argparse.ArgumentParser(description = "SIMPLE CONSOLE CRUD")
        parser.add_argument('-c','--create_db', help = "untuk membuat database baru")
        parser.add_argument('-d','--drop_db', help = "untuk menghapus(DROP) database")
        parser.add_argument('-s','--status', help = "tampilkan status koneksi ke database",action="store_true")
        parser.add_argument('-I','--insert', help= "insert data",action="store_true")
        parser.add_argument('-S','--show_data', help= "show data",action="store_true")
        parser.add_argument('-D','--delete_data', help= "delete data",action="store_true")
        parser.add_argument('-SD','--search_data', help="search data", action="store_true")
        parser.add_argument('-U','--update_data', help="update data", action="store_true")
        parser.add_argument('-v','--version',help="show version info", action="store_true")

        
        args = parser.parse_args()

        app = DB(db_host,db_username,db_password,db_name,db_auth_plugin)
        
        if args.create_db:
            app.create_DB(args.create_db)        
        if args.drop_db:
            app.drop_DB(args.drop_db)
        if args.status:
            print(app.status())
        if args.insert:
            app.insert_data()
        if args.show_data:
            app.show_data()
        if args.delete_data:
            app.show_data()
            app.delete_data()
        if args.search_data:
            app.search_data()
        if args.update_data:
            app.show_data()
            app.update_data()
        if args.version:
            print(bulid['version'])



        
