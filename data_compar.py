from query import *
from result_formater import *
from Vars import *

def check_24_hours_serving(alist):
    if len(alist) == 24:
        test_result = True
        return test_result
    elif len(alist) != 24:
        test_result = False
        return test_result

def check_delta_last_5_days(num,delta_percent):
    if num < delta_percent:
        return True
    elif num >= delta_percent:
        return False


result_test_delta_rev = check_delta_last_5_days(rev_last_5_days_delta,min_delta)
result_test_delta_imps = check_delta_last_5_days(rev_last_5_days_delta,min_delta)

print result_test_delta_imps
print result_test_delta_rev

if result_test_delta_rev and result_test_delta_imps == True:
    print test_result_formater("\nIMPs and Rev last 4 days delta: ", True)

# serving_24_hours_test_result = check_24_hours_serving(result_24_hour_serving)

# print test_result_formater("\n24 Hours exist: ", serving_24_hours_test_result)