import mysql.connector

def connect_sql():

    # Replace these values with your actual MySQL server details
    host = "sql12.freemysqlhosting.net"
    user = "sql12674443"
    password = "HykJ5ctNhG"
    database = "sql12674443"

    # local mySQL 
    # host = "localhost"
    # user = "root"
    # password = "NewPass123@@"
    # database = "so"

    # Establish a connection to MySQL
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    return conn


def account_exists(conn, user_id, account_number):
    cursor = conn.cursor()

    query = f"SELECT account_id FROM accounts WHERE account_number = '{account_number}' AND user_id = {user_id};"
    cursor.execute(query)

    result = cursor.fetchone()

    return result


def create_or_get_account(conn, user_id, account_number):
    cursor = conn.cursor()

    try:
        if account_exists(conn, user_id, account_number):
            query = f"SELECT account_id FROM accounts WHERE account_number = '{account_number}' AND user_id = {user_id};"
            cursor.execute(query)
            result = cursor.fetchone()
            account_id = result[0]
            return account_id

        else: 
            print("creating the account.")
            query1 = f"INSERT INTO accounts (user_id, account_number) VALUES (1, '{account_number}')"
            cursor.execute(query1)
            query3 = f"INSERT INTO accounts (user_id, account_number) VALUES (3, '{account_number}')"
            cursor.execute(query3)
            query6 = f"INSERT INTO accounts (user_id, account_number) VALUES (6, '{account_number}')"
            cursor.execute(query6)
            conn.commit()
            # Handle the case where the account creation was not successful
            return create_or_get_account(conn, user_id, account_number)
    
    except Exception as e:
        # Handle any exceptions, print or log the error
        print(f"Error in create_or_get_account: {e}")
        # Rollback changes in case of an error
        conn.rollback()
        return None
    
    finally:
        # Close the cursor
        cursor.close()


def get_account_summary(conn, account_id):
    cursor = conn.cursor()

    try:

        # Account exists, fetch the summary for the account_id
        cursor.execute("""
            SELECT total_asset, total_cash, margin_ratio
            FROM summary
            WHERE account_id = %s
        """, (account_id,))
        
        # Fetch the summary
        summary = cursor.fetchone()

        if summary:
            # Convert the result to a dictionary
            summary_dict = {
                'total_asset': float(summary[0]),
                'total_cash': float(summary[1]),
                'margin_ratio': float(summary[2])
            }
            return summary_dict
        else:
            # No summary found for the account
            print(f"No summary found for account_id {account_id}.")
            return {}


    except Exception as e:
        # Handle any exceptions, print or log the error
        print(f"Error in get_account_summary: {e}")
        # Return an empty dictionary in case of an error
        return {}

    finally:
        # Close the cursor
        cursor.close()


def add_or_modify_summary(conn, account_id, total_asset, total_cash, margin_ratio):
    cursor = conn.cursor()

    try:
        # Check if summary exists for the given account_id
        cursor.execute("SELECT COUNT(*) FROM summary WHERE account_id = %s", (account_id,))
        summary_count = cursor.fetchone()[0]

        if summary_count > 0:
            # Summary exists, modify the existing record
            cursor.execute("""
                UPDATE summary
                SET total_asset = %s, total_cash = %s, margin_ratio = %s
                WHERE account_id = %s
            """, (total_asset, total_cash, margin_ratio, account_id))
        else:
            # Summary does not exist, add a new record
            cursor.execute("""
                INSERT INTO summary (account_id, total_asset, total_cash, margin_ratio)
                VALUES (%s, %s, %s, %s)
            """, (account_id, total_asset, total_cash, margin_ratio))

        # Commit the changes to the database
        conn.commit()

        # Return success
        return True

    except Exception as e:
        # Handle any exceptions, print or log the error
        print(f"Error: {e}")
        # Rollback changes in case of an error
        conn.rollback()
        # Return failure
        return False

    finally:
        # Close the cursor
        cursor.close()


