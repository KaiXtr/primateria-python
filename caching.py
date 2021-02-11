from pymemcache.client import base

key = 'visiting'
client = base.Client(('localhost', 11211))
result = client.get(key)
print(result)

tbl = sqlite3.connect('userdata.db')
com = tbl.cursor()



if result == None:
    result = do_some_query()
    client.set(key, result)
else:
		client.set(key, 'Hello')

print(client.get(key))
tbl.close()