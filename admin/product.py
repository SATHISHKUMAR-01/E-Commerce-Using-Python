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
        print(f"Product {product_id} updated!")

    def deleteOffer(self):
        # Code to delete a product
        print(f"Product {product_id} deleted!")
    
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
            update_query = f"UPDATE {table_name} SET {column_name} = %s WHERE id = %s"
            self.cursor.execute(update_query, (new_value, product_id))  # Pass values safely to prevent SQL injection

            # Commit the changes
            self.conn.commit()
            print(f"\nProduct ID {product_id} updated successfully: {column_name} = {new_value}")
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

    def search(self):
        
        name = input("\nEnter the product name : ")

        query = "SELECT id, name FROM products"
        self.cursor.execute(query)
        products = self.cursor.fetchall()  # List of tuples: [(id1, name1), (id2, name2), ...]

        # Use fuzzy matching to find the best match for the entered name
        product_names = {product[1]: product[0] for product in products}  # {name: id}
        best_match = process.extract(name, product_names.keys(), score_cutoff=80)

        if best_match:  # Only consider matches with high confidence
            print("\nResults Found : \n")
            for idx, match in enumerate(best_match, 1):
                matched_name, confidence, _ = match
                matched_id = product_names[matched_name]
                print(f"{matched_name}  (Product ID: {matched_id})")

        else:
            print("No product found. Please try again !!!")
            


