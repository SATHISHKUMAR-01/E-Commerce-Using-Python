import mysql.connector
import json
from datetime import datetime
from product import Product

LOGIN = 1
REGISTER = 2



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
                print("\n<--------- Login Successful --------->\n")
                return user
            else:
                print("\nNo vendor found with the provided email and password.")
        
        except mysql.connector.Error as err:
            print(f"\nError: {err}")
        
        return [] 

app = EMSVendor()
print("Welcome to SK Store - Vendor Page")
print("\nEnter 1 to Login in to the System")
print("Enter 2 to Register")

print("\nEnter your choice : ", end = " ")
choice = int(input())

product_app = Product(conn)

if (choice == LOGIN):
    print("\nEnter your email : ", end = " ")
    email = input()

    print("\nEnter the password : ", end = " ")
    password = input()

    res = app.getVendorInfo(email,password)

    if (res):
        print("\n<--------- Dashboard --------->\n")

        options = [
            "1. Add new product to the store",
            "2. Update the product price/stock details",
            "3. Delete product from the store",
            "4. View products present in the store",
            "5. Add Discount/Offer to the product",
            "6. Delete Discount/Offer of the product",
            "7. Update Discount/Offer of the products",
            "8. View Discount/Offer of the products",
            "9. View Sales Details",
            "0. Exit"
        ]

        numOptions = len(options)

        for option in options:
            print(option)

        print("\nEnter your choice of operation from the above : ", end = " ")
        operation = int(input())

        while (operation < 0 or operation > numOptions):
            print("Invalid Choice !!!\n")
            print("Enter your choice of operation from the above : ", end = " ")
            operation = int(input())

        
        match operation:
            case 1:
                print("\n<--------- Add new product --------->\n")
                product_app.addProduct()
            case 2:
                print("\n<--------- Update the product details --------->\n")
                product_app.updateProduct()
            case 3 :
                print("\n<--------- Delete product --------->\n")
            case 4 :
                print("\n<--------- View products --------->\n")
                product_app.viewProduct()
            case 5 :
                print("\n<--------- Add Discount/Offer --------->\n")
            case 6 :
                print("\n<--------- Delete Discount/Offer --------->\n")
            case 7 :
                print("\n<--------- Update Discount/Offer --------->\n")
            case 8 :
                print("\n<--------- View Discount/Offer --------->\n")
            case 9 :
                print("\n<--------- View Sales Details --------->\n")
            
            

elif (choice == REGISTER):
    details = []

    print("\nEnter your name  : ", end = " ")
    name = input()
    print("\nEnter your company name : ", end = " ")
    company = input()
    print("\nEnter your email : ", end = " ")
    email = input()
    print("\nEnter your phone number   : ", end = " ")
    phoneNum = input()
    print("\nCreate your password      : ", end = " ")
    password = input()
    print("\nConfirm your password     : ", end = " ")
    confirmPassword = input()

    while (password != confirmPassword):
        print("\n------ Password Mismatch!!! -----", end="\n")
        print("\nCreate your password      : ", end = " ")
        password = input()
        print("\nConfirm your password     : ", end = " ")
        confirmPassword = input()
    
    print("\nVerify your details\n")
    print("Name                   :  ", name)
    print("Email                  :  ", email)
    print("Company Name           :  ", company)
    print("Phone Number           :  ", phoneNum)

    details.extend([name, company, email, phoneNum, password])

    app.addVendor(details)
    