import calendar
import time


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


class BTCTransactionAddress:

    def __init__(self, *args, **kwargs):
        self.address = kwargs['address']


class BTCTransactionInput:
    def __init__(self, *args, **kwargs):
        self.addresses = kwargs['addresses']
        self.value = int(kwargs['value'])


class BTCTransactionInputs:

    def __init__(self, *args, **kwargs):
        self.inputs = kwargs['inputs']


class BTCTransactionOutput:

    def __init__(self, *args, **kwargs):
        self.addresses = kwargs['addresses']
        self.value = int(kwargs['value'])


class BTCTransactionOutputs:

    def __init__(self, *args, **kwargs):
        self.outputs = kwargs['outputs']


class BTCTransaction:

    def __init__(self, *args, **kwargs):
        self.outputs = kwargs['outputs']
        self.inputs = kwargs['inputs']
        self.hash = kwargs['hash']
