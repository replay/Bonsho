import datetime
import pytz


class Utils:

    @classmethod
    def utc_ts_to_str(self, ts, format):
        dt = datetime.datetime.fromtimestamp(ts, tz=pytz.utc)
        return dt.strftime(format)

    @classmethod
    def utc_str_to_ts(self, str, format):
        dt = datetime.datetime.strptime(str, format).replace(tzinfo=pytz.utc)
        return dt.timestamp()
