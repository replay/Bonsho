import threading
import itertools
from lib import queue_filter_base
from lib import redis_client


class AddressFilter(queue_filter_base.QueueFilterBase):
    __shared_state = {}
    __initialized = False

    def __init__(self, *args, **kwargs):
        self.__dict__ = self.__shared_state
        if self.__initialized:
            return
        self.__initialized = True
        super(AddressFilter, self).__init__(*args, **kwargs)
        self.redis = redis_client.RedisClient()
        self.addresses_lock = threading.Lock()
        self.search_addresses = set()

    def _extract_output_addresses(self, transaction):
        address_lists = [
            output.addresses
            for output in transaction.outputs.outputs]
        addresses = set([
            transaction_address.address
            for transaction_address in itertools.chain(*address_lists)])
        return addresses

    def _lock(self):
        self.addresses_lock.acquire(blocking=True)

    def _unlock(self):
        self.addresses_lock.release()

    def process_q_msg(self, transaction):
        out_addresses = self._extract_output_addresses(transaction)
        self._lock()
        if 'all' in self.search_addresses:
            intersection = 1
        else:
            intersection = len(out_addresses & self.search_addresses)
        self._unlock()
        if intersection:
            return transaction

    def add_address(self, address):
        self._lock()
        self.search_addresses.add(address)
        self._unlock()

    def del_address(self, address):
        self._lock()
        self.search_addresses.remove(address)
        self._unlock()

    def shutdown(self):
        # we need to reset the shared state because threads can only be
        # started once
        self.__initialized = False
        self.__shared_state = {}
        super(AddressFilter, self).shutdown()
