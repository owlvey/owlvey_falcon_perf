from app.components.ConfigurationComponent import ConfigurationComponent
from app.gateways.OwlveyGateway import OwlveyGateway


class OwlveyComponent:

    def __init__(self, client, configuration: ConfigurationComponent):
        self.gateway = OwlveyGateway(client, configuration)

    def ensure_organization_product(self, organization, product):
        org = self.gateway.post_organization(organization)
        self.gateway.post_product(org["id"], product)

    def ensure_organization_product_service_feature(self, organization, product, service, feature):
        org = self.gateway.post_organization(organization)
        prod = self.gateway.post_product(org["id"], product)
        ser = self.gateway.post_service(prod["id"], service)
        fea = self.gateway.post_feature(prod["id"], feature)
        self.gateway.put_service_map(ser["id"], fea["id"])
        return org, prod, ser, fea

    def ensure_source(self, product, feature, source):
        sur = self.gateway.post_source(product["id"], source, "Interaction", "Availability")
        self.gateway.put_sli(feature["id"], sur["id"])
        return sur

    def send_source_item(self, source, on, total, good):
        return self.gateway.post_source_item(source["id"], on, total, good)










