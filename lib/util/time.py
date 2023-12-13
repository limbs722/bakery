from datetime import datetime, timedelta
from dateutil.parser import parse
import pytz 

class TimeUtil:

    @staticmethod
    def utcToStr( t, f = '%Y-%m-%dT%H:%M:%S.%fZ'):
        return t.strftime( f )
    
    @staticmethod
    def strToUtc( s ):
        try:
            return parse( s ).astimezone( pytz.utc )
        except:
            raise ValueError("Provided string is not time format")
    
    @staticmethod
    def is_overlapping_or_contained( pivot_beg, pivot_end, check_beg, check_end ):

        return (pivot_beg <= check_beg and check_end <= pivot_end) or \
            (check_beg < pivot_beg and pivot_beg < check_end ) or \
            (check_beg < pivot_end and pivot_end <= check_end )
    
    @staticmethod
    def calculate_date_range_from_offset( offset = 1, tz = 'Asia/Seoul' ):

        b = datetime.now( pytz.timezone(tz) ).replace( hour = 0, minute = 0, second = 0, microsecond = 0)
        e = b + timedelta( days = offset )

        return b, e

    @staticmethod
    def ensure_utc_aware( t ):
        if t.tzinfo is None or t.tzinfo.utcoffset( t ) is None:
            return t.replace( tzinfo = pytz.utc )
        else:
            return t.astimezone( pytz.utc )
        
        


