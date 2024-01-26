import pprint
import random
import time

ids = []
min_value = 0
ids.extend([i for i in range(10, 15, 2)])
ids.extend([i for i in range(20, 35, 1)])
ids.extend([i for i in range(40, 69, 3)])
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

print(ids)




# free_ids = [0]

start = time.perf_counter()
ids = sorted(ids)
length = ids[-1] - len(ids) -ids[0]+1
print(ids[-1], len(ids))
print(length)
free_ids = [0]*length
i = 0
j = 0
min_val = ids[0]
max_val = ids[1]
while i+1 < len(ids) and ids[i] < max_val:

    if min_val + 1 < max_val:
        min_val += 1
        # free_ids.append(min_val)
        free_ids[j] = min_val
        j += 1

    if min_val + 1 == max_val:

        i += 1
        if i+1 < len(ids):
            min_val = ids[i]
            max_val = ids[i + 1]
###############################

end = time.perf_counter()
print(f'Time of work: {(end - start):.6f}s')

print(free_ids)
print(len(ids), len(free_ids))

print(len(ids + free_ids))
print(len(set(ids + free_ids)))

# print(len(set(free_ids))-1)