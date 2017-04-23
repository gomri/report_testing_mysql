from query import *
from result_formater import *

def check_24_hours_serving(alist):
    if len(alist) == 24:
        test_result = True
        return test_result
    elif len(alist) != 24:
        test_result = False
        return test_result

serving_24_hours_test_result = check_24_hours_serving(result_24_hour_serving)

print test_result_formater("\n24 Hours exist: ",serving_24_hours_test_result)

