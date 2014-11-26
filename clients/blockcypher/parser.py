from clients.base import parser
from utter_libs.models import blockchain
from lib import connection


class BlockCypherParser(parser.ParserBase):
    ws_endpoint_url = 'ws://socket.blockcypher.com/v1/btc/main'
    chain_head_url = 'http://api.blockcypher.com/v1/btc/main'
    block_url = 'https://api.blockcypher.com/v1/btc/main/blocks/{block}'
    endpoint_name = 'Block Cypher'
    ping_msg = '{"event": "ping"}'
    ping_interval = 20
    connection_class = connection.WebsocketsConnection

    @classmethod
    def build_transaction(cls, tx_data):
        return blockchain.BTCTransaction(
            outputs=cls.build_transaction_outputs(tx_data['outputs']),
            inputs=cls.build_transaction_inputs(tx_data['inputs']),
            hash=tx_data['hash'])

    @classmethod
    def extract_block_transactions(cls, block):
        return block['txids']

    @classmethod
    def build_transaction_input(cls, data):
        return blockchain.BTCTransactionInput(
            value=data['output_value'],
            addresses=[
                blockchain.BTCTransactionAddress(
                    address=address)
                for address in data['addresses']])

    @classmethod
    def build_transaction_inputs(cls, data):
        return blockchain.BTCTransactionInputs(
            inputs=[
                cls.build_transaction_input(input)
                for input in data])

    @classmethod
    def build_transaction_output(cls, data):
        return blockchain.BTCTransactionOutput(
            value=data['value'],
            addresses=[
                blockchain.BTCTransactionAddress(
                    address=address)
                for address in data['addresses']])

    @classmethod
    def build_transaction_outputs(cls, data):
        return blockchain.BTCTransactionOutputs(
            outputs=[
                cls.build_transaction_output(output)
                for output in data])
