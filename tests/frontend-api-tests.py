#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Frontend API validation and load testing
#
# Usage:
#   
#   pip install -r requirements.txt
#
#   locust --host=http://0.0.0.0:8081 -f frontend-api-tests.py
#   firefox http://0.0.0.0:8089/
#
#   (headless without Web UI)
#   locust --headless --users 10 --spawn-rate 1 --host=http://0.0.0.0:8081 -f frontend-api-tests.py

from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/hi")
        self.client.get("/hi/flaskie")


# from locust import HttpUser, TaskSet, task

# class FrontendApi(TaskSet):

#     @task
#     def get_tests(self):
#         self.client.get("/hi")
#         self.client.get("/hi/flaskie")
        
#     @task
#     def put_tests(self):
#         self.client.post("/tests", {
# 						  "name": "load testing",
# 						  "description": "checking if a software can handle the expected load"
# 						})
        
# class WebsiteUser(HttpUser):
#     task_set = FrontendApi