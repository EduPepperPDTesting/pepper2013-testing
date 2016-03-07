from django.conf import settings
import pymongo
import logging
log = logging.getLogger("tracking")


class MongoViewCounterStore(object):

    def __init__(self, host, db, collection, port=27017, default_class=None, user=None, password=None,
                 mongo_options=None, **kwargs):

        super(MongoViewCounterStore, self).__init__(**kwargs)

        if mongo_options is None:
            mongo_options = {}

        self.collection = pymongo.connection.Connection(
                host=host,
                port=port,
                tz_aware=True,
                **mongo_options
        )[db][collection]

        if user is not None and password is not None:
            self.collection.database.authenticate(user, password)

        # Force mongo to report errors, at the expense of performance
        self.collection.safe = True

    def get_item(self, type, identifier):
        return self.collection.find_one(
                {
                    'type': type,
                    'identifier': identifier,
                }
        )

    def get_most_viewed(self, type, number):
        return self.collection.find(
                {
                    'type': type,
                }
        ).sort([('views', -1)]).limit(number)

    def set_item(self, type, identifier, views):
        return self.collection.update(
                {
                    'type': type,
                    'identifier': identifier,
                },
                {
                    '$inc': {'views': views}
                },
                True
        )

    def delete_item(self, type, identifier):
        return self.collection.remove(
                {
                    'type': type,
                    'identifier': identifier,
                }
        )


def view_counter_store():
    options = {}
    options.update(settings.VIEWCOUNTERSTORE['OPTIONS'])
    return MongoViewCounterStore(**options)
