from locust import TaskSet, task, HttpUser, between, tag, events, SequentialTaskSet

from app.components.RandomComponent import RandomComponent


class OrganizationCreateSequence(SequentialTaskSet):

    @task
    def create_customer(self):
        self.user.state["organization"] = self.user.organization_component.post(RandomComponent.random_string())

    @task
    def read_customer(self):
        organization = self.user.state["organization"]
        self.user.organization_component.get_by_id(organization['id'])

    @task
    def update_customer(self):
        self.user.organization_component.put(self.user.state["organization"]['id'], RandomComponent.random_string())

    @task
    def read_customer_v2(self):
        organization = self.user.state["organization"]
        self.user.organization_component.get_by_id(organization['id'])

    @task
    def delete_customer(self):
        pass
        # organization = self.user.state["organization"]
        # self.user.organization_component.delete(organization['id'])
        # self.interrupt()
