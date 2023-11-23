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

import logging
from locust import HttpUser, task
from locust import events

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/hi")
        self.client.get("/hi/flaskie")

    @events.quitting.add_listener
    def _(environment, **kw):
        if environment.stats.total.fail_ratio > 0.001:
            logging.error("Test failed due to failure ratio > 0.1%")
            environment.process_exit_code = 1
        elif environment.stats.total.avg_response_time > 80:
            logging.error("Test failed due to average response time ratio > 80 ms")
            environment.process_exit_code = 1
        elif environment.stats.total.get_response_time_percentile(0.95) > 300:
            logging.error("Test failed due to 95th percentile response time > 300 ms")
            environment.process_exit_code = 1
        else:
            environment.process_exit_code = 0

# import time
# from locust import HttpUser, task, between

# class QuickstartUser(HttpUser):
#     wait_time = between(1, 5)

#     @task
#     def hello_world(self):
#         self.client.get("/hello")
#         self.client.get("/world")

#     @task(3)
#     def view_items(self):
#         for item_id in range(10):
#             self.client.get(f"/item?id={item_id}", name="/item")
#             time.sleep(1)

#     def on_start(self):
#         self.client.post("/login", json={"username":"foo", "password":"bar"})


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




# # creds is created before running locust file and can be stored outside or part of locust # file
# creds = [('demo_user1', 'pass1', 'lnla'),
#          ('demo_user2', 'pass2', 'taam9'),
#          ('demo_user3', 'pass3', 'wevee'),
#          ('demo_user4', 'pass4', 'avwew')]

# class RegisteredUser(SequentialTaskSet)

#     def on_start(self):
#         self.credentials = creds.pop()

#     @task
#     def task_one_name(self):
#         task_one_commands

#     @task
#     def task_two_name(self):
#         task_two_commands

#     @task
#     def stop(self):
#         if len(creds) == 0:
#             self.user.environment.reached_end = True
#             self.user.environment.runner.quit()


# class ApiUser(HttpUser):
#     tasks = [RegisteredUser]
#     host = 'hosturl'


	
# from locust.exception import StopLocust
 
# ...
 
# response = locust.client.post(uri, data=json.dumps(data), headers=headers)
# if response.status_code != 200:
#     raise StopLocust()
