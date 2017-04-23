from kitewrapper import KiteFront
from kiteconnect import KiteConnect

q_arr = [
    'question1',
    'question2',
    "question3",
    'question4',
    'question5',
    'question6',
    ]
#answer array
a_arr = [
    "ans1",
    "ans2",
    "ans3",
    "ans4",
    "ans5",
    "ans6"
    ]
auth={k:v for k,v in zip(q_arr,a_arr)}
auth['user_id'] = 'UDI'
auth['password'] = 'PASS1'

# get session parameters 
k_browser = KiteFront(auth=auth)
k_browser.connect()
z = k_browser.zsession()

# Use session parameters with native api
kite = KiteConnect(api_key="kitefront")
kite.set_access_token(z['access_token'])

# Place an order
try:
	order_id = kite.order_place(tradingsymbol="INFY",
					exchange="NSE",
					transaction_type="BUY",
					quantity=1,
					order_type="MARKET",
					product="NRML")

	print("Order placed. ID is", order_id)
except Exception as e:
	print("Order placement failed", e.message)

# Fetch all orders
print(kite.orders())

