from locust import TaskSet, task, HttpUser, between, tag
from app.components.ConfigurationComponent import ConfigurationComponent
from app.components.OwlveyComponent import OwlveyComponent
from specs.LiveServerSession import LiveServerSession
from specs.test_A001 import load_case_a001, build_context

'''
Stress because we will test different interactions 
'''


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

    # And tasks can then be specified/excluded using the --tags/-T and --exclude-tags/-E command line arguments.
    @task
    @tag("tag1", "tag2")
    def setup_context(self):
        load_case_a001(self.owlvey, self.product)
