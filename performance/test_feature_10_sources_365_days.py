from locust import TaskSet, task, HttpLocust, between, TaskSequence, seq_task
from datetime import datetime, timedelta
from app.components.ConfigurationComponent import ConfigurationComponent
from app.components.OwlveyComponent import OwlveyComponent
import random

class UserBehavior(TaskSequence):

    def __init__(self, parent):
        super().__init__(parent)
        self.owlvey = OwlveyComponent(self.client, ConfigurationComponent())
        org, prod, ser, fea = self.owlvey.ensure_organization_product_service_feature("test_org", "test_prod",
                                                                                      "test_service", "test_feature")
        self.product = prod
        self.service = ser
        self.feature = fea
        self.source = None

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def logout(self):
        pass

    @seq_task(1)
    def setup_context(self):
        name = "test_source_{}".format(random.randint(1, 9))
        self.source = self.owlvey.ensure_source(self.product, self.feature, name)

    @seq_task(2)
    def setup_source_items(self):
        base = datetime(2020, 1, 1)
        for temp in range(0, 365):
            target = base + timedelta(days=temp)
            good = random.randint(800, 1000)
            total = 1000
            self.owlvey.send_source_item(self.source, target,  total, good)




class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 9)


