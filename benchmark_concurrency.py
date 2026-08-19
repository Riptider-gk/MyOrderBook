import threading
import time
from orderbook import OrderBook
from order import Order
import random

book = OrderBook(persist=False)
NUM_THREADS = 4
ORDERS_PER_THREAD = 250

def worker (thread_id):
    for i in range(ORDERS_PER_THREAD):
        side = random.choice(["buy", "sell"])
        price = random.randint(95, 105)
        quantity = random.randint(1, 100)
        order = Order(id=thread_id * ORDERS_PER_THREAD + i, side=side, price=price, quantity=quantity, timestamp=time.time())
        book.add_order(order)

threads=[threading.Thread(target=worker, args=(i,)) for i in range(NUM_THREADS)]

start=time.perf_counter()
for t in threads:
    t.start()
for t in threads:
    t.join()
end=time.perf_counter()

total_orders = NUM_THREADS * ORDERS_PER_THREAD
elapsed_time = end - start
print(f"Concurrent ({NUM_THREADS} threads): {total_orders} orders in {elapsed_time:.6f}s, throughput: {total_orders/elapsed_time:.2f} orders/sec")