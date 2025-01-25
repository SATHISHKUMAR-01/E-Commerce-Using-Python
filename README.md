# E-Commerce-Using-Python

This is an e-commerce platform built using Python where users and vendors can interact with the system to manage products, place orders, and handle transactions. The platform provides separate functionalities for customers and vendors.

Features

Vendor Features:

Vendor Registration: Vendors can register on the platform.
Product Management: Vendors can add, update, delete, or view products.
Discount Management: Vendors can add, update, delete, or view discounts/offers on products.
Order Management: Vendors can view orders, change the order status to 'delivered', and manage return and dispatched orders.
Sales Overview: Vendors can view sales data.

Vendor Operations:

    "1. Add new product to the store",
    "2. Update the product price/stock details",
    "3. Delete product from the store",
    "4. View products present in the store",
    "5. Add Discount/Offer to the product",
    "6. Delete Discount/Offer of the product",
    "7. Update Discount/Offer of the products",
    "8. View Discount/Offer of the products",
    "9. View Sales Details",
    "10. View current orders",
    "11. View Dispatched orders",
    "12. View completed orders",
    "13. Change order status to delivered",
    "14. View return orders",
    "0. Exit"

Customer Features:

Customer Registration/Login: Customers can register and log in to the platform.
Profile Management: Customers can edit their profiles and view their wallets.
Product Search & Purchase: Customers can search for products by category, buy products, add them to the cart, or save them in a wishlist.
Order and Wishlist Management: Customers can view their cart, orders, and wishlist. They can also cancel or return items.
Product Reviews: Customers can add and view reviews on products.

Customer Operations:

    "1. View cart",
    "2. View orders",
    "3. View wishlist",
    "4. Go to search",
    "5. Edit profile",
    "6. View wallet",
    "7. Logout"

Product Operations for Customers:

    "1. Buy the product",
    "2. Add product to cart",
    "3. Add product to wishlist",
    "4. Add review comments",
    "5. See reviews of the product",
    "0. Exit"

Order Management:

Order Status: Customers and vendors can track the order status, which includes:

Pending
Dispatched
Delivered
Cancelled
Returned
Replaced

Payment and Wallet:

Wallet System: Each user has a wallet for managing funds.
Order Payment: Users can pay for orders directly using their wallet balance.

SQL Tables:

The following tables are created to store data for various functionalities in the e-commerce platform:

cancel_table	    Stores information about cancelled orders
cart	            Stores cart details for users
discount	        Stores product discounts and offers
orders	            Stores customer orders
products	        Stores details about products
replace_table	    Stores information about replaced items
return_table	    Stores information about returned items
review	            Stores customer reviews
shipping_address	Stores shipping address of users
user	            Stores user details
vendor	            Stores vendor details
wallet	            Stores wallet details for users
wishlist	        Stores products added to the wishlist

Database Schema:

The database schema for the platform involves multiple relationships between products, users, vendors, orders, and more. The core tables for handling transactions and managing user data are user, vendor, orders, cart, products, and wallet.


Setup Instructions:

Prerequisites:
Python 3.x
MySQL (or any other relational database)

Installation:

Clone the repository:

git clone https://github.com/yourusername/ecommerce-project.git
cd ecommerce-project

Setup the database:

Create a database and import the schema from database_schema.sql.
Update database credentials in the configuration file.

Run the application:

python admin/app.py  --> For Vendor

python user/app.py   --> For User

Configuration:
Database connection details can be configured in config.json.
