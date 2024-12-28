import mysql.connector
import json
from datetime import datetime
from prettytable import PrettyTable
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from product import Product


# # Load configuration
with open('/Users/sathiska/Documents/python/E-Commerce-Using-Python/config.json', 'r') as config_file:
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
                return user[0]
            else:
                print("\nNo user found with the provided email and password.")
        
        except mysql.connector.Error as err:
            print(f"\nError: {err}")
        return False

app = EMSAPP()
product_app = Product(conn)
print("Welcome to SK Store")
print("\nEnter 1 to Login in to the System")
print("Enter 2 to Register")

print("\nEnter your choice : ", end = " ")
choice = int(input())

if (choice == 1):
    # print("\nEnter your email : ", end = " ")
    # email = input()

    # print("\nEnter the password : ", end = " ")
    # password = input()

    # res = app.getUserInfo(email,password)
    res = 1
    if (res):
        print("\n<---------  Main Dashboard --------->\n")

        query = """
            WITH RankedData AS (
                SELECT
                    name,
                    company,
                    category,
                    sub_category,
                    price,
                    ROW_NUMBER() OVER (PARTITION BY category ORDER BY id) AS row_num
                FROM
                    products
            )
            SELECT 
                name,
                company,
                category,
                sub_category,
                price
            FROM 
                RankedData
            WHERE 
                row_num <= 5; -- Fetch the first 4 rows from each subcategory
            """
        cursor.execute(query)
        products = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]  # Extract column names
        
        table_category = products[0][2]  # First product's category
        table = PrettyTable()

        for product in products:
            if table_category != product[2]:  # Check if category has changed
                table.add_column("Many More ...", [""] * len(table._rows))
                print("\n<--------- ", table_category," --------->\n")
                print(table)  # Print the table for the previous category

                # Create a new table for the new category
                table = PrettyTable()
                table_category = product[2]  # Update category

            # Transpose: Make each product a column instead of a row
            table.add_column(product[0], [product[i] for i in range(1,len(product))])

        # Print the last table
        table.add_column("Many More ...", [""] * len(table._rows))
        print("\n<--------- ", table_category," --------->\n")
        print(table)

        print("\n\n<--------- Search for the product name which you need --------->\n")
        try:
            product_app.search(True)

            product_id = input("\nChoose the product which you want to buy by entering its product ID : ")

            query = """
                SELECT * from products where id = %s
            """
            cursor.execute(query, (product_id,))
            selected_product = cursor.fetchone()
            
            selected_table = PrettyTable()

            column_title = selected_product[1]
            product_details = [str(selected_product[i]) for i in range(2, len(selected_product))]
            selected_table.add_column(column_title, product_details)
            
            actions = ["Add to Cart", "Add to Wishlist", "Buy now"]

            action_table = PrettyTable()
            action_table.field_names = ["Options"] 
            for action in actions:
                action_table.add_row([action])
            print(action_table)

            product_options = [
                "Enter 1 to buy the product",
                "Enter 2 to add product to cart",
                "Enter 3 to add product to wishlist",
                "Enter 4 to add review comments",
                "Enter 5 to see reviews of the product",
                "Enter 6 to Exit"
            ]

            num_product_options = len(product_options)

            print("\n")
            for product_option in product_options:
                print("---------> ",product_option)
            print("\n")

            user_options = int(input("\nEnter your choice : "))
            product_app.product_operations(user_options,product_id,res)
        except Exception as e:
            print(f"Error during search: {e}")

elif (choice == 2):
    details = []

    print("\nEnter your Name  : ", end = " ")
    name = input()
    print("\nEnter your email : ", end = " ")
    email = input()
    print("\nEnter your DOB (DD/MM/YYYY) : ", end = " ")
    dob = input()

    # Reformat DOB to MySQL DATE format
    try:
        dob = datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("\nError: Invalid date format. Please use DD/MM/YYYY.")
        exit()

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
    print("Name          :  ", name)
    print("Email         :  ", email)
    print("DOB           :  ", dob)
    print("Phone Number  :  ", phoneNum)

    details.extend([name, email, dob, phoneNum, password])

    app.addUser(details)
    




    