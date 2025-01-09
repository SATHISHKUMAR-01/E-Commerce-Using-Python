import mysql.connector
import json
from datetime import datetime
from prettytable import PrettyTable
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from product import Product
from wallet import Wallet
import random
import string

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

        try:

            product_actions = [
                "Enter 1 to view cart",
                "Enter 2 to view orders",
                "Enter 3 to view wishlist",
                "Enter 4 to go for search",
                "Enter 0 to Logout"
            ]

            while(True):
                print("\n")
                for product_action in product_actions:
                    print("---------> ",product_action)
                print("\n")
                product_action_choice  = int(input("Enter your choice : "))
                if product_action_choice == 0:
                    print("\n<--------- Logging out... --------->\n")
                    break
                self.dashboard_operation(product_action_choice, user_id)

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

    def dashboard_operation(self, product_action_choice, user_id):

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

            delete_choice = input("\nDo you want to remove any products from cart (y/n) : ")

            if delete_choice == "y" or delete_choice == "Y":
                id = int(input("\nEnter the product id : "))
                confirmation = input("\nAre you want to remove (y/n) : ")
                if confirmation == 'y' or confirmation == 'Y':
                    query = "DELETE from cart WHERE product_id = %s AND user_id = %s"
                    with conn.cursor() as cart_cursor:
                        cart_cursor.execute(query, (id, user_id))
                        conn.commit()
                        if cart_cursor.rowcount == 0:
                            print("\n<--------- No matching product found in your cart --------->\n")
                        else:
                            print("\n<--------- Product successfully removed from your cart --------->\n")
                                    
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
            order_mapping = {}
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
                    order_mapping[items[5]] = order_details[1:]
                    order_table.add_column(column_title, order_details)
                    print(order_table, "\n")

                is_exchange = input("\nDo you want to return or replace any product (y/n) : ")

                if is_exchange == 'Y' or is_exchange == 'y':
                    order_id = input("\nEnter the Order ID of the completed order : ")

                    exchange_options = [
                        "Press 1 to return the product",
                        "Press 2 to replace the product"
                    ]

                    for options in exchange_options:
                        print("\n---------> ", options)

                    exchange_choice = int(input("\nEnter your choice of exchange : "))

                    while (exchange_choice < 1 or exchange_choice > 2):
                        print("\nInvalid Choice !!!\n")
                        exchange_choice = int(input("\nEnter your choice of exchange : "))

                    query = """
                    SELECT wallet_id, amount from wallet where user_id = %s
                    """
                    with conn.cursor() as wallet_details:
                        wallet_details.execute(query, (user_id,))
                        wallet_info = wallet_details.fetchall()
                    
                    wallet_id = str(wallet_info[0])
                    wallet_amount = float(wallet_info[1])

                    order_amt = float(order_mapping[order_id][5].split(':')[1].strip())
                    
                    if exchange_choice == 1:
                        reason = input("\nEnter the reason for your return : ")

                        characters = string.ascii_uppercase + string.digits
                        return_id = ''.join(random.choices(characters, k=6))
                        
                        print("\n<--------- Your order amount will be credited back to your account, once product is collected --------->")

                        update_order_query = """
                        UPDATE orders SET order_status = %s WHERE order_id = %s
                        """

                        add_return_data = """
                        INSERT INTO return_table (return_id, order_id, reason, return_status)
                        VALUES (%s, %s, %s, %s)
                        """
                        
                        with conn.cursor() as update_order:
                            update_order.execute(update_order_query, ["Return", order_id])
                            update_order.commit()
                        
                            update_order.execute(add_return_data, [return_id, order_id, reason, "Pending"])
                            update_order.commit()

                        print("\n<--------- Product Return request successful --------->\n")

                    elif exchange_choice == 2:
                        reason = input("\nEnter the reason for your replacement : ")

                        replace_options = [
                            "Press 1 to replace the same product",
                            "Press 2 to replace the different product"
                        ]
                        
                        for options in replace_options:
                            print("\n---------> ", options)
                        
                        replace_choice = int(input("\nEnter your choice of replacement : "))

                        while (replace_choice < 1 or replace_choice > 2):
                            print("\nInvalid Choice !!!\n")
                            exchange_choice = int(input("\nEnter your choice of replacement : "))

                        payment_completed = False

                        if exchange_choice == 1:
                            print("<--------- Replacement requested for the old product --------->")
                            payment_completed = True

                        elif exchange_choice == 2:
                            print("\n<--------- Search for the product to replace --------->\n")

                            product_found = product_app.search(True)
                            while (not product_found):
                                product_found = product_app.search(True)
                            product_id = input("\nChoose the product which you want to buy by entering its product ID : ")

                            query = """
                                SELECT * from products where id = %s
                            """

                            with conn.cursor() as product_details:
                                product_details.execute(query, (product_id,))
                                product_info = product_details.fetchall()
                            
                            count = int(input("\nAdd the number of products you want to buy : "))

                            amt = count * product_info[0][5]

                            amt =  float(amt)
                            
                            if ( amt > order_amt) :
                                print("\nYour amount exceeds the previous ordered amount\n")
                                print("\nPay : ", amt - order_amt)

                                print("\n<--------- Checking your wallet balance --------->\n")

                                print("\nWallet Balance : ", wallet_amount)

                                balance_amt = amt - order_amt

                                while(not payment_completed):
                                    if (wallet_amount < balance_amt):
                                        print ("\n<--------- Insufficient Balance --------->\n")
    
                                        op = input("\nDo you want to recharge your wallet now (y/n) : ")

                                        if (op == 'Y' or op == 'y'):
                                            wallet_app.recharge_wallet(wallet_amount, wallet_id)
                                        else :
                                            payment_completed = True
                                            print("<--------- Payment failed !!! --------->\n")

                                    else :
                                        update_balance = wallet_amount - balance_amt

                                        wallet_app.deduct_amt_from_wallet(wallet_id, update_balance)

                                        payment_completed = True
                            else :
                                print("\nBalance Amount : ", order_amt - amt, " will be credited back to wallet\n")
                                wallet_app.recharge_wallet(order_amt - amt, wallet_id)
                                payment_completed = True


                        if (payment_completed):
                            print("\n<--------- Delivery Location Details --------->\n")

                            query = """
                                SELECT * from shipping_address where order_id = %s
                                """

                            with conn.cursor() as location_details:
                                location_details.execute(query, (order_id,))
                                location_info = location_details.fetchall()

                            address = location_info[6]
                            pincode = location_info[5]
                            city = location_info[4]
                            state = location_info[3]

                            print("\nAddress : ", address)
                            print("City    : ", city)
                            print("State   : ", state)
                            print("PinCode : ", pincode)

                            is_location_change = input("\nIs there any change in delivery location (y/n) ? ")

                            if is_location_change == 'y' or is_location_change == 'Y':
                                while(True):
                                    address = input("\nEnter the delivery address (Flat/Building No, Street, Area name) : ")
                                    city    = input("\nEnter the city    : ")
                                    state   = input("\nEnter the state   : ")
                                    pincode = input("\nEnter the pincode : ")

                                    print("\n<--------- Confirm your delivery address --------->\n")
                                    print("Address : ", address)
                                    print("City    : ", city)
                                    print("State   : ", state)
                                    print("PinCode : ", pincode)

                                    confirmation_location = input("\nEnter y/Y to confirm, if there is any change in address, Enter n/N : ")
                                    if confirmation_location == 'y' or confirmation_location == 'Y':
                                        break


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

            delete_choice = input("\nDo you want to remove any products from wishlist (y/n) : ")

            if delete_choice == "y" or delete_choice == "Y":
                id = int(input("\nEnter the product id : "))
                confirmation = input("\nAre you want to remove (y/n) : ")
                if confirmation == 'y' or confirmation == 'Y':
                    query = "DELETE from wishlist WHERE product_id = %s AND user_id = %s"
                    with conn.cursor() as wishlist_cursor:
                        wishlist_cursor.execute(query, (id, user_id))
                        conn.commit()
                        if wishlist_cursor.rowcount == 0:
                            print("\n<--------- No matching product found in your wishlist --------->\n")
                        else:
                            print("\n<--------- Product successfully removed from your wishlist --------->\n")

        elif product_action_choice == 4:
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

            print ("\n<---------  Today Offers --------->\n")
            product_app.viewOffer()

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
        