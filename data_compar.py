from query import *

def check_24_hours_serving(alist):
    if len(alist) == 24:
        test_result = True
        return test_result
    elif len(alist) != 24:
        test_result = False
        return test_result

check_24_hours_serving(result_24_hour_serving)
