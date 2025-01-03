import mysql.connector
import json
from datetime import datetime
from prettytable import PrettyTable
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from product import Product
from wallet import Wallet

# # Load configuration
with open('/Users/sathiska/Documents/python/E-Commerce-Using-Python/config.json', 'r') as config_file:
    config = json.load(config_file)

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

class EMSAPP:
    def addUser(self, details):
        try:
            query = """
            INSERT INTO user (name, email, dob, phone_number, password, address, city, state, pincode)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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

    def main_dashboard(self,user_id):
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
        try:

            product_actions = [
                "Enter 1 to view cart",
                "Enter 2 to view orders",
                "Enter 3 to view wishlist",
                "Enter 0 to go for search"
            ]

            print("\n")
            for product_action in product_actions:
                print("---------> ",product_action)
            print("\n")

            product_action_choice  = int(input("Enter your choice : "))

            if product_action_choice == 1:

                print("\n<--------- Your cart details --------->\n")
                
                query = """
                    SELECT 
                        p.name AS product_name,
                        p.id AS product_id,
                        p.company,
                        p.category,
                        p.sub_category,
                        p.price,
                        c.count AS cart_count
                    FROM 
                        cart c
                    JOIN 
                        products p ON c.product_id = p.id
                    WHERE 
                        c.user_id = %s;

                    """
                conn = mysql.connector.connect(**config)
                with conn.cursor() as cart_cursor:
                    cart_cursor.execute(query, (user_id,))
                    cart_list = cart_cursor.fetchall()

                if (not cart_list):
                    print("\n<--------- Your cart is empty :( --------->\n")
                else:
                    self.view_product_info(cart_list)
                    
            elif product_action_choice == 2:
                print("\n<--------- Your orders --------->\n")

                query = """
                    SELECT 
                        p.name AS product_name,
                        p.id AS product_id,
                        p.company,
                        p.category,
                        p.sub_category,
                        
                        o.order_id,
                        o.total_amount,
                        o.payment_status,
                        o.order_status
                    FROM 
                        orders o
                    JOIN 
                        products p ON o.product_id = p.id
                    WHERE 
                        o.user_id = %s;
                    """
                
                conn = mysql.connector.connect(**config)
                with conn.cursor() as orders_cursor:
                    orders_cursor.execute(query, (user_id,))
                    order_info = orders_cursor.fetchall()

                if (not order_info):
                    print("\n<--------- No order placed :( --------->\n")
                else:
                    for items in order_info:
                        order_table = PrettyTable()
                        column_title = items[0]
                        order_details = [
                            f"Product ID   : {items[1]}",
                            f"Company      : {items[2]}",
                            f"Category     : {items[3]}",
                            f"Sub Category : {items[4]}",
                            "--------------------------",
                            f"Order Id     : {items[5]}",
                            f"Amount       : {items[6]}",
                            f"Payment Status : {items[7]}",
                            f"Delivery     : {items[8]}"
                        ]
                        order_table.add_column(column_title, order_details)
                        print(order_table, "\n")

            elif product_action_choice == 3:
                print("\n<--------- Your wishlist details --------->\n")
                
                query = """
                    SELECT 
                        p.name AS product_name,
                        p.id AS product_id,
                        p.company,
                        p.category,
                        p.sub_category,
                        p.price,
                        w.count AS cart_count
                    FROM 
                        wishlist w
                    JOIN 
                        products p ON w.product_id = p.id
                    WHERE 
                        w.user_id = %s;
                    """
                conn = mysql.connector.connect(**config)
                with conn.cursor() as wishlist_cursor:
                    wishlist_cursor.execute(query, (user_id,))
                    wishlist_list = wishlist_cursor.fetchall()

                if (not wishlist_list):
                    print("\n<--------- Your wishlist is empty :( --------->\n")
                else:
                    self.view_product_info(wishlist_list)

            elif product_action_choice == 0:
                print("\n\n<--------- Search for the product name which you need --------->\n")

                product_found = product_app.search(True)

                while (not product_found):
                    product_found = product_app.search(True)

                product_id = input("\nChoose the product which you want to buy by entering its product ID : ")

                product_app.view_product(product_id)
                product_app.product_actions()

                product_options = [
                    "Enter 1 to buy the product",
                    "Enter 2 to add product to cart",
                    "Enter 3 to add product to wishlist",
                    "Enter 4 to add review comments",
                    "Enter 5 to see reviews of the product",
                    "Enter 0 to Exit"
                ]
                print("\n")
                for product_option in product_options:
                    print("---------> ",product_option)
                print("\n")

                user_options = int(input("\nEnter your choice : "))
                product_app.product_operations(user_options,product_id,user_id)

        except Exception as e:
            print(f"Error during search: {e}")

    def view_product_info(self, product_data):
        for items in product_data:
            product_table = PrettyTable()
            column_title = items[0]
            product_details = [
                f"Product ID   : {items[1]}",
                f"Company      : {items[2]}",
                f"Category     : {items[3]}",
                f"Sub Category : {items[4]}",
                f"Price        : {items[5]}",
                f"Count        : {items[6]}",
            ]
            product_table.add_column(column_title, product_details)
            print(product_table, "\n")

app = EMSAPP()
product_app = Product(conn)
wallet_app = Wallet(conn)
print("Welcome to SK Store")
print("\nEnter 1 to Login in to the System")
print("Enter 2 to Register")

print("\nEnter your choice : ", end = " ")
choice = int(input())

if (choice == 1):
    print("\nEnter your email : ", end = " ")
    email = input()

    print("\nEnter the password : ", end = " ")
    password = input()

    res = app.getUserInfo(email,password)
    
    if (res):
        app.main_dashboard(res)

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

    address = input("\nEnter your address (Flat/Building Number, Street Name, Area) : ")
    city = input("\nEnter your city : ")
    state = input("\nEnter your state : ")
    pincode = input("\nEnter your pincode : ")
    
    print("\n<--------- Verify your details --------->\n")
    print("Name          :  ", name)
    print("Email         :  ", email)
    print("DOB           :  ", dob)
    print("Phone Number  :  ", phoneNum)
    print("Address       :  ", address)
    print("City          :  ", city)
    print("State         :  ", state)
    print("Pincode       :  ", pincode)

    details.extend([name, email, dob, phoneNum, password, address, city, state, pincode])

    app.addUser(details)

    query = """
            SELECT id from users where email = %s and phone_number = %s
            """
    cursor.execute(query, (email,phoneNum,))
    user_id = cursor.fetchone()
    user_id = user_id[0]

    print("\n<--------- Add money to your E-Wallet and Enjoy Shopping !!! --------->\n")

    opinion = input("Do you want add money to your wallet now ? Enter y/Y to continue, Enter n/N to skip : ")

    if opinion == 'y' or opinion == 'Y':
        wallet_app.create_wallet(user_id)
    
    app.main_dashboard(user_id)
        