# zerodha
*Wrapper around kiteconnect*
**Installation**
```
git clone https://github.com/swapniljariwala/zerodha.git
cd zerodha
python setup.py install
```
**Usage**
```python
from kitewrapper import KiteFront
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
auth['txn_password'] = 'PASS2'
k = KiteFront(auth=auth)
h = k.holdings()
```
Limited functionality from [kiteconnect](https://kite.trade/docs/pykiteconnect/) is supported
Supported methods-
* holdings
* margins
* orders
* positions
* trades
* order_place [not tested]
* order_modify [not tested]
* order_cancel [not tested]

**old way** Automation of zerodha for HFT (currently tested with Python2.7)
```python
from broker.module import Zerodha, Order
#question array
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
auth['txn_password'] = 'PASS2'

"""
    MIS- margin intraday square-off, 
    CNC - cash (buy for delivery, sell existing shares)
"""
zerodha = Zerodha(auth, prefs = {'default_product' : 'MIS',})
if zerodha.connect():
  print('Logged in to Zerodha')
else:
  print('Check credentials')
#Will result in 0.0 after market
print('Current price of SBIN {}'.format(zerodha.get_current_price('SBIN')))
#CAUTION- This will actually place orders in your zerodha account
buy_id = zerodha.buy(security="SBIN-EQ",
                                quantity=1,
                                price=230)

sell_id = zerodha.sell(security="SBIN-EQ",
                                quantity = 1,
                                price = 230)

buy_order = zerodha.get_order_info(buy_id)
if buy_order.state == order.State.FILLED:
  print("Buy exectuted")
```

To Do:
- Addition of Test casees
- Support for F&O
- Integration with data vendors
- Integration with a broader library like Zipline to include simulation and several brokers
- Support for Python 3

Please log issues  if you find any.

