from student_bot import StudentBot, Side, OrderRequest, OrderBook
from IPython.display import clear_output

# Addresses for the test and real exchange
TEST_EXCHANGE = "https://test-cmi-exchange.imclaunchpad.com"
REAL_EXCHANGE = "https://cmi-exchange.imclaunchpad.com"

USERNAME = ""  # TODO: Change to your username
PASSWORD = ""    # TODO: Change to your password
EXCHANGE = TEST_EXCHANGE  # Change to REAL_EXCHANGE when ready

# Flags for printing
print_feed_top = True
print_positions = True

class YourBot(StudentBot):
    def on_orderbooks(self, orderbooks: dict[str, OrderBook]):
        clear_output(wait=True)

        components = ["LETTUCE", "BUN", "CHICKEN"]

        # Ensure BURGER is in the orderbooks
        if "BURGER" not in orderbooks:
            print("⚠️ BURGER orderbook missing, skipping this cycle.")
            return

        # Check if all component products are present
        missing_components = [p for p in components if p not in orderbooks]
        if missing_components:
            print(f"⚠️ Missing components in orderbook: {missing_components}, skipping this cycle.")
            return

        # Get best asks (lowest sell price) and best bids (highest buy price) safely
        component_best_asks = {}
        component_best_bids = {}

        for product in components:
            book = orderbooks[product]
            if not book.sell_orders or not book.buy_orders:
                print(f"⚠️ No sell or buy orders for {product}, skipping this cycle.")
                return
            component_best_asks[product] = book.sell_orders[0].price
            component_best_bids[product] = book.buy_orders[0].price

        component_ask_total = sum(component_best_asks.values())
        component_bid_total = sum(component_best_bids.values())

        burger_book = orderbooks["BURGER"]
        if not burger_book.sell_orders or not burger_book.buy_orders:
            print("⚠️ No sell or buy orders for BURGER, skipping this cycle.")
            return

        burger_best_ask = burger_book.sell_orders[0].price
        burger_best_bid = burger_book.buy_orders[0].price

        # Debug print
        print("Component best asks:", component_best_asks)
        print("Component best bids:", component_best_bids)
        print("BURGER best ask:", burger_best_ask, "| best bid:", burger_best_bid)
        print("Component ask total:", component_ask_total)
        print("Component bid total:", component_bid_total)

        # Arbitrage: Buy components -> sell BURGER
        if component_ask_total < burger_best_bid:
            profit = burger_best_bid - component_ask_total
            print(f"💰 Arbitrage Opportunity! Profit per unit: {profit}")

            # BUY each component
            for product in components:
                best_ask = component_best_asks[product]
                self.hit(OrderRequest(product=product, price=best_ask, side=Side.BUY, volume=1))
                print(f"Placed BUY (IOC) order for 1 {product} at {best_ask}")

            # SELL BURGER
            self.hit(OrderRequest(product="BURGER", price=burger_best_bid, side=Side.SELL, volume=1))
            print(f"Placed SELL (IOC) order for 1 BURGER at {burger_best_bid}")

        # Reverse Arbitrage: Buy BURGER -> sell components
        elif burger_best_ask < component_bid_total:
            profit = component_bid_total - burger_best_ask
            print(f"💰 Reverse Arbitrage! Profit per unit: {profit}")

            # BUY BURGER
            self.hit(OrderRequest(product="BURGER", price=burger_best_ask, side=Side.BUY, volume=1))
            print(f"Placed BUY (IOC) order for 1 BURGER at {burger_best_ask}")

            # SELL each component
            for product in components:
                best_bid = component_best_bids[product]
                self.hit(OrderRequest(product=product, price=best_bid, side=Side.SELL, volume=1))
                print(f"Placed SELL (IOC) order for 1 {product} at {best_bid}")
        else:
            print("No arbitrage opportunity this cycle.")

        # Optionally print positions
        if print_positions:
            positions = self.get_positions()
            print("Current Positions:", positions)

