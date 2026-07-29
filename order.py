from dataclasses import dataclass
from typing import Literal


@dataclass
class Order:
    id: int
    side: str
    price: int
    quantity: int
    timestamp: float

class Trade:
    def __init__(self, buy_order_id: int, sell_order_id: int, quantity: int, price: int, timestamp: float):
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
            