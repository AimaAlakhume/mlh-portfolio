# test_db.py

import unittest

from peewee import *
from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

from app import app

class AppTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()
    
  def test_home(self):
    response = self.client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "<title>MLH Fellow</title> in html
    
  def test_timeline(self):
    response = self.client.get("/api/timeline_post")
    assert response.status_code == 200
    assert response.is_json
    json = response.get_json()
    assert "timeline_posts" in json
    assert len(json["timeline_posts"]) == 0
