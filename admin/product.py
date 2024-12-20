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
            product_name = input("Enter product name: ")
            product_company = input("Enter product company: ")
            product_category = input("Enter product category: ")
            product_sub_category = input("Enter product sub-category: ")
            product_price = float(input("Enter product price: "))
            product_weight = float(input("Enter product weight (in g/kg/ml/l): "))
            product_count = int(input("Enter product count: "))

            # SQL query to insert product details into the 'products' table
            query = """
            INSERT INTO products 
            (name, company, category, sub_category, price, weight, count)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                product_name, 
                product_company, 
                product_category, 
                product_sub_category, 
                product_price, 
                product_weight, 
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
        print(f"Enter the ID of the product")
        print(f"If you dont know the product ID search for product name ")
        print(f"Enter the product name : ")
        name = input()

        query = "SELECT id, name FROM products"
        self.cursor.execute(query)
        products = self.cursor.fetchall()  # List of tuples: [(id1, name1), (id2, name2), ...]

        # Use fuzzy matching to find the best match for the entered name
        product_names = {product[1]: product[0] for product in products}  # {name: id}
        best_match, confidence, product_id = process.extractOne(name, product_names.items())

        if confidence > 60:  # Only consider matches with high confidence
            print(f"Best match found: '{best_match}' (Product ID: {product_id}) with confidence {confidence}%")
            
            # Proceed with updating the product details
            print(f"Enter the new price: ", end="")
            new_price = float(input())
            
            update_query = """
                UPDATE products
                SET price = %s
                WHERE id = %s
            """
            self.cursor.execute(update_query, (new_price, product_id))
            self.conn.commit()

            print(f"Product '{best_match}' updated successfully!")
        else:
            print("No close match found. Please try again with a more accurate product name.")
            

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

