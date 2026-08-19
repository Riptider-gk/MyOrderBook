from orderbook import OrderBook
from order import Order
import time
import threading

def test_partial_fill_accross_price_levels():
    book = OrderBook(persist=False)
    book.add_order(Order(1, "sell", 100, 5, time.time()))
    book.add_order(Order(2, "sell", 101, 5, time.time()))
    book.add_order(Order(3, "buy", 101, 8, time.time()))

    assert len(book.trades) == 2
    assert book.asks[0]==(101,2,2)
    assert len(book.bids)==0

def test_time_priority_tie_breaker():
    book=OrderBook(persist=False)
    book.add_order(Order(1, "sell", 100, 5, time.time()))
    book.add_order(Order(2, "sell", 100, 5, time.time()))  # Later timestamp
    book.add_order(Order(3, "buy", 100, 8, time.time()+1))

    assert len(book.trades) == 2
    assert book.asks[0]==(100,2,2)
    assert len(book.bids)==0

def test_persist_toggle_doesnt_affect_matching_logic():
    import os
    if os.path.exists("orderbook.db"):
        os.remove("orderbook.db")

    orders=[
        Order(1, "sell", 100, 5, time.time()),
        Order(2, "sell", 101, 5, time.time()),
        Order(3, "buy", 101, 8, time.time())
    ]

    book_false=OrderBook(persist=False)
    for o in orders:
        book_false.add_order(o)

    if os.path.exists("orderbook.db"):
            os.remove("orderbook.db")

    orders1=[
            Order(1, "sell", 100, 5, time.time()),
            Order(2, "sell", 101, 5, time.time()),
            Order(3, "buy", 101, 8, time.time())
        ]
    
    book_true=OrderBook(persist=True)
    for o in orders1:
        book_true.add_order(o)

    assert book_false.trades==book_true.trades

def test_concurrent_order_submission():
    book=OrderBook(persist=False)
    errors=[]

    def submit_orders(start_id, side, price):
          try:
               for i in range(50):
                    order=Order(start_id+i, side, price, 1, time.time())
                    book.add_order(order)
          except Exception as e:
               errors.append(e)

    threads=[
            threading.Thread(target=submit_orders, args=(0,"sell", 100)),
            threading.Thread(target=submit_orders, args=(1000,"buy", 100))
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors==[]
            
