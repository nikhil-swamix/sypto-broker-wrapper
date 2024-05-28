from vendors import UniversalTradingClient

if __name__ == '__main__':

    # Initialize client for AngelOne
    client_a = UniversalTradingClient(broker='angelone')
    client_u = UniversalTradingClient(broker='upstox')
    
    # BUY/SELL orders
    angel_order = {
        "producttype": "INTRADAY",
        "variety": "NORMAL",
        "tradingsymbol": "SBIN-EQ",
        "symboltoken": "3045",
        "exchange": "NSE",
    }
    print(client_a.place_order("BUY", price=96, quantity=20, kwargs=angel_order))  # Buy
    print(client_a.place_order("SELL", price=100, quantity=20, kwargs=angel_order))  # Sell

    upstox_order = {
        "product": "D",
        "instrument_token": "NSE_EQ|INE669E01016",
        "order_type": "MARKET",
        "transaction_type": "BUY",
    }
    print(client_u.place_order("BUY", price=96, quantity=20, kwargs=upstox_order))
    print(client_u.place_order("SELL", price=100, quantity=20, kwargs=upstox_order))

    # HOLDINGS
    print(client_u.get_holdings())
    print(client_a.get_holdings())
