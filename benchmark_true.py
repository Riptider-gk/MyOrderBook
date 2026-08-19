
from orderbook import OrderBook
from order import Order
import random
import time

import os
if os.path.exists("orderbook.db"):
    os.remove("orderbook.db")

book = OrderBook(persist=True)



order_list = list()

for i in range(1000):
    side = random.choice(["buy", "sell"])
    price = random.randint(95, 105)
    quantity = random.randint(1, 100)
    order = Order(id=i, side=side, price=price, quantity=quantity, timestamp=time.time())
    order_list.append(order)

start_time=time.perf_counter()

for order in order_list:
    book.add_order(order)

end_time=time.perf_counter()
execution_time=end_time-start_time
print(f"persist=TRUE Execution time: {execution_time:.6f} seconds, throughput: {1000/execution_time:.2f} orders/second, latency: {execution_time/1000*1000000:.6f} μs/order")

if os.path.exists("orderbook.db"):
    os.remove("orderbook.db")
    
book = OrderBook(persist=False)

start_time=time.perf_counter()

for order in order_list:
    book.add_order(order)

end_time=time.perf_counter()
execution_time=end_time-start_time
print(f"Persist=FALSE Execution time: {execution_time:.6f} seconds, throughput: {1000/execution_time:.2f} orders/second, latency: {execution_time/1000*1000000:.6f} μs/order")