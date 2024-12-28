import mysql.connector
from prettytable import PrettyTable
from rapidfuzz import process

class Product:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.discount_code_buy_x_get_x = "D0001"
        self.discout_code_flat_percent = "D0002"

    def addProduct(self):
        # Code to add product details
        try:        
            # Prompt user for product details
            product_name = input("Enter product name (Add product weight in name. Example : 1kg/500ml): ")
            product_company = input("Enter product company: ")
            product_category = input("Enter product category: ")
            product_sub_category = input("Enter product sub-category: ")
            product_price = float(input("Enter product price: "))
            product_count = int(input("Enter product count: "))

            # SQL query to insert product details into the 'products' table
            query = """
            INSERT INTO products 
            (name, company, category, sub_category, price, count)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                product_name, 
                product_company, 
                product_category, 
                product_sub_category, 
                product_price,
                product_count
            )

            # Execute the query
            self.cursor.execute(query, values)
            self.conn.commit()

            print("\nProduct added successfully!")

        except mysql.connector.Error as err:
            print(f"\nError: {err}")
        except ValueError:
            print("\nInvalid input. Please enter the correct values.")

    def updateProduct(self):
        # Code to update product details
        print(f"If you dont know the product ID search for product name, press (Y/y) to search for product ID \n")

        choice = input("Do you want to search (y/n) : ")

        if (choice == 'y' or choice == 'Y'):
            self.search()
            
        product_id = int(input("\nEnter the ID of the product : "))

        print ("<--------- Which field you need to update --------->\n")

        options = [
            "1. Update the product name",
            "2. Update the company/manufacturer of the product",
            "3. Update the category of the product",
            "4. Update the sub_category of the product",
            "5. Update the price of the product",
            "6. Update the count of the product",
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
                print("\n<--------- Update the product name --------->\n")       
                new_name = input("Enter the new name: ")
                self.update(new_name,"name", "products", product_id)
                   
            case 2:
                print("\n<--------- Update the company/manufacturer of the product --------->\n")  
                new_company = input("Enter the new company: ")
                self.update(new_company,"company", "products", product_id)
                
            case 3 :
                print("\n<--------- Update the category of the product --------->\n")
                new_category = int(input("Enter the new category: "))
                self.update(new_category,"category", "products", product_id)
                
            case 4 :
                print("\n<--------- Update the sub_category of the product --------->\n")
                new_sub_category = int(input("Enter the new sub_category: "))
                self.update(new_sub_category,"sub_category", "products", product_id)
                
            case 5 :
                print("\n<--------- Update the price of the product --------->\n")
                new_price = float(input("Enter the new price: "))
                self.update(new_price,"price", "products", product_id)

            case 6 :
                print("\n<--------- Update the count of the product --------->\n")
                new_count = int(input("Enter the new count: "))
                self.update(new_count,"count", "products", product_id)
            
    def deleteProduct(self):
        # Code to delete a product
        print(f"If you dont know the product ID search for product name, press (Y/y) to search for product ID \n")

        choice = input("Do you want to search (y/n) : ")

        if (choice == 'y' or choice == 'Y'):
            self.search()
            
        product_id = int(input("\nEnter the ID of the product : "))

        confirmation = input(("\nAre you sure you want to delete this product (y/n)? "))

        if confirmation == 'y' or confirmation == 'Y':
            self.delete("products", "id",  product_id)
        else:
            print("<--------- Product Delete Operation Failed --------->")
    
    def viewProduct(self):
        
        query = """
            SELECT * FROM products
            """
        self.cursor.execute(query)
        products =self.cursor.fetchall()

        # Dynamically fetch column names from the cursor description
        columns = [desc[0] for desc in self.cursor.description]  # Extract column names

        table = PrettyTable()
        table.field_names = columns

        for product in products:
            table.add_row(product)

        print(table)

    def addOffer(self):
        # Code to add offer to product
        print("<--------- Search for the product to add offer (One product at a time) --------->\n")
        self.search()

        product = input("\nEnter the product ID : ")

        print("\n<--------- Available Discount Options --------->\n")

        discount_options = [
            "1. Buy X Get Y Offer",
            "2. Flat Discount for certain percentage"
        ]

        numOptions = len(discount_options)

        for option in discount_options:
            print(option)

        operation  = int(input("\nWhat type of offer/discount, do you want to apply to the product : "))

        while (operation < 1 or operation > numOptions):
            print("Invalid Choice !!!\n")
            print("Enter your choice of operation from the above : ", end = " ")
            operation = int(input())

        match operation:
            case 1:
                print("\n<--------- Add Buy X Get Y Offer --------->\n")
                buy_x = int(input("Enter the buy quantity value : "))
                get_x = int(input("\nEnter the get quantity value : "))
                discount_code = self.discount_code_buy_x_get_x
                flat_percentage = 0.00

                query = """
                INSERT INTO discount 
                (product_id, discount_type, buy_val, get_val, flat_percentage)
                VALUES (%s, %s, %s, %s, %s)
                """
                values = (
                    product, 
                    discount_code, 
                    buy_x, 
                    get_x, 
                    flat_percentage
                )

                # Execute the query
                self.cursor.execute(query, values)
                self.conn.commit()
            case 2:
                print("\n<--------- Add Flat Discount for the product --------->\n")
                buy_x = 0
                get_x = 0
                discount_code = self.discout_code_flat_percent
                flat_percentage = float(input("\nEnter the discount percentage : "))
                
                query = """
                INSERT INTO discount 
                (product_id, discount_type, buy_val, get_val, flat_percentage)
                VALUES (%s, %s, %s, %s, %s)
                """
                values = (
                    product, 
                    discount_code, 
                    buy_x, 
                    get_x, 
                    flat_percentage
                )

                # Execute the query
                self.cursor.execute(query, values)
                self.conn.commit()

        print("\n<---------Offer added to the product successfully --------->")
    
    def updateOffer(self):
        # Code to update product details
        print("Search for the product to which offer details are added")

        self.search()

        id = input("\nEnter the product id of the product : ")

        print("\n<--------- Searching for the discount/offer of product ID ", id," --------->")

        query = """
                SELECT * FROM discount WHERE product_id = %s
                """
        self.cursor.execute(query, tuple(id))
        offers = self.cursor.fetchall()

        columns = [desc[0] for desc in self.cursor.description]

        table = PrettyTable()
        table.field_names = columns

        for offer in offers:
            table.add_row(offer)

        print(table)

        offer_id = input("\nEnter the discount id for which you need to update : ")

        print("\n<--------- Selected Discount ID : ", offer_id, " --------->\n")

        print("\n<--------- Which field you need to update --------->\n")

        options = [
            "1. Update the discount type",
            "2. Update the buy value",
            "3. Update the get value",
            "4. Update the flat percentage",
        ]

        numOptions = len(options)

        for option in options:
            print(option)

        print("\nEnter your choice of operation from the above : ", end = " ")
        operation = int(input())

        while (operation < 1 or operation > numOptions):
            print("Invalid Choice !!!\n")
            print("Enter your choice of operation from the above : ", end = " ")
            operation = int(input())
        
        match operation:
            case 1:
                print("\n<--------- Update the discount type --------->\n")       
                new_discount_type = input("Enter the new discount type (D0001/D0002) : ")
                self.update(new_discount_type,"discount_type", "discount", offer_id)
                   
            case 2:
                print("\n<--------- Update the buy value --------->\n")  
                new_buy_val = input("Enter the new buy value : ")
                self.update(new_buy_val,"buy_val", "discount", offer_id)
                
            case 3 :
                print("\n<--------- Update the get value --------->\n")
                new_get_val = int(input("Enter the new get value : "))
                self.update(new_get_val,"get_val", "discount", offer_id)
                
            case 4 :
                print("\n<--------- Update the flat percentage --------->\n")
                new_percent = int(input("Enter the new flat percentage : "))
                self.update(new_percent,"flat_percentage", "discount", offer_id)
                
    def deleteOffer(self):
        # Code to delete a product
        print("Search for the product to which offer details are added")

        self.search()

        id = input("\nEnter the product id of the product : ")

        print("\n<--------- Searching for the discount/offer of product ID ", id," --------->")

        query = """
                SELECT * FROM discount WHERE product_id = %s
                """
        self.cursor.execute(query, tuple(id))
        offers = self.cursor.fetchall()

        columns = [desc[0] for desc in self.cursor.description]

        table = PrettyTable()
        table.field_names = columns

        for offer in offers:
            table.add_row(offer)

        print(table)

        offer_id = input("\nEnter the discount id for which you need to delete : ")

        print("\n<--------- Selected Discount ID : ", offer_id, " --------->\n")

        confirmation = input(("\nAre you sure you want to delete this offer (y/n)? "))

        if confirmation == 'y' or confirmation == 'Y':
            self.delete("discount", "discount_id",  offer_id)
        else:
            print("<--------- Offer Delete Operation Failed --------->")
    
    def viewOffer(self):
        query = """
            SELECT * FROM discount
            """
        self.cursor.execute(query)
        products =self.cursor.fetchall()

        # Dynamically fetch column names from the cursor description
        columns = [desc[0] for desc in self.cursor.description]  # Extract column names

        table = PrettyTable()
        table.field_names = columns

        for product in products:
            table.add_row(product)

        print(table)

    def update(self,new_value,column_name,table_name,product_id):
        try:
            # Dynamic query to update any column
            update_query = ""
            if table_name == "products":
                update_query = f"UPDATE {table_name} SET {column_name} = %s WHERE id = %s"
            elif table_name == "discount":
                update_query = f"UPDATE {table_name} SET {column_name} = %s WHERE discount_id = %s"

            self.cursor.execute(update_query, (new_value, product_id))  # Pass values safely to prevent SQL injection

            # Commit the changes
            self.conn.commit()
            print(f"\nUpdated successfully: {column_name} = {new_value}")
        except Exception as e:
            print(f"Error updating product: {e}")
    
    def delete(self,table_name,column_name,value):
        try:
            # SQL query to delete the product
            delete_query = f"DELETE FROM {table_name} WHERE {column_name} = %s"
            self.cursor.execute(delete_query, (value,))  # Pass ID as a parameter
            
            # Commit the changes
            self.conn.commit()
            
            print(f"\nProduct ID {value} deleted successfully!\n")
        except Exception as e:
            print(f"Error deleting product: {e}")

    def search(self, user=False):
        try:
            # Check and reconnect to database if not connected
            if not self.conn.is_connected():
                self.conn.reconnect(attempts=3, delay=2)

            # Take product name input
            name = input("\nEnter the product name: ").strip()

            # Define SQL query based on user type
            query = (
                "SELECT id, name, company, category, sub_category, price FROM products"
                if user
                else "SELECT id, name, company, category, sub_category, price, count FROM products"
            )

            # Reinitialize the cursor
            self.cursor.close()
            self.cursor = self.conn.cursor()

            # Execute query and fetch products
            self.cursor.execute(query)
            products = self.cursor.fetchall()

            # Map product details for fuzzy matching
            product_details = {
                "|".join(map(str, product[1:])): product[0] for product in products
            }

            # Extract product keys for fuzzy matching
            concatenated_keys = list(product_details.keys())

            # Use `rapidfuzz` for fuzzy matching
            best_match = process.extract(name, concatenated_keys, score_cutoff=60)

            # Check if matches are found
            if best_match:
                print("\nResults Found:\n")
                table = PrettyTable()

                for idx, match in enumerate(best_match, 1):
                    matched_name, confidence = match[0], match[1]

                    # Fetch product ID using matched name
                    product_id = product_details[matched_name]

                    # Split details into fields
                    product_info = matched_name.split('|')

                    # Format labels for display
                    labels = [
                        f"Company      : {product_info[1]}",
                        f"Category     : {product_info[2]}",
                        f"Sub Category : {product_info[3]}",
                        f"Price        : {product_info[4]}",
                    ]

                    # Add Stock Count for admin view
                    if not user:
                        labels.append(f"Stock Count  : {product_info[5]}")

                    # Add Product ID
                    labels.append(f"Product ID   : {product_id}")

                    # Add product details as a column in the table
                    table.add_column(product_info[0], labels)

                # Print table
                print(table)

            else:
                print("\nNo product found. Please try again!!!")

        except Exception as e:
            print(f"\nError during search: {e}")

    def product_operations(self, user_options, product_id, user_id):
        
        if (user_options == 1):
            # Code to buy the product
            count = int(input("\nAdd the number of products you want to add to buy : "))
            pass
        elif(user_options == 2):
            # Code to add the product to cart
            count = int(input("\nAdd the number of products you want to add to cart : "))

            query = """
            INSERT INTO cart (product_id, user_id, count)
            VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, [product_id, user_id, count])
            self.conn.commit()
            print("\n<--------- Product added to cart successfully! --------->\n")
        elif(user_options == 3):
            # Code to add the product to wishlist
            count = int(input("\nAdd the number of products you want to add to wishlist : "))

            query = """
            INSERT INTO wishlist (product_id, user_id, count)
            VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, [product_id, user_id, count])
            self.conn.commit()
            print("\n<--------- Product added to wishlist successfully! --------->\n")
            
        elif(user_options == 4):
            # Code to add review comments
            print("\nAdd review to the product\n")

            comments = input("\nAdd your comments : ")

            # Input validation for rating
            while True:
                try:
                    rating = int(input("\nAdd your rating to the product (out of 5): "))
                    if 1 <= rating <= 5:  # Ensure rating is between 1 and 5
                        break
                    else:
                        print("\nInvalid rating! Please enter a value between 1 and 5.")
                except ValueError:
                    print("\nInvalid input! Please enter a number between 1 and 5.")
            print("\n<--------- Your Feedback --------->\n")
            print("Comment  : ", comments)
            print("Rating   : ", rating)

            proceed = input("\nEnter y/Y to add comments : ")

            if (proceed == 'y' or proceed == 'Y'):
                query = """
                INSERT INTO review (product_id, user_id, comments, rating)
                VALUES (%s, %s, %s, %s)
                """
                self.cursor.execute(query, [product_id, user_id, comments, rating])
                self.conn.commit()
                print("\n<--------- Review added successfully! --------->\n")
            else:
                print("\n<--------- Review failed! --------->\n")
            
        elif(user_options == 5):
            # Code to see review comments of the product
            query = """
                SELECT r.comments, r.rating, r.timestamp, u.name AS user_name
                FROM review r
                JOIN user u ON r.user_id = u.id
                WHERE r.product_id = %s
                ORDER BY r.timestamp DESC
            """
            self.cursor.execute(query, (product_id,))
            reviews = self.cursor.fetchall()

            if reviews:
                print("\n<--------- Reviews --------->\n")
                print("\n<--------------------------->\n")
                for review in reviews:
                    print(f"User      : {review[3]}")
                    print(f"Comment   : {review[0]}")
                    print(f"Rating    : {review[1]}")
                    print(f"Timestamp : {review[2]}\n")
                    print("\n<--------------------------->\n")
            else:
                print("\nNo reviews available for this product.\n")
        else:
            # Code to exit
            pass