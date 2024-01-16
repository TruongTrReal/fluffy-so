from mysql_functions import *

# Example usage:
conn = connect_sql()

# ADD OR CREATE ACCOUNT NUMBER 
user_id_to_associate = 1
account_number_to_check = "A12345"
account_id = create_or_get_account(conn, user_id_to_associate, account_number_to_check)
print(account_id)
if account_id:
    print(f"Account with account_number {account_number_to_check} exists or was created. Account ID: {account_id}")
else:
    print(f"Failed to create with account_number {account_number_to_check}")

# ADD OR MODIFY SUMMARY
asset = 2000000000
cash = 500000000
margin_rate = 88.88
test = add_or_modify_summary(conn, account_id, asset, cash, margin_rate)

print(get_account_summary(conn, account_id))
print(test) # true
    
# ADD OR MODIFY A STOCK
stock_data = {
    'symbol': 'VIC',
    'owning_price': 50.00,
    't0_volume': 0,
    't1_volume': 5000,
    't2_volume': 3000,
    'other_volume': 0,
    'having_volume': 8000,
    'reward_volume': 0,
    'FS_volume': 0,
    'Outroom_volume': 0,
}

print(add_or_modify_a_stock(conn, account_id, stock_data)) # true
# print(delete_a_stock(conn, account_id, 'VIC')) # true
# print(delete_all_stocks_for_account(conn, account_id)) # true

# GET ALL STOCK 
print(get_all_stocks_for_account(conn, account_id)) # true

# Close the connection
conn.close()

