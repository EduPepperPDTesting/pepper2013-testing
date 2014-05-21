from pymongo import Connection
import gridfs
from gridfs.errors import NoFile

'''
[USAGE]

NEW:
us=MongoUserStore(host='localhost',db='userstore',user=None,password=None)
file_read = open('test.png','rb')
data = file_read.read()
file_read.close()
us.save({"user_id":1,"type":"photo","data": data})

DEL:
us=MongoUserStore(host='localhost',db='userstore',user=None,password=None)
one=us.find_one(1,"photo")
us.delete(one.get("id"))

TEST:
us=MongoUserStore(host='localhost',db='userstore',user=None,password=None)
one=us.find_one(1,"photo")
file_write = open('test3.png','wb')
file_write.write(one.get("data"))
file_write.close()
'''

class MongoUserStore():
    def __init__(self, host, db, port=27017, user=None, password=None, bucket='fs', **kwargs):
        # logging.debug('Using MongoDB for static content serving at host={0} db={1}'.format(host, db))
        _db = Connection(host=host, port=port, **kwargs)[db]
        self.db=_db
        if user is not None and password is not None:
            _db.authenticate(user, password)
        self.fs = gridfs.GridFS(_db, bucket)
        self.fs_files = _db[bucket + ".files"]   # the underlying collection GridFS uses
        
    def save(self, content):
        id = content.get("id")
        # Seems like with the GridFS we can't update existing ID's we have to do a delete/add pair
        if id:
            self.delete(id)
        
        data=content.get("data")
        with self.fs.new_file( user_id=content.get("user_id"), type=content.get("type")) as fp:
            if hasattr(data, '__iter__'):
                for chunk in data:
                    fp.write(chunk)
            else:
                fp.write(data)
        return content
    
    def delete(self, id):
        if self.fs.exists({"_id": id}):
            self.fs.delete(id)
            
    def find_one(self,user_id,type):
        # self.find({"user_id":user_id,"type":type}) # New feature "find" in version gridfs 2.7?
        doc=self.db["fs.files"].find_one({"user_id":user_id,"type":type},["_id"])
        if doc:
            id=doc["_id"];
            with self.fs.get(id) as fp:
                return {"id":id, "user_id":user_id, "type":type, "data": fp.read(), "length":fp.length}
 
