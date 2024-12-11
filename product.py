import mysql.connector

class Product:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def addProduct(self, product_details):
        # Code to add a product
        print("Product added successfully!")

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

