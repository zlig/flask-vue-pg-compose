# from locust import HttpUser, task

# class HelloWorldUser(HttpUser):
#     @task
#     def hello_world(self):
#         self.client.get("/hi")
#         self.client.get("/hi/flaskie")


from locust import HttpUser, TaskSet, task

class FrontendApi(TaskSet):

    @task
    def get_tests(self):
        self.client.get("/hi")
        self.client.get("/hi/flaskie")
        
    @task
    def put_tests(self):
        self.client.post("/tests", {
						  "name": "load testing",
						  "description": "checking if a software can handle the expected load"
						})
        
class WebsiteUser(HttpUser):
    task_set = FrontendApi