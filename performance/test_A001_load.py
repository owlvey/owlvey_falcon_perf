from locust import TaskSet, task, HttpUser, between, tag, events
from locust.runners import MasterRunner
from app.components.ConfigurationComponent import ConfigurationComponent
from app.components.OwlveyComponent import OwlveyComponent
from specs.LiveServerSession import LiveServerSession
from specs.test_A001 import load_case_a001, build_context

'''
Stress because we will test different interactions 
'''

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        print("I'm on master node")
    else:
        print("I'm on a worker or standalone node")

@events.test_start.add_listener
def on_global_start(**kwargs):
    print('a new test started')

@events.test_stop.add_listener
def on_global_stop(**kwargs):
    print('a stop')







class WebsiteUser(HttpUser):
    wait_time = between(5, 9)

    def __init__(self, parent):
        super().__init__(parent)
        self.configuration = ConfigurationComponent()
        self.session = LiveServerSession(self.configuration.api)
        self.owlvey_live = OwlveyComponent(self.session, self.configuration)
        self.owlvey = OwlveyComponent(self.client, self.configuration)
        self.product = None

    def on_start(self):
        self.product = build_context(self.owlvey_live)

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    def on_start():
        pass

    def on_end():
        pass

    # And tasks can then be specified/excluded using the --tags/-T and --exclude-tags/-E command line arguments.
    @task
    @tag("tag1", "tag2")
    def setup_context(self):
        load_case_a001(self.owlvey, self.product)
