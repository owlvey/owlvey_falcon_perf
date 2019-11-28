import datetime

from locust import HttpLocust, TaskSet, task, between
import requests


class UserBehavior(TaskSet):

    def __init__(self, parent):
        self.token_on = None
        self.token = None

        super().__init__(parent)

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.generate_token()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def logout(self):
        pass

    def generate_token(self):
        payload = {
            "grant_type": "client_credentials",
            "scope": "api",
            "client_id": "CF4A9ED44148438A99919FF285D8B48D",
            "client_secret": "0da45603-282a-4fa6-a20b-2d4c3f2a2127"
        }

        response = requests.post("http://localhost:50000/connect/token", data=payload)
        self.token_on = datetime.datetime.now()
        self.token = response.json()

    def __build_authorization_header(self):
        if self.token:
            expires_in = self.token["expires_in"]
            if (self.token_on + datetime.timedelta(seconds=expires_in + 30)) > datetime.datetime.now():
                self.generate_token()
        else:
            self.generate_token()

        return {
            "Authorization": "Bearer " + self.token["access_token"]
        }

    @task(1)
    def get_organizations(self):
        self.client.get('/customers',
                        headers=self.__build_authorization_header())

    @task(2)
    def get_members(self):
        self.client.get('/users',
                        headers=self.__build_authorization_header())


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 9)
