import mariadb
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

def get_connection() -> mariadb.Connection:
    try:
        conn = mariadb.connect(
            user= os.getenv('DB_USERNAME'),
            password = os.getenv('DB_PASSWORD'),
            host = os.getenv('DB_HOST'),
            port = int(os.getenv('DB_PORT')),
            database = os.getenv('DB_DATABASE') 
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")  
        return False

    return conn

class Transactions():          
    trx_cache = []
    def save_transaction(self, conn: mariadb.Connection)->bool:
        cur = conn.cursor()
        # positional 
        sql = """
        INSERT INTO tbl_transactions(stock_code, tick_time, price, shares, type)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            cur.executemany(sql, self.trx_cache)
            conn.commit()
            cur.close()
            self.trx_cache = []
            return True
        except mariadb.Error as e:
            print("Database Error : ", e)
            conn.rollback()
            return False    
        
if __name__ == '__main__':     
    conn = get_connection()
    trx = Transactions()
    trx.trx_cache.append(('AMRT', datetime.datetime.strptime('2024-12-25 10:30:45', "%Y-%m-%d %H:%M:%S"), 100.40, 100, 1))
    trx.save_transaction(conn)



