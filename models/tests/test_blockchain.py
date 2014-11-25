import unittest
import python_jsonschema_objects as pjs
from models import blockchain


test_data = {
  'hash': 'mytesthash123',
  'outputs': {
    'outputs': [{
      'addresses': [{
        'address': 'myaddress1'}],
        'value': 123}]},
  'inputs': {
    'inputs': [{
      'addresses': [{
        'address': 'anotheraddress1'}],
      'value': 321}]} }


class TestModelSchemaMixin(unittest.TestCase):

  def setUp(self):
    pass


  def test_from_and_to_dict(self):
    result = blockchain.BTCTransaction.from_dict(test_data).as_dict()
    self.assertEqual(result, test_data)
