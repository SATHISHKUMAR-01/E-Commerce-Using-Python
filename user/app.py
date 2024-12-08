import mysql.connector
import json
from datetime import datetime

# # Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

class EMSAPP:
    def addUser(self, details):
        try:
            query = """
            INSERT INTO user (name, email, dob, phone_number, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, details)
            conn.commit()
            print("\nUser registered successfully!")
        except mysql.connector.Error as err:
            print(f"\nError: {err}")
            
    def getUserInfo(self,email,password):
        try:
            query = "SELECT * FROM user WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()

            if user:
                print("\nUser found! Welcome back.")
                print("User Details: ", user)
            else:
                print("\nNo user found with the provided email and password.")
        
        except mysql.connector.Error as err:
            print(f"\nError: {err}")

app = EMSAPP()
print("Welcome to SK Store")
print("\nEnter 1 to Login in to the System")
print("Enter 2 to Register")

print("\nEnter your choice : ", end = " ")
choice = int(input())

if (choice == 1):
    print("\nEnter your email : ", end = " ")
    email = input()

    print("Enter the password : ", end = " ")
    password = input()

    app.getUserInfo(email,password)

elif (choice == 2):
    details = []

    print("\nEnter your Name  : ", end = " ")
    name = input()
    print("Enter your email : ", end = " ")
    email = input()
    print("Enter your DOB (DD/MM/YYYY) : ", end = " ")
    dob = input()

    # Reformat DOB to MySQL DATE format
    try:
        dob = datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("\nError: Invalid date format. Please use DD/MM/YYYY.")
        exit()

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
    print("Name          :  ", name)
    print("Email         :  ", email)
    print("DOB           :  ", dob)
    print("Phone Number  :  ", phoneNum)

    details.extend([name, email, dob, phoneNum, password])

    app.addUser(details)
    




    