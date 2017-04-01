### List to dict ###
# list1 = [
#     ["OpenX", "Date1",125,10],
#     ["OpenX", "Date2",150,15],
#     ["OpenX", "Date3",175,20],
#     ["OpenX", "Date4",200,30]
# ]
# def something(list1):
#     dict1 = {}
#     for i in range(len(list1)):
#         for ii in range(len(list1[i])):
#             if list1[i][0] == "OpenX":
#                 temp_dict = {
#                     list1[i][1]:{
#                         "IMPs":list1[i][2],
#                         "Rev":list1[i][3]
#                     }
#                 }
#                 dict1.update(temp_dict)
#     return dict1
#
# print something(list1)

#----------------------------------------------------------------

from datetime import date, timedelta
import json

OpenX = [
    ["OpenX", "Date1",125,10],
    ["OpenX", "Date2",150,15],
    ["OpenX", "Date3",175,20],
    ["OpenX", "Date4",200,30]
]

x = json.dumps(OpenX)
y = json.loads(x)

'2017-04-01 00:00:00'

x = date.today() - timedelta(5)

print x.strftime("%Y-%m-%d %H:%M:%S")

