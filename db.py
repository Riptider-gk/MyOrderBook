import sqlite3

conn = sqlite3.connect('orderbook.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS orders 
             (id INTEGER PRIMARY KEY, 
             side TEXT, price INTEGER, 
             quantity INTEGER,
             remaining_quantity INTEGER,
             timestamp FLOAT)''')
c.execute('''CREATE TABLE IF NOT EXISTS trades (
             id INTEGER PRIMARY KEY, 
             buy_order_id INTEGER, 
             sell_order_id INTEGER, 
             quantity INTEGER, 
             price INTEGER,
             timestamp FLOAT)''')


def log_order(order):
    c.execute(
        "INSERT INTO orders (id, side, price, quantity, remaining_quantity, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (order.id, order.side, order.price, order.quantity, order.quantity, order.timestamp)
    )
    conn.commit()


def log_trade(trade):
    c.execute(
        "INSERT INTO trades (buy_order_id, sell_order_id, quantity, price, timestamp) VALUES (?, ?, ?, ?, ?)",
        (trade.buy_order_id, trade.sell_order_id, trade.quantity, trade.price, trade.timestamp)
    )
    conn.commit()

def update_remaining_quantity(order_id, remaining_quantity):
    c.execute(
        "UPDATE orders SET remaining_quantity = ? WHERE id = ?",
        (remaining_quantity, order_id)
    )
    conn.commit()

