# import pprint
# import random
# import time
#
# from backend.api.common.getting_free_id import GetFreeId
#
# ids = []
# min_value = 0
# ids.extend([i for i in range(10, 15, 2)])
# ids.extend([i for i in range(20, 35, 1)])
# ids.extend([i for i in range(40, 69, 3)])
# ids.extend([i for i in range(80, 92, 1)])
# ids.extend([i for i in range(5022, 5050, 3)])
# ids.extend([i for i in range(7000, 10124, 4)])
# ids.extend([i for i in range(13011, 14124, 1)])
# ids.extend([i for i in range(14125, 15000, 1)])
# ids.extend([i for i in range(15110, 20001, 2)])


# ids.extend([i for i in range(1, 15, 2)])
# ids.extend([i for i in range(13011, 14124, 1)])
# ids.extend([i for i in range(20, 35, 1)])
# ids.extend([i for i in range(15110, 20001, 2)])
# ids.extend([i for i in range(7000, 10124, 4)])
# ids.extend([i for i in range(5022, 5050, 3)])
# ids.extend([i for i in range(14125, 15000, 1)])
# ids.extend([i for i in range(40, 69, 3)])

##############################
# value = 20
# # c = len(ids)//2 + 1
#
# left = 0
# right = len(ids)-1
#
# while left+1 < right:
#     c = (right + left) // 2
#     if ids[c] == value:
#         print('Find', value)
#         break
#     elif value < ids[c]:
#         right = c
#     else:
#         left = c
#
#     # print(left, right, c)
#
# print(left, right)
# print(ids[left], ids[right])
# print(len(ids), c)
# print(ids[c])
###################################


#########################################

###########################################
# free_ids = [0]

# start = time.perf_counter()
# ids = sorted(ids)
# length = ids[-1] - len(ids) -ids[0]+1
# print(ids[-1], len(ids))
# print(length)
# free_ids = [0]*length
# i = 0
# j = 0
# min_val = ids[0]
# max_val = ids[1]
# while i+1 < len(ids) and ids[i] < max_val:
#
#     if min_val + 1 < max_val:
#         min_val += 1
#         # free_ids.append(min_val)
#         free_ids[j] = min_val
#         j += 1
#
#     if min_val + 1 == max_val:
#
#         i += 1
#         if i+1 < len(ids):
#             min_val = ids[i]
#             max_val = ids[i + 1]
# ###############################
#
# end = time.perf_counter()
# print(f'Time of work: {(end - start):.6f}s')

# class A:
#     def __init__(self, a, b, c, d=None):
#         self.a_param = a
#         self.b_param = b
#         self.c_param = c
#         self.d_param = d
#
# a = A(1, 2, 2)
#
# keys = set(a.__dict__.keys())
# print(keys)
#
# row = 'asdasd asdasd a_param'
# for key in keys:
#     if key in row:
#         print(key)
#
# row_split = set(row.split(' '))
# fields = dict((row_split & keys))
# fields['a_param'] = 'das'

#
# l = []
#
# g1 = GetFreeId()
# id1 = g1.get_free_spaces(l)
# print(id1)
# l.append(id1)
#
# print(l)
#
# g2 = GetFreeId()
# id2 = g2.get_free_spaces(l)
# print(id2)
# l.append(id2)

# list_test = [
#     {
#         'key': i,
#         'text1': 'gggggg'*100,
#         'text2': 'gggggg'*100,
#         'text3': 'gggggg'*100,
#         'text4': 'gggggg'*100,
#         'text5': 'gggggg'*100,
#         'text6': 'gggggg'*100,
#         'text7': 'gggggg'*100,
#         'text8': 'gggggg'*100,
#         'text9': 'gggggg'*100,
#         'text10': 'gggggg'*100,
#         'text11': 'gggggg'*100,
#         'text12': 'gggggg'*100,
#         'text13': 'gggggg'*100,
#         'text14': 'gggggg'*100,
#         'text15': 'gggggg'*100,
#         'text16': 'gggggg'*100,
#         'text17': 'gggggg'*100,
#         'text18': 'gggggg'*100,
#         'text19': 'gggggg'*100,
#     } for i in range(1, 10000)
# ]
#
# print(len(list_test))
# from marshmallow import Schema, fields, post_load
#
#
# class UserSchema(Schema):
#     name = fields.Str()
#     slug = fields.Str()
#
#     @post_load
#     def slugify_name(self, in_data, **kwargs):
#         print(in_data)
#         # in_data["slug"] = in_data["slug"].lower().strip().replace(" ", "-")
#         for key, value in in_data.items():
#             in_data[key] = value if type(value) == list else [value]
#         return in_data
#
#
# schema = UserSchema()
# result = schema.load({"name": "Steve", "slug": "Steve Loria "})
# print(result)