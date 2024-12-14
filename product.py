import mysql.connector

class Product:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def addProduct(self, product_details):
    
        try:        
            # Prompt user for product details
            product_name = input("Enter product name: ")
            product_company = input("Enter product company: ")
            product_category = input("Enter product category: ")
            product_sub_category = input("Enter product sub-category: ")
            product_price = float(input("Enter product price: "))
            product_weight = float(input("Enter product weight (in kg): "))
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

    def updateProduct(self, product_id, updates):
        # Code to update product details
        print(f"Product {product_id} updated!")

    def deleteProduct(self, product_id):
        # Code to delete a product
        print(f"Product {product_id} deleted!")
    
    def viewProduct(self):
        print(f"Product {product_id} Display!")

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

