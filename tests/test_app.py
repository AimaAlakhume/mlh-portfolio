# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<title>Aima Alakhume</title>' in html
        
        response = self.client.get("/aima")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<title>About Aima</title>' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline")
        assert response.status_code == 200 ###
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        
        # test /api/show_posts GET and POST apis
        response = self.client.post("/api/timeline", data={"name": "Aima Alakhume", "email": "aimailene@gmail.com", "content" : "Hello world, I'm Aima!"})
        html = response.get_data(as_text=True)
        assert "Aima Alakhume" in html
        assert "aimailene@gmail.com" in html
        assert "Hello world, I'm Aima!" in html

        response = self.client.get("/api/timeline")
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1

    def test_malformed_timeline_post(self):
        # POST request with name missing
        response = self.client.post("/api/timeline", data={"email": "aimailene@gmail.com", "content": "Hello world, I'm Aima!"})
        assert response.status_code >= 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html  ###

        # POST request with empty content
        response = self.client.post("/api/timeline", data={"name": "Aima Alakhume", "email": "aimailene@gmail.com", "content": ""})
        assert response.status_code >= 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline", data={"name": "Aima Alakhume", "email": "not-an-email", "content" : "Hello world, I'm Aima!"})
        assert response.status_code >= 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
