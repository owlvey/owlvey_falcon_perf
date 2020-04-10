import datetime
from locust import HttpLocust, TaskSet, task, between
from app.components.ConfigurationComponent import ConfigurationComponent
from app.components.OwlveyComponent import OwlveyComponent


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.owlvey = OwlveyComponent(self.client, ConfigurationComponent())

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def logout(self):
        pass

    @task(1)
    def ensure_organization_product(self):
        self.owlvey.ensure_organization_product('test_org', None)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 9)


