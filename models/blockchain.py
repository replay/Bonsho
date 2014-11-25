import abc
import calendar
import time
import six


@six.add_metaclass(abc.ABCMeta)
class Serializer:

    @abc.abstractproperty
    def serializing_properties(self):
        pass

    def _get_value(self, type, obj):
        if type == 'number':
            return int(obj)
        elif type == 'string':
            return str(obj)
        elif type == 'object':
            return obj.as_dict()

    def as_dict(self):
        dict_properties = {}
        for name, specs in six.iteritems(self.serializing_properties):
            if specs['type'] in ['number', 'string', 'object']:
                dict_properties[name] = self._get_value(
                    specs['type'],
                    getattr(
                        self,
                        name))
            elif specs['type'] == 'array':
                tmp_list = []
                for element in getattr(self, name):
                    tmp_list.append(
                        self._get_value(
                            specs['elements']['type'],
                            element))
                    dict_properties[name] = tmp_list
        return dict_properties

    @classmethod
    def _create_value(cls, specs, data):
        if specs['type'] == 'number':
            return int(data)
        if specs['type'] == 'string':
            return str(data)
        if specs['type'] == 'object':
            return specs['class'].from_dict(data)

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        for name, specs in six.iteritems(cls.serializing_properties):
            if specs['type'] in ['number', 'string', 'object']:
                setattr(obj, name, cls._create_value(specs, data[name]))
            elif specs['type'] == 'array':
                tmp_list = []
                for val in data[name]:
                    tmp_list.append(cls._create_value(specs['elements'], val))
                    setattr(obj, name, tmp_list)
        return obj


class Block:

    @property
    def age(self):
        return calendar.timegm(time.gmtime()) - self.time

    def __init__(self, **kwargs):
        self.populate(**kwargs)

    def populate(self, **kwargs):
        self.prev_block = kwargs['prev_block']
        self.transactions = kwargs['transactions']
        self.time = kwargs['time']


class BTCTransactionAddress(Serializer):

    serializing_properties = {
        'address': {'type': 'string'}}

    def __init__(self, address=None):
        self.address = address


class BTCTransactionInput(Serializer):

    serializing_properties = {
        'addresses': {
            'type': 'array',
            'elements': {
                'type': 'object',
                'class': BTCTransactionAddress}},
        'value': {
            'type': 'number'}}

    def __init__(self, addresses=None, value=None):
        self.addresses = addresses
        self.value = value


class BTCTransactionInputs(Serializer):

    serializing_properties = {
        'inputs': {
            'type': 'array',
            'elements': {
                'type': 'object',
                'class': BTCTransactionInput}}}

    def __init__(self, inputs=None):
        self.inputs = inputs


class BTCTransactionOutput(Serializer):

    serializing_properties = {
        'addresses': {
            'type': 'array',
            'elements': {
                'type': 'object',
                'class': BTCTransactionAddress}},
        'value': {
            'type': 'number'}}

    def __init__(self, addresses=None, value=None):
        self.addresses = addresses
        self.value = value


class BTCTransactionOutputs(Serializer):

    serializing_properties = {
        'outputs': {
            'type': 'array',
            'elements': {
                'type': 'object',
                'class': BTCTransactionOutput}}}

    def __init__(self, outputs=None):
        self.outputs = outputs


class BTCTransaction(Serializer):

    serializing_properties = {
        'outputs': {
            'type': 'object',
            'class': BTCTransactionOutputs},
        'inputs': {
            'type': 'object',
            'class': BTCTransactionInputs},
        'hash': {
            'type': 'string'}}

    def __init__(self, outputs=None, inputs=None, hash=None):
        self.outputs = outputs
        self.inputs = inputs
        self.hash = hash
