import mysql.connector
import json
from datetime import datetime

# # Load configuration
with open('../config.json', 'r') as config_file:
    config = json.load(config_file)

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

class EMSVendor:
    def addVendor(self, details):
        try:
            query = """
            INSERT INTO vendor (name, company_name, email, phone_number, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, details)
            conn.commit()
            print("\nVendor registered successfully!")
        except mysql.connector.Error as err:
            print(f"\nError: {err}")
            
    def getVendorInfo(self,email,password):
        try:
            query = "SELECT * FROM vendor WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()

            if user:
                print("\nVendor found! Welcome back.")
                print("Vendor Details: ", user)
            else:
                print("\nNo vendor found with the provided email and password.")
        
        except mysql.connector.Error as err:
            print(f"\nError: {err}")

app = EMSVendor()
print("Welcome to SK Store - Vendor Page")
print("\nEnter 1 to Login in to the System")
print("Enter 2 to Register")

print("\nEnter your choice : ", end = " ")
choice = int(input())

if (choice == 1):
    print("\nEnter your email : ", end = " ")
    email = input()

    print("Enter the password : ", end = " ")
    password = input()

    app.getVendorInfo(email,password)

elif (choice == 2):
    details = []

    print("\nEnter your name  : ", end = " ")
    name = input()
    print("\nEnter your company name : ", end = " ")
    company = input()
    print("Enter your email : ", end = " ")
    email = input()
    print("Enter your phone number   : ", end = " ")
    phoneNum = input()
    print("Create your password      : ", end = " ")
    password = input()
    print("Confirm your password     : ", end = " ")
    confirmPassword = input()

    while (password != confirmPassword):
        print("\n------ Password Mismatch!!! -----", end="\n")
        print("Create your password      : ", end = " ")
        password = input()
        print("Confirm your password     : ", end = " ")
        confirmPassword = input()
    
    print("\nVerify your details\n")
    print("Name                   :  ", name)
    print("Email                  :  ", email)
    print("Company Name           :  ", company)
    print("Phone Number           :  ", phoneNum)

    details.extend([name, company, email, phoneNum, password])

    app.addVendor(details)
    