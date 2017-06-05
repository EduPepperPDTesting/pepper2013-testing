from pymongo import Connection
import gridfs
from gridfs.errors import NoFile
from bson import ObjectId

class MongoUserStore():
    def __init__(self, host, db, port=27017, user=None, password=None, bucket='fs', **kwargs):
        # logging.debug('Using MongoDB for static content serving at host={0} db={1}'.format(host, db))
        _db = Connection(host=host, port=port, **kwargs)[db]
        self.db = _db
        if user is not None and password is not None:
            _db.authenticate(user, password)
        self.fs = gridfs.GridFS(_db, bucket)
        self.fs_files = _db[bucket + ".files"]   # the underlying collection GridFS uses

    def save(self, _id, data):
        # Seems like with the GridFS we can't update existing ID's we have to do a delete/add pair
        if _id:
            self.delete(_id)

        with self.fs.new_file(_id=_id) as fp:
            if hasattr(data, '__iter__'):
                for chunk in data:
                    fp.write(chunk)
            else:
                fp.write(data)

    def delete(self, _id):
        if self.fs.exists({"_id": _id}):
            self.fs.delete(_id)

    def find_one(self, ref_id, type):
        _id = {"ref_id": ref_id, "type": type}
        doc = self.db["fs.files"].find_one({"_id.ref_id": ref_id, "_id.type": type})
        if doc:
            with self.fs.get(_id) as fp:
                return {"_id": _id, "data": fp.read(), "length": fp.length}
