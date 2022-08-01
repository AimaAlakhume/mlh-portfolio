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
        response = self.client.get("/api/show_posts")
        assert response.status_code == 200
        print('code given as:', response.status_code) #debug
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        
        # test /api/timeline_post GET and POST apis
        response = self.client.post("/api/show_posts", data={"name": "john", "email": "john@example.com", "content": "Hello world, I'm John!"})
        html = response.get_data(as_text=True)
        assert "john" in html
        assert "john@example.com" in html
        assert "Hello world, I'm John!" in html

        response = self.client.get("/api/show_posts")
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline", data={"email": "aimailene@gmail.com", "content": "Hello world, I'm Aima!"})
        assert response.status_code >= 400
        html = response.get_data(as_text=True)
        assert "Bad Request" in html

        # POST request with empty content
        response = self.client.post("/api/timeline", data={"name": "Aima Alakhume", "email": "aimailene@gmail.com", "content" : ""})
        assert response.status_code >= 400
        html = response.get_data(as_text=True)
        print('HTML', html)
        assert "Bad Request" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline", data={"name": "John Doe", "email": "not-an-email", "content" : "Hello world, I'm Aima!"})
        assert response.status_code >= 400
        html = response.get_data(as_text=True)
        assert "Bad Request" in html
