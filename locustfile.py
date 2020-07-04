import random
import sys
print(sys.path)

from locust import HttpUser, TaskSet, task, HttpLocust, between

class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def index_page(self):
        self.client.get("/")        

