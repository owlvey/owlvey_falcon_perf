from app.gateways.OwlveyGateway import OwlveyGateway


class OrganizationComponent:

    def __init__(self, owlvey_gateway: OwlveyGateway):
        self.gateway = owlvey_gateway

    def get_all(self):
        organizations = self.gateway.get_organizations()
        return organizations

    def get_by_id(self, id):
        organization = self.gateway.get_organization(id)
        return organization

    def post(self, name):
        return self.gateway.post_organization(name)

    def put(self, id, name):
        return self.gateway.put_organization(id, name)

    def delete(self, id):
        return self.gateway.delete_organization(id)





