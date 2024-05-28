import requests
import os
from typing import Literal

otype_map = {
    "upstox": {
        "MK": "MARKET",
        "LT": "LIMIT",
        "SL": "SL",
        "SM": "SL-M",
    },
    "angelone": {
        "MK": "MARKET",
        "LT": "LIMIT",
        "SL": "STOPLOSS_LIMIT",
        "SM": "SL-STOPLOSS_MARKET",
    },
}


class UniversalTradingClient:
    def __init__(self, broker, auto_creds=True):
        self.broker = broker

        # Set broker-specific URLs | AUTO DETECT credentials for api
        if broker == 'angelone':
            self.base_url = 'https://apiconnect.angelbroking.com'
            if auto_creds:
                self.access_token = os.environ.get('ANGELONE_ACCESS_TOKEN')
        elif broker == 'upstox':
            self.base_url = 'https://api.upstox.com/v2'
            if auto_creds:
                self.access_token = os.environ.get('UPSTOX_ACCESS_TOKEN')
        else:
            raise ValueError("Broker not supported")

    def place_order(
        self,
        side: Literal["BUY", "SELL"],
        price: float,
        quantity: int,
        time_in_force: Literal["DAY", "IOC"] = "DAY",
        otype: Literal["MK", "LT", "SL", "SM"] = "MK",
        **kwargs,
    ):
        for x in [side, price, quantity]:
            if x is None:
                raise ValueError("Missing mandatory parameter {}".format(x))

        # typecasting
        price = float(price)

        if self.broker == 'angelone':
            kwargs['price'] = price
            kwargs['quantity'] = quantity
            kwargs['duration'] = time_in_force
            kwargs['ordertype'] = otype_map[self.broker][otype]
            kwargs["transactiontype"] = "BUY" if side == "BUY" else "SELL"
            return self._place_order_angelone(**kwargs)
        elif self.broker == 'upstox':
            kwargs['price'] = price
            kwargs['quantity'] = quantity
            kwargs['validity'] = time_in_force
            kwargs['order_type'] = otype_map[self.broker][otype]
            kwargs["transaction_type"] = "BUY" if side == "BUY" else "SELL"
            return self._place_order_upstox(**kwargs)

    def _place_order_angelone(self, **kwargs):
        url = f"{self.base_url}/rest/secure/angelbroking/order/v1/placeOrder"
        payload = {
            "variety": kwargs.get("variety", "NORMAL"),
            "tradingsymbol": kwargs["tradingsymbol"],
            "symboltoken": kwargs["symboltoken"],
            "transactiontype": kwargs["transactiontype"],
            "exchange": kwargs["exchange"],
            "ordertype": kwargs.get("ordertype", "LIMIT"),
            "producttype": kwargs["producttype"],
            "duration": kwargs["duration"],
            "price": kwargs.get("price", 0),
            "triggerprice": kwargs.get("triggerprice", 0),
            "quantity": kwargs["quantity"],
        }
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-ClientLocalIP': '192.168.1.1',
            'X-ClientPublicIP': '192.168.1.1',
            'X-MACAddress': '00:00:00:00:00:00',
            'X-PrivateKey': self.api_key,
            'Content-Type': 'application/json',
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def _place_order_upstox(self, **kwargs):
        url = f"{self.base_url}/order/place"
        payload = {
            "quantity": kwargs["quantity"],
            "product": kwargs["product"],
            "validity": kwargs["validity"],
            "price": kwargs["price"],
            "tag": kwargs.get("tag", ""),
            "instrument_token": kwargs["instrument_token"],
            "order_type": kwargs["order_type"],
            "transaction_type": kwargs["transaction_type"],
            "disclosed_quantity": kwargs.get("disclosed_quantity", 0),
            "trigger_price": kwargs.get("trigger_price", 0),
            "is_amo": kwargs.get("is_amo", False),
        }
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def get_holdings(self):
        """https://apiconnect.angelbroking.com/rest/secure/angelbroking/portfolio/v1/getAllHolding"""
        if self.broker == 'angelone':
            url = f"{self.base_url}/rest/secure/angelbroking/portfolio/v1/getAllHolding"
            return requests.get(
                url, headers={'Authorization': f'Bearer {self.access_token}', "Accept": "application/json"}
            ).json()
        elif self.broker == 'upstox':
            return requests.get(
                "https://api.upstox.com/v2/portfolio/long-term-holdings",
                headers={'Authorization': f'Bearer {self.access_token}', "Accept": "application/json"},
                data={},
            ).json()