def add_or_modify_a_stock(conn, account_id, data):
    cursor = conn.cursor()

    try:
        # Extract data from the object
        symbol = data.get('symbol')
        owning_price = data.get('owning_price')
        t0_volume = data.get('t0_volume', 0)
        t1_volume = data.get('t1_volume', 0)
        t2_volume = data.get('t2_volume', 0)
        other_volume = data.get('other_volume', 0)
        having_volume = data.get('having_volume', 0)
        reward_volume = data.get('reward_volume', 0)
        FS_volume = data.get('FS_volume', 0)
        Outroom_volume = data.get('Outroom_volume', 0)

        # Calculate total_volume and can_sell_volume
        total_volume = t0_volume + t1_volume + t2_volume + other_volume + having_volume + reward_volume + FS_volume + Outroom_volume
        can_sell_volume = total_volume - having_volume

        # Check if the stock exists for the given account_id and symbol
        cursor.execute("""
            SELECT COUNT(*) 
            FROM portfolio 
            WHERE account_id = %s AND stock_symbol = %s
        """, (account_id, symbol))
        stock_count = cursor.fetchone()[0]

        if stock_count > 0:
            # Stock exists, modify the existing record
            cursor.execute("""
                UPDATE portfolio
                SET owning_price = %s,
                    t0_volume = %s, t1_volume = %s, t2_volume = %s,
                    other_volume = %s, having_volume = %s,
                    reward_volume = %s, FS_volume = %s, Outroom_volume = %s,
                    total_volume = %s, can_sell_volume = %s
                WHERE account_id = %s AND stock_symbol = %s
            """, (owning_price, t0_volume, t1_volume, t2_volume, other_volume, having_volume, reward_volume, FS_volume, Outroom_volume, total_volume, can_sell_volume, account_id, symbol))
        else:
            # Stock does not exist, add a new record
            cursor.execute("""
                INSERT INTO portfolio (account_id, stock_symbol, owning_price,
                                       t0_volume, t1_volume, t2_volume, other_volume, having_volume,
                                       reward_volume, FS_volume, Outroom_volume,
                                       total_volume, can_sell_volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (account_id, symbol, owning_price,
                  t0_volume, t1_volume, t2_volume, other_volume, having_volume,
                  reward_volume, FS_volume, Outroom_volume,
                  total_volume, can_sell_volume))

        # Commit the changes to the database
        conn.commit()

        # Return success
        return True

    except Exception as e:
        # Handle any exceptions, print or log the error
        print(f"Error: {e}")
        # Rollback changes in case of an error
        conn.rollback()
        # Return failure
        return False

    finally:
        # Close the cursor
        cursor.close()


def delete_a_stock(conn, account_id, symbol):
    cursor = conn.cursor()

    try:
        # Check if the stock exists for the given account_id and symbol
        cursor.execute("""
            SELECT COUNT(*)
            FROM portfolio
            WHERE account_id = %s AND stock_symbol = %s
        """, (account_id, symbol))
        stock_count = cursor.fetchone()[0]

        if stock_count > 0:
            # Stock exists, delete the record
            cursor.execute("""
                DELETE FROM portfolio
                WHERE account_id = %s AND stock_symbol = %s
            """, (account_id, symbol))

            # Commit the changes to the database
            conn.commit()

            # Return success
            return True
        else:
            # Stock does not exist
            print(f"Stock with symbol {symbol} does not exist for account_id {account_id}")
            return False

    except Exception as e:
        # Handle any exceptions, print or log the error
        print(f"Error in delete_a_stock: {e}")
        # Rollback changes in case of an error
        conn.rollback()
        # Return failure
        return False

    finally:
        # Close the cursor
        cursor.close()


def delete_all_stocks_for_account(conn, account_id):
    cursor = conn.cursor()

    try:
        # Check if the account exists
        cursor.execute("SELECT COUNT(*) FROM accounts WHERE account_id = %s", (account_id,))
        account_count = cursor.fetchone()[0]

        if account_count > 0:
            # Account exists, delete all stocks for the account_id
            cursor.execute("DELETE FROM portfolio WHERE account_id = %s", (account_id,))

            # Commit the changes to the database
            conn.commit()

            # Return success
            return True
        else:
            # Account does not exist
            print(f"Account with account_id {account_id} does not exist.")
            return False

    except Exception as e:
        # Handle any exceptions, print or log the error
        print(f"Error in delete_all_stocks_for_account: {e}")
        # Rollback changes in case of an error
        conn.rollback()
        # Return failure
        return False

    finally:
        # Close the cursor
        cursor.close()


def get_all_stocks_for_account(conn, account_id):
    cursor = conn.cursor()

    try:
        # Check if the account exists
        cursor.execute("SELECT COUNT(*) FROM accounts WHERE account_id = %s", (account_id,))
        account_count = cursor.fetchone()[0]

        if account_count > 0:
            # Account exists, fetch all stocks for the account_id
            cursor.execute("""
                SELECT stock_symbol, owning_price,
                       t0_volume, t1_volume, t2_volume, other_volume,
                       having_volume, reward_volume, FS_volume, Outroom_volume,
                       total_volume, can_sell_volume
                FROM portfolio
                WHERE account_id = %s
            """, (account_id,))
            
            # Fetch all rows
            stocks = cursor.fetchall()

            # Convert the result to a list of dictionaries with appropriate types
            stocks_list = [
                {
                    'stock_symbol': row[0],
                    'owning_price': float(row[1]),
                    't0_volume': row[2],
                    't1_volume': row[3],
                    't2_volume': row[4],
                    'other_volume': row[5],
                    'having_volume': row[6],
                    'reward_volume': row[7],
                    'FS_volume': row[8],
                    'Outroom_volume': row[9],
                    'total_volume': row[10],
                    'can_sell_volume': row[11]
                }
                for row in stocks
            ]

            # Return the array of stocks
            return stocks_list

        else:
            # Account does not exist
            print(f"Account with account_id {account_id} does not exist.")
            return []

    except Exception as e:
        # Handle any exceptions, print or log the error
        print(f"Error in get_all_stocks_for_account: {e}")
        # Return an empty list in case of an error
        return []

    finally:
        # Close the cursor
        cursor.close()


