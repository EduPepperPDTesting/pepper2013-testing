from django.conf import settings
import pymongo
import logging
log = logging.getLogger("tracking")


class MongoPollStore(object):

    def __init__(self, host, db, collection_poll, collection_answers, port=27017, default_class=None, user=None,
                 password=None, mongo_options=None, **kwargs):

        super(MongoPollStore, self).__init__(**kwargs)

        if mongo_options is None:
            mongo_options = {}

        self.collection_poll = pymongo.connection.Connection(
                host=host,
                port=port,
                tz_aware=True,
                **mongo_options
        )[db][collection_poll]

        self.collection_answers = pymongo.connection.Connection(
                host=host,
                port=port,
                tz_aware=True,
                **mongo_options
        )[db][collection_answers]

        if user is not None and password is not None:
            self.collection_poll.database.authenticate(user, password)
            self.collection_answers.database.authenticate(user, password)

        # Force mongo to report errors, at the expense of performance
        self.collection_poll.safe = True
        self.collection_answers.safe = True

    def get_poll(self, type, identifier):
        return self.collection_poll.find_one(
                {
                    'type': type,
                    'identifier': str(identifier),
                }
        )

    def set_poll(self, type, identifier, question, answers, expiration):
        return self.collection_poll.update(
                {
                    'type': type,
                    'identifier': str(identifier),
                },
                {
                    '$set': {
                        'question': question,
                        'answers': answers,
                        'expiration': expiration,
                    }
                },
                True
        )

    def get_answers(self, type, identifier, answer, user=None):
        data = {
            'type': type,
            'identifier': str(identifier),
        }
        if user:
            data.update({'user': str(user)})
        if answer:
            data.update({'answer': answer})

        return self.collection_answers.find(data)

    def set_answer(self, type, identifier, user, answer):
        return self.collection_answers.update(
                {
                    'type': type,
                    'identifier': str(identifier),
                },
                {
                    '$set': {
                        'user': str(user),
                        'answer': str(answer),
                    }
                },
                True
        )

    def user_answered(self, type, identifier, user):
        answers = self.collection_answers.find(
                {
                    'type': type,
                    'identifier': str(identifier),
                    'user': str(user),
                }
        ).count()
        return bool(answers)

    def poll_exists(self, type, identifier):
        polls = self.collection_poll.find(
                {
                    'type': type,
                    'identifier': str(identifier),
                }
        ).count()
        return bool(polls)


def poll_store():
    options = {}
    options.update(settings.POLLSTORE['OPTIONS'])
    return MongoPollStore(**options)
