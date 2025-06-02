from student_bot import StudentBot, Side, OrderRequest, OrderBook
from IPython.display import clear_output

# Addresses for the test and real exchange
TEST_EXCHANGE = "https://test-cmi-exchange.imclaunchpad.com"
REAL_EXCHANGE = "https://cmi-exchange.imclaunchpad.com"

USERNAME = ""  # TODO: Change to your username
PASSWORD = ""    # TODO: Change to your password
EXCHANGE = TEST_EXCHANGE  # Change to REAL_EXCHANGE when ready

print_feed_top = True
print_positions = True

class YourBot(StudentBot):
    def on_orderbooks(self, orderbooks: dict[str, OrderBook]):
        clear_output(wait=True)

        # --- Setup ---
        burger_components = ["LETTUCE", "BUN", "CHICKEN"]
        salad_components = ["LETTUCE", "CHICKEN"]

        # Check all required products exist
        for product in burger_components + ["BURGER", "SALAD"]:
            if product not in orderbooks:
                print(f"⚠️ Missing {product} orderbook, skipping this cycle.")
                return

        # --- Helper: Get best ask/bid safely ---
        def get_best_prices(products):
            best_asks = {}
            best_bids = {}
            for p in products:
                book = orderbooks[p]
                if not book.sell_orders or not book.buy_orders:
                    print(f"⚠️ No orders for {p}, skipping this cycle.")
                    return None, None
                best_asks[p] = book.sell_orders[0].price
                best_bids[p] = book.buy_orders[0].price
            return best_asks, best_bids

        # Get burger component prices
        burger_asks, burger_bids = get_best_prices(burger_components)
        if burger_asks is None:
            return

        # Get salad component prices
        salad_asks, salad_bids = get_best_prices(salad_components)
        if salad_asks is None:
            return

        burger_book = orderbooks["BURGER"]
        salad_book = orderbooks["SALAD"]

        if not burger_book.sell_orders or not burger_book.buy_orders:
            print("⚠️ No BURGER orders, skipping.")
            return
        if not salad_book.sell_orders or not salad_book.buy_orders:
            print("⚠️ No SALAD orders, skipping.")
            return

        burger_ask = burger_book.sell_orders[0].price
        burger_bid = burger_book.buy_orders[0].price

        salad_ask = salad_book.sell_orders[0].price
        salad_bid = salad_book.buy_orders[0].price

        burger_ask_total = sum(burger_asks.values())
        burger_bid_total = sum(burger_bids.values())

        salad_ask_total = sum(salad_asks.values())
        salad_bid_total = sum(salad_bids.values())

        print("BURGER component ask total:", burger_ask_total, "| BURGER bid:", burger_bid)
        print("SALAD component ask total:", salad_ask_total, "| SALAD bid:", salad_bid)

        # --- BURGER Arbitrage ---
        if burger_ask_total < burger_bid:
            profit = burger_bid - burger_ask_total
            print(f"🍔 Arbitrage: BUY components -> SELL BURGER | Profit: {profit}")
            for p in burger_components:
                self.hit(OrderRequest(product=p, price=burger_asks[p], side=Side.BUY, volume=1))
            self.hit(OrderRequest(product="BURGER", price=burger_bid, side=Side.SELL, volume=1))

        elif burger_ask < burger_bid_total:
            profit = burger_bid_total - burger_ask
            print(f"🍔 Reverse Arbitrage: BUY BURGER -> SELL components | Profit: {profit}")
            self.hit(OrderRequest(product="BURGER", price=burger_ask, side=Side.BUY, volume=1))
            for p in burger_components:
                self.hit(OrderRequest(product=p, price=burger_bids[p], side=Side.SELL, volume=1))

        # --- SALAD Arbitrage ---
        if salad_ask_total < salad_bid:
            profit = salad_bid - salad_ask_total
            print(f"🥗 Arbitrage: BUY components -> SELL SALAD | Profit: {profit}")
            for p in salad_components:
                self.hit(OrderRequest(product=p, price=salad_asks[p], side=Side.BUY, volume=1))
            self.hit(OrderRequest(product="SALAD", price=salad_bid, side=Side.SELL, volume=1))

        elif salad_ask < salad_bid_total:
            profit = salad_bid_total - salad_ask
            print(f"🥗 Reverse Arbitrage: BUY SALAD -> SELL components | Profit: {profit}")
            self.hit(OrderRequest(product="SALAD", price=salad_ask, side=Side.BUY, volume=1))
            for p in salad_components:
                self.hit(OrderRequest(product=p, price=salad_bids[p], side=Side.SELL, volume=1))

        if print_positions:
            positions = self.get_positions()
            print("📊 Current Positions:", positions)
