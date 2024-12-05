import mysql.connector
import json

class EMSAPP:
    def addAdmin():
    def addUser():

    def getUserInfo(username,password):
    def getAdminInfo(username,password):
    
    def updateUserData(username,password):
    def updateAdminData(username,password):
    
    def view_dashboard():



# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Query example
cursor.execute("SELECT * FROM products")
print(cursor.fetchall())

cursor.close()
conn.close()





    