import abc


class ParserBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def build_transaction(self, tx_data):
        '''Build Transaction object from data.'''
        pass
