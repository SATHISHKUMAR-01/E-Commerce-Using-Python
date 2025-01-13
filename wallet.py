import mysql.connector
import random
import string

class Wallet:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        
    def generate_wallet_id(self, length=6):
        # Generate a random string with uppercase letters and digits
        characters = string.ascii_uppercase + string.digits
        wallet_id = ''.join(random.choices(characters, k=length))
        return wallet_id
    
    def create_wallet(self,user_id):

        bank_list = [
            '1. HSBC Bank',
            '2. Bank of India',
            '3. HDFC Bank',
            '4. ICICI Bank',
            '5. Axis Bank',
            '6. State Bank of India',
            '7. Punjab National Bank',
            '8. Canara Bank',
            '9. Bank of Baroda',
            '10. Union Bank of India'
        ]
        
        print("\n")
        for bank in bank_list:
            print(bank)
        
        selected_bank = int(input("\nChoose the bank from the list : "))

        print("\n<--------- Selected Bank : ", bank_list[selected_bank-1], " --------->\n")

        money = float(input("\nEnter the amount you want to add to the wallet : "))

        # Generate and print a wallet ID
        wallet_id = self.generate_wallet_id()

        print("\nYour Wallet ID : ", wallet_id)

        query = """       
            INSERT INTO wallet (wallet_id, user_id, amount)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, [wallet_id, user_id, money])
        self.conn.commit()

        print("\n<--------- E-Wallet created successfully !!! --------->")

    def recharge_wallet(self, wallet_amt, wallet_id):
        money = float(input("\nEnter the amount you want to add to the wallet : "))

        update_balance = money + wallet_amt
        query = """       
            UPDATE wallet SET amount = %s WHERE wallet_id = %s
        """
        self.cursor.execute(query, [update_balance, wallet_id])
        self.conn.commit()

        print("\n<--------- Wallet Recharged successfully !!! --------->\n")
    
    def deduct_amt_from_wallet(self,wallet_id, update_balance):
        query = """       
             UPDATE wallet SET amount = %s WHERE wallet_id = %s
            """
        self.cursor.execute(query, [update_balance, wallet_id])
        self.conn.commit()

    def add_wallet_amt(self, wallet_amount, wallet_id, return_amt):
        amt = float(wallet_amount) + float(return_amt)
        query = """       
            UPDATE wallet SET amount = %s WHERE wallet_id = %s
        """
        self.cursor.execute(query, [amt, wallet_id])
        self.conn.commit()
