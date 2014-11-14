from clients.base import parser
from models import blockchain


class Parser(parser.ParserBase):

    @classmethod
    def build_transaction(cls, tx_data):
        return blockchain.BTCTransaction(
            outputs=cls.build_transaction_outputs(tx_data['out']),
            inputs=cls.build_transaction_inputs(tx_data['inputs']),
            hash=tx_data['hash'])

    @classmethod
    def build_transaction_inputs(cls, data):
        return blockchain.BTCTransactionInputs(
            inputs=[
                cls.build_transaction_input(input['prev_out'])
                for input in data
                if 'prev_out' in input])

    @classmethod
    def build_transaction_input(cls, data):
        return blockchain.BTCTransactionInput(
            value=data['value'],
            addresses=[
                blockchain.BTCTransactionAddress(
                    address=data['addr'])])

    @classmethod
    def build_transaction_outputs(cls, data):
        return blockchain.BTCTransactionOutputs(
            outputs=[
                cls.build_transaction_output(output)
                for output in data])

    @classmethod
    def build_transaction_output(cls, data):
        if 'addr' in data:
            address = blockchain.BTCTransactionAddress(address=data['addr'])
        else:
            address = []
        return blockchain.BTCTransactionOutput(
            value=data['value'],
            addresses=[address])
