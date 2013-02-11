import base64
from collections import OrderedDict
import datetime
import hashlib, hmac
import logging
from lxml import etree, objectify
import requests
import urllib, urlparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

action_details = {
    'CreatePurchaseContract': {
        'params': {
            'PurchaseContractMetadata': False,
            'DirectedId': True,
            'AuthorizationToken': True,
        },
        'response': ['PurchaseContractId'],
    },
    'GetPurchaseContract': {
        'params': {
            'PurchaseContractId': True,
        },
        'response': ['PurchaseContract'],
    },
    'SetPurchaseItems': {
        'params': {
            'PurchaseContractId': True,
        },
    },
    'SetContractCharges': {
        'params': {
            'PurchaseContractId': True,
            'Charges.Tax.Amount': True,
            'Charges.Tax.CurrencyCode': True,
            'Charges.Shipping.Amount': True,
            'Charges.Shipping.CurrencyCode': True,
        },
    },
    'CompletePurchaseContract': {
        'params': {
            'PurchaseContractId': True,
            'IntegratorId': False,
            'IntegratorName': False,
            'InstantOrderProcessingNotificationURLs.MerchantUrl': False,
            'InstantOrderProcessingNotificationURLs.IntegratorURL': False,
        },
        'response': ['OrderIds.OrderId[:]'],
    },
}

def _dotted_getattr(obj, attr):
    left, _, right = attr.partition('.')
    if not right:
        return getattr(obj, right)
    else:
        return _dotted_getattr(getattr(obj, left), right)

def sign_request(method, host, request_uri='/', params={}, settings={}):
    keys = sorted(params.keys())
    sanitize = lambda v: urllib.quote(str(v), '~')
    gen = ((sanitize(key), sanitize(params[key])) for key in sorted(params.keys()))
    gen = ('{0}={1}'.format(k,v) for k,v in gen)
    # cqs means Canonicalized Query String
    cqs = '&'.join(gen)
    to_sign = '\n'.join((method, host.lower(), request_uri, cqs))
    hash = hmac.new(str(settings['secret-access-key']), to_sign, hashlib.sha256)
    return base64.b64encode(hash.digest())

def make_request(method, action, params={}, settings={}):
    if action not in action_details:
        raise ValueError('Invalid action. Choose from {0}'.format(', '.join(action_details.keys())))
    for ap, required in action_details[action]['params'].items():
        if required and ap not in params:
            raise ValueError('Missing required param "{0}"'.format(ap))
    if method not in ('GET', 'POST'):
        raise ValueError('method must be either "GET" or "POST"')
    host = 'payments{sandbox}.amazon.com'.format(sandbox=('-sandbox' if settings['sandbox'] else ''))
    endpoint = 'https://{host}/cba/api/purchasecontract/'.format(host=host)
    timestamp = datetime.datetime.utcnow()

    query = {
        'Action': action,
        'AWSAccessKeyId': settings['public-access-key'],
        'SignatureMethod': 'HmacSHA256',
        'SignatureVersion': 2,
        'Timestamp': timestamp.isoformat(),
        'Version': '2010-08-31',
    }
    query.update(params)

    signature = sign_request(
        method,
        host,
        '/cba/api/purchasecontract/',
        query,
        settings=settings
    )
    query['Signature'] = signature

    query = [(k, v) for k,v in query.iteritems()]
    query.sort()
    query = OrderedDict(query)

    logger.debug('{0} {1} with params={2}'.format(method, query['Action'], query))

    response = requests.request(method, endpoint, params=query)
    root = objectify.fromstring(response.content)
    if root.tag.endswith('ErrorResponse'):
        raise Exception('Bad response from Amazon!\n{0}'.format(etree.tostring(root, pretty_print=True)))
    logger.debug(etree.tostring(root, pretty_print=True))
    try:
        result_element = getattr(root, action + 'Result')
        response_elements = tuple(eval('e.'+response, {}, {'e': result_element}) for response in action_details[action]['response'])
        for i, element in enumerate(response_elements):
            try:
                logger.debug('response_element {0}: {1}'.format(
                    i, etree.tostring(element, pretty_print=True),
                ))
            except TypeError:
                logger.debug('response_element {0}: {1}'.format(
                    i, element,
                ))
    except AttributeError:
        response_elements = []
    request_id = root.ResponseMetadata.RequestId.text
    return response_elements, request_id
