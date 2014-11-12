import abc


class ParserBase:

    def build_transaction(self, tx_data):
        '''Build Transaction object from data.'''
        pass

    @abc.abstractmethod
    def _extract_transaction_data(self, data):
        '''Extract transaction from raw data.'''
        pass
