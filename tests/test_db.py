import os
os.environ["TESTING"] = "true"

import unittest
from peewee import *
from app import TimelinePost

MODELS = [TimelinePost]
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Use test database
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TimelinePost._meta.database = test_db
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(name='John Doe',
                                         email='john@example.com',
                                         content='Hello world, I\'m John!')
        assert first_post.id == 1

        second_post = TimelinePost.create(name='Jane Doe',
                                          email='jame@example.com',
                                          content='Hello world, I\'m Jane!')
        assert second_post.id == 2

        posts = TimelinePost.select().order_by(TimelinePost.id)
        assert posts.count() == 2
        assert posts[0].name == 'John Doe'
        assert posts[1].email == 'jame@example.com'
