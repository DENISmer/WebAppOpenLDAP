from backend.api.redis.redis_storage import RedisStorage

r = RedisStorage()

r.add(1001, 'value1')
r.add(1002, 'value2')
r.add(1003, 'value3')
r.add(1004, 'value4')
print(r.add(1005, 'value5'))
print(r.add(1005, 'value5'))
r.add(1006, 'value6')

print(r.get(1002))
print(r.get(1006))
print(r.delete(1006))
print(r.get(1007))
print(r.get(1010))
print(r.get_redit().keys())
print(r.delete(10213))
print(*r.get_redit().keys())
print(r.delete(*r.get_redit().keys()))
print(r.get_redit().keys())
