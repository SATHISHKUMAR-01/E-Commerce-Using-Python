import mysql.connector
from prettytable import PrettyTable
from rapidfuzz import process

class Product:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def addProduct(self):
    
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
        product_id = 0
        print(f"If you dont know the product ID search for product name, press (Y/y) to search for product ID \n")

        choice = input("Do you want to search (y/n) : ")

        if (choice == 'y' or choice == 'Y'):
            name = input("\nEnter the product name : ")

            query = "SELECT id, name FROM products"
            self.cursor.execute(query)
            products = self.cursor.fetchall()  # List of tuples: [(id1, name1), (id2, name2), ...]

            # Use fuzzy matching to find the best match for the entered name
            product_names = {product[1]: product[0] for product in products}  # {name: id}
            best_match = process.extract(name, product_names.keys(), score_cutoff=80)

            if best_match:  # Only consider matches with high confidence
                for idx, match in enumerate(best_match, 1):
                    matched_name, confidence, _ = match
                    matched_id = product_names[matched_name]
                    print(f"{idx}. {matched_name} (ID: {matched_id}")

                # Ask the user to choose a specific product
                selection = int(input("\nEnter the number of the product you want to update: "))
                selected_name = best_match[selection - 1][0]
                product_id = product_names[selected_name]
            else:
                print("No product found. Please try again !!!")
        
        product_id = int((f"Enter the ID of the product : "))

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
                update_query = "UPDATE products SET name = %s WHERE id = %s"
                self.cursor.execute(update_query, (new_name, product_id))   
            case 2:
                print("\n<--------- Update the company/manufacturer of the product --------->\n")  
                new_count = int(input("Enter the new category: "))
                update_query = "UPDATE products SET category = %s WHERE id = %s"
                self.cursor.execute(update_query, (new_count, product_id))
            case 3 :
                print("\n<--------- Update the category of the product --------->\n")
                new_count = int(input("Enter the new category: "))
                update_query = "UPDATE products SET category = %s WHERE id = %s"
                self.cursor.execute(update_query, (new_count, product_id))
            case 4 :
                print("\n<--------- Update the sub_category of the product --------->\n")
                new_count = int(input("Enter the new sub_category: "))
                update_query = "UPDATE products SET sub_category = %s WHERE id = %s"
                self.cursor.execute(update_query, (new_count, product_id))
            case 5 :
                print("\n<--------- Update the price of the product --------->\n")
                new_price = float(input("Enter the new price: "))
                update_query = "UPDATE products SET price = %s WHERE id = %s"
                self.cursor.execute(update_query, (new_price, product_id))
            case 6 :
                print("\n<--------- Update the count of the product --------->\n")
                new_count = int(input("Enter the new count: "))
                update_query = "UPDATE products SET count = %s WHERE id = %s"
                self.cursor.execute(update_query, (new_count, product_id))

        self.conn.commit()
        print("\nProduct updated successfully!")
            
    def deleteProduct(self, product_id):
        # Code to delete a product
        print(f"Product {product_id} deleted!")
    
    def viewProduct(self):
        
        query = """
            SELECT * FROM products
            """
        self.cursor.execute(query)
        products =self.cursor.fetchall()

        table = PrettyTable()
        table.field_names = ["ID", "Product Name", "Company", "Category", "Sub-category", "Price", "Weight", "Stock Count"]

        for product in products:
            table.add_row(product)

        print(table)
        

    def addOffer(self, offer_details):
        # Code to add a product
        print("Product added successfully!")

    def updateOffer(self, product_id, updates):
        # Code to update product details
        print(f"Product {product_id} updated!")

    def deleteOffer(self, product_id):
        # Code to delete a product
        print(f"Product {product_id} deleted!")
    
    def viewOffer(self):
        print(f"Product {product_id} Display!")

