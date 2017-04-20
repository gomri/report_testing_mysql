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

import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')


