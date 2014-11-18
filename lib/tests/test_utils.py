import unittest
from lib import utils


class UtilsTest(unittest.TestCase):

    def test_ts_str_time_conversion(self):
        ts1 = 3600
        format = '%Y-%m-%dT%H:%M:%SZ'
        str1 = utils.Utils.utc_ts_to_str(ts1, format)
        self.assertEqual(
            ts1,
            utils.Utils.utc_str_to_ts(str1, format))
