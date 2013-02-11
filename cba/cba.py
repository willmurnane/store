from decorator import decorator
from lxml import etree, objectify

class CheckoutCallbackError(Exception):
    pass

class Destination(object):
    def __init__(self, city, state, postal_code, country_code):
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country_code = country_code

class PurchaseContract(object):
    def __init__(self, id, expires, merchant_id, marketplace_id, state, destinations):
        self.id = str(id)
        self.expires = expires
        self.merchant_id = merchant_id
        self.marketplace_id = marketplace_id
        self.state = state
        self.destinations = destinations


