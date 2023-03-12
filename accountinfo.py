import requests
import time
import hmac
import hashlib
import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="accountinfo"
)

mycursor = mydb.cursor()

# Create table for storing account information
mycursor.execute("CREATE TABLE IF NOT EXISTS account_info ("
                 "id INT AUTO_INCREMENT PRIMARY KEY,"
                 "balance_idr DECIMAL(18,8),"
                 "balance_btc DECIMAL(18,8),"
                 "balance_eth DECIMAL(18,8),"
                 "server_time BIGINT,"
                 "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

# Please find Key from trade API Indodax exchange
key = 'AVM50K8H-BZNAQA4J-MWISNK9Y-U5U9RNHA-K0FCP2NL'

# Please find Secret Key from trade API Indodax exchange
secretKey = 'b2bfc38bbd8b416e4443caf5b9cc1e04d98326020c98c518893818d7a26d8ced757e94e7e4e2bceb'

url = 'https://indodax.com/tapi'

data = {
    'method': 'getInfo',
    'timestamp': str(int(time.time() * 1000)),
    'recvWindow': '5000'
}

post_data = '&'.join([f"{k}={v}" for k, v in data.items()])


sign = hmac.new(secretKey.encode(), post_data.encode(), hashlib.sha512).hexdigest()

headers = {
    'Key': key,
    'Sign': sign
}

# Make the POST request
response = requests.post(url, headers=headers, data=data).json()

# Extract the relevant data from the response
account_info = response['return']
balance_idr = account_info['balance']['idr']
balance_btc = account_info['balance']['btc']
balance_eth = account_info['balance']['eth']
server_time = account_info['server_time']

# Insert the data into the database
sql = "INSERT INTO account_info (balance_idr, balance_btc, balance_eth, server_time) VALUES (%s, %s, %s, %s)"
val = (balance_idr, balance_btc, balance_eth, server_time)
mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "record inserted.")
