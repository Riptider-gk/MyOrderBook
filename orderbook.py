
import heapq
import itertools
import order as order_module
import db


class OrderBook:
    def __init__(self, persist=True):
        self.bids=[]
        self.asks=[]
        self.trades=[]
        self._counter=itertools.count()
        self.persist=persist

    def add_bid(self,  price,  quantity, id):
        heapq.heappush(self.bids, (-price, quantity, id))

    def add_ask(self, price, quantity, id):
        heapq.heappush(self.asks, (price, quantity, id))

    def add_order(self, order):
            if(self.persist):
                db.log_order(order)
            
            if order.side == "buy":
                
                while(order.quantity>0 and len(self.asks)>0 and order.price>=self.asks[0][0]):
                    ask=heapq.heappop(self.asks)
                    trade_qty=min(order.quantity, ask[1])
                    
                    
                    self.trades.append((order.id,ask[2], trade_qty, ask[0]))
                    if(self.persist):
                        db.log_trade(order_module.Trade(buy_order_id=order.id, sell_order_id=ask[2], quantity=trade_qty, price=ask[0], timestamp=order.timestamp))
                    order.quantity-=trade_qty
                    #ask[1]-=trade_qty
                    if(self.persist):
                        db.update_remaining_quantity(order.id, order.quantity)
                    if (ask[1]-trade_qty>0):
                        self.add_ask(ask[0], ask[1]-trade_qty, ask[2])
                        if(self.persist):
                            db.update_remaining_quantity(ask[2], ask[1]-trade_qty)
                if(order.quantity>0):
                    #order.price=-order.price
                    #heapq.heappush(self.bids, next(self.counter), order)
                    self.add_bid(order.price, order.quantity, order.id)
                    
                
            else: #SELL branch
                
                while(order.quantity>0 and len(self.bids)>0 and order.price<=-self.bids[0][0]):
                    bid=heapq.heappop(self.bids)
                    trade_qty=min(order.quantity, bid[1]) 
                    #db.log_order(order)

                    self.trades.append(( bid[2],order.id, trade_qty, -bid[0]))
                    if(self.persist):
                        db.log_trade(order_module.Trade(buy_order_id=bid[2], sell_order_id=order.id, quantity=trade_qty, price=-bid[0], timestamp=order.timestamp))
                    order.quantity-=trade_qty
                    #bid[1]-=trade_qty
                    if(self.persist):
                        db.update_remaining_quantity(order.id, order.quantity)
                    if (bid[1]-trade_qty>0):
                        if(self.persist):
                            db.update_remaining_quantity(bid[2], bid[1]-trade_qty)
                        self.add_bid(-bid[0], bid[1]-trade_qty, bid[2])
                if(order.quantity>0):
                    #heapq.heappush(self.asks, next(self.counter), order)
                    self.add_ask(order.price, order.quantity, order.id)
                
    
        

    
