from decorator import decorator
import logging
from lxml import etree
from pprint import pformat

from core import make_request
from models import Item, Order, PurchaseContract, Settings
import settings

__all__ = 'create_purchase_contract get_purchase_contract'.split()
logger = logging.getLogger(__name__)

@decorator
def override_settings(f, *args, **kwargs):
    arg_index = f.__code__.co_varnames.index('settings')

    new_settings = Settings().to_dict()
    if 'settings' in kwargs:
        new_settings.update(kwargs['settings'])
        del kwargs['settings']

    if len(args) < arg_index + 1:
        kwargs['settings'] = new_settings
    else: # need to place it in args
        args = list(args)
        args[arg_index] = new_settings
        args = tuple(args)

  # print args, kwargs
    return f(*args, **kwargs)    

@override_settings
def set_purchase_items(contract_id, order, settings={}):
    params = {
        'PurchaseContractId': contract_id,
    }
    assert len(order.items) <= 50
    for i, item in enumerate(order.items):
        key = lambda k: unicode('PurchaseItems.PurchaseItem.' + str(i+1) + '.' + str(k))

        params[key('MerchantId')] = settings['merchant-id']

        item_dict = item.as_dict()
        logger.warn('item {0}: {1}'.format(i, pformat(item_dict)))
        for k, v in item_dict.iteritems():
            params[key(k)] = unicode(v)

    logger.warn('params = {0}'.format(pformat(params)))

@override_settings
def set_contract_charges(contract_id, order, tax=0, shipping=0, promotions=[]):
    pass

@override_settings
def complete_purchase_contract(contract_id):
    pass
