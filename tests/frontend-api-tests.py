#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Frontend API validation and load testing
#
# Usage:
#   
#   pip install -r requirements.txt
#
#   locust --modern-ui --host=http://0.0.0.0:8081 -f frontend-api-tests.py
#   firefox http://0.0.0.0:8089/
#
#   (headless without Web UI for 30s)
#   locust --headless --users 3 --spawn-rate 1 --run-time=30s --host=http://0.0.0.0:8081 -f frontend-api-tests.py
#
#   (headless without UI and HTML report output)
#   locust --headless --users 10 --spawn-rate 1 --host=http://0.0.0.0:8081 -f frontend-api-tests.py --html tests-results.html
#
import logging
from locust import HttpUser, task
from locust import events

class HelloWorldUser(HttpUser):
    @task
    def test_hi(self):
        self.client.get("/hi")

    @task
    def test_hi_name(self):
        self.client.get("/hi/flaskie")

    @task
    def test_ping(self):
        self.client.get("/ping")

    @task
    def test_redis(self):
        self.client.get("/redis")

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
