try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    import json
except ImportError:
    import simplejson as json
import logging

from models import Item, Order, PurchaseContract, Settings

logging.basicConfig(level=logging.DEBUG)

class TestCheckoutByAmazonIntegration(unittest.TestCase):
    def setUp(self):
        self.shop_items = (
            {
                'id': 1234,
                'title': 'Wine Glass',
                'price': 9.99,
            },
            {
                'id': 2345,
                'title': 'Frosted Shot Glasses, set of 4',
                'price': 14.99,
            },
        )
        f = open('secret_settings.json')
        self.settings = Settings(**json.load(f))

    def fill_cart(self):
        self.cart = [self.shop_items[1], self.shop_items[0]]

    def test_whole_checkout_process(self):
        # While browsing, the customer add stuff to the cart
        self.fill_cart()
        # Page 1: initiate checkout and choose address
        contract = PurchaseContract(settings=self.settings.as_dict())
        for item in self.cart:
            contract.order.add_item(Item(id=item['id'], title=item['title'], price=item['price']))
        # Page 2: Choose payment method
        contract.add_destination('#default', 'John Doe', '123 Main St\nApt. B', 'New York', 'NY', 'US', '(123) 456-7890')
        # Page 3: Confirmation
        # Page 4: "Thank You" page
        contract.complete()

if __name__ == '__main__':
    unittest.main()
