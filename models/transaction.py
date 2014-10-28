

class BTCTransactionAddress:

    def __init__(self, *args, **kwargs):
        self.address = kwargs['address']


class BTCTransactionInput:
    def __init__(self, *args, **kwargs):
        self.addresses = kwargs['addresses']
        self.value = kwargs['value']


class BTCTransactionInputs:

    def __init__(self, *args, **kwargs):
        self.inputs = kwargs['inputs']


class BTCTransactionOutput:

    def __init__(self, *args, **kwargs):
        self.addresses = kwargs['addresses']
        self.value = kwargs['value']


class BTCTransactionOutputs:

    def __init__(self, *args, **kwargs):
        self.outputs = kwargs['outputs']


class BTCTransaction:

    def __init__(self, *args, **kwargs):
        self.outputs = kwargs['outputs']
        self.inputs = kwargs['inputs']
        self.hash = kwargs['hash']
