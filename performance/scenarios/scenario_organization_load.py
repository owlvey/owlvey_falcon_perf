from datetime import datetime
from locust import TaskSet, task, HttpUser, between, tag, events, SequentialTaskSet
from locust.runners import MasterRunner

from app.components.ConfigurationComponent import ConfigurationComponent
from app.components.OrganizationComponent import OrganizationComponent
from app.components.OwlveyComponent import OwlveyComponent
from app.gateways.OwlveyGateway import OwlveyGateway
from performance.sequences.Organizations.OrganizationCreateSequence import OrganizationCreateSequence
from performance.sequences.Organizations.OrganizationReadSequence import OrganizationReadSequence
import logging

from specs.LiveServerSession import LiveServerSession


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logging.warning("A new test is starting")
    logging.warning(environment.__dict__.keys())

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logging.warning("A new test is ending")


# init for nodes 
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        logging.warning("I'm on master node")
    else:
        logging.warning("I'm on a worker or standalone node")


class CustomerWriteUser(HttpUser):
    weight = 10
    wait_time = between(3, 7)
    tasks = {OrganizationCreateSequence: 1}

    def __init__(self, parent):
        super().__init__(parent)
        self.configuration = ConfigurationComponent()
        self.session = LiveServerSession(self.configuration.api)
        self.owlvey_gateway = OwlveyGateway(self.client, self.configuration.identity_api)
        self.owlvey_gateway_live = OwlveyGateway(self.session, self.configuration.identity_api)
        self.organization_component = OrganizationComponent(self.owlvey_gateway)
        self.state = dict()

    def on_start(self):
        pass


class CustomerReadUser(HttpUser):
    weight = 40
    wait_time = between(3, 7)
    tasks = {OrganizationReadSequence: 1}

    def __init__(self, parent):
        super().__init__(parent)
        self.configuration = ConfigurationComponent()
        self.live_client = LiveServerSession(self.configuration.api)
        self.owlvey_gateway = OwlveyGateway(self.client, self.configuration.identity_api)
        self.owlvey_gateway_live = OwlveyGateway(self.live_client, self.configuration.identity_api)
        self.organization_component = OrganizationComponent(self.owlvey_gateway)
        self.state = dict()

    def on_start(self):
        pass

    def on_stop(self):
        pass



