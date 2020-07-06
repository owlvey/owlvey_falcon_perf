from locust import TaskSet, task, HttpUser, between, tag, events, SequentialTaskSet
import logging


class OrganizationReadSequence(SequentialTaskSet):

    @task
    def list_customers(self):
        self.user.state['organizations'] = self.user.organization_component.get_all()

    @task
    def read_customer(self):
        for organization in self.user.state['organizations']:
            self.user.organization_component.get_by_id(organization["id"])
        self.interrupt()
