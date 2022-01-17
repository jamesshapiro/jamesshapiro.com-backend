from datetime import datetime
from random import randint
from uuid import uuid4

def lambda_handler(event, context):
    stock_price = event["stock_price"]
    transaction_result = {
        "id": str(uuid4()),
        "price": str(stock_price),
        "type": "buy",
        "qty": str(randint(1, 10)),
        "timestamp": datetime.now().isoformat(),
    }
    return transaction_result
