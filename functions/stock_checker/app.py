from random import randint

def lambda_handler(event, context):
    stock_price = randint(0, 100)
    return {"stock_price": stock_price}
