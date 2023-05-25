from mongoDB import MongoDB

import sys
sys.path.insert(1, r'')

db = MongoDB()
print(db.host)
print(db.port)

db.connect()