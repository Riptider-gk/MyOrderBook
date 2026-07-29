from orderbook import OrderBook
from order import Order
import time
from fastapi import FastAPI
from orderbook import OrderBook
from orderrequest import OrderRequest
import order as order_module
import time, itertools

app=FastAPI()
book=OrderBook()
id_counter=itertools.count(1)

@app.post("/orders")
def submit_order(req: OrderRequest):
    order_id=next(id_counter)
    order=order_module.Order(id=order_id, side=req.side, price=req.price, quantity=req.quantity, timestamp=time.time())
    book.add_order(order)
    return {"message": "Order submitted successfully", "order_id": order_id}

@app.get("/book")
def get_order_book():
    return {
        "best bid": -book.bids[0] if book.bids else None,
        "best ask": book.asks[0] if book.asks else None
    }

book.add_order(Order(1, "sell", 102, 10, time.time()))
book.add_order(Order(2, "sell", 101, 5, time.time()))
book.add_order(Order(3, "buy", 101, 8, time.time()))
print(book.bids)
print(book.asks)
print(book.trades)
