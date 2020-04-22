from locust import TaskSet, task, HttpLocust, between, TaskSequence, seq_task
from app.components.ConfigurationComponent import ConfigurationComponent
from app.components.OwlveyComponent import OwlveyComponent
from specs.LiveServerSession import LiveServerSession
from specs.test_A002 import read_case_a002, build_context, restore_backup

'''
Stress because we will test different interactions 
'''


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.configuration = ConfigurationComponent()
        self.session = LiveServerSession(self.configuration.api)
        self.owlvey_live = OwlveyComponent(self.session, self.configuration)
        self.owlvey = OwlveyComponent(self.client, self.configuration)
        self.product = None

    def on_start(self):
        print('################################ on start cls')
        self.product = build_context(self.owlvey_live)

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    @task
    def execute(self):
        print('*********************** on start cls')
        read_case_a002(self.owlvey, self.product)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 15)
