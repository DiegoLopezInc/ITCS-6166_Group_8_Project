"""
Competition Scoring Logic
- Tracks P&L, rankings for each bot
"""
class Scoring:
    def __init__(self):
        self.pnl = {}  # trader_id -> P&L
        self.trades = []

    def record_trade(self, trade):
        # trade: {'buy_order_id', 'sell_order_id', 'price', 'qty', 'timestamp'}
        for side, trader_id in [('buy', trade.get('buy_order_id').split('-')[0]), ('sell', trade.get('sell_order_id').split('-')[0])]:
            pnl = self.pnl.get(trader_id, 0)
            if side == 'buy':
                pnl -= trade['price'] * trade['qty']
            else:
                pnl += trade['price'] * trade['qty']
            self.pnl[trader_id] = pnl
        self.trades.append(trade)

    def get_leaderboard(self):
        return sorted(self.pnl.items(), key=lambda x: x[1], reverse=True)
