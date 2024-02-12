# locustfile.py

from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(5, 10)  # Simulate realistic wait time between actions

    @task
    def visit_homepage(self):
        response = self.client.get("/")
        self.response_check(response, expected_status_code=200, expected_text="Welcome to your Flask API!")

    @task(weight=2)  # Make this task twice as likely to be executed
    def add_user(self):
        data = {"name": "Locust User", "email": f"locust_{self.user_id}@example.com"}
        response = self.client.post(url_for("add_user"), json=data)
        self.response_check(response, expected_status_code=201, expected_text="User created successfully")

    def response_check(self, response, expected_status_code, expected_text):
        """
        This method checks the response against various criteria and marks the request as failed if they are not met.

        Args:
            response: The response object from the client.
            expected_status_code: The expected HTTP status code.
            expected_text: The expected text to be present in the response body.
        """
        if response.status_code != expected_status_code:
            response.failure(f"Unexpected status code: {response.status_code} (expected: {expected_status_code})")
        elif expected_text not in response.text:
            response.failure(f"Expected text '{expected_text}' not found in response body")

# You can add more checks to the response_check method as needed,
# such as checking for specific JSON data or headers.
