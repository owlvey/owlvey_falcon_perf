from app.components.ConfigurationComponent import ConfigurationComponent
from app.gateways.OwlveyGateway import OwlveyGateway


class OwlveyComponent:

    def __init__(self, client, configuration: ConfigurationComponent):
        self.gateway = OwlveyGateway(client, configuration)

    def ensure_organization_product(self, organization, product):
        org = self.gateway.post_organization(organization)
        prod = self.gateway.post_product(org["id"], product)
        return org, prod

    def ensure_service(self, product, service):
        ser = self.gateway.post_service(product["id"], service)
        return ser

    def ensure_feature(self, product, feature):
        fea = self.gateway.post_feature(product["id"], feature)
        return fea

    def ensure_feature_service(self, service, feature):
        self.gateway.put_service_map(service["id"], feature["id"])

    def ensure_feature_with_service(self, product, service, feature):
        fea = self.gateway.post_feature(product["id"], feature)
        self.gateway.put_service_map(service["id"], fea["id"])
        return fea

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

    def read_organizations(self):
        return self.gateway.get_organizations()

    def read_organization(self, organization_id):
        return self.gateway.get_organization(organization_id)

    def read_products(self, organization_id):
        return self.gateway.get_products(organization_id)

    def read_product(self, product_id):
        return self.gateway.get_product(product_id)

    def read_product_daily(self, product_id, start, end):
        return self.gateway.get('/products/{}/reports/daily/services/series?start={}&end={}&group='.format(product_id, start, end))

    def read_services(self, product_id):
        return self.gateway.get('/services?productId={}'.format(product_id))

    def read_services_by_date(self, product_id, start, end):
        return self.gateway.get('/services?productId={}&start={}&end={}&group='.format(product_id, start, end))

    def read_service_by_id_date(self,  service_id, start, end):
        return self.gateway.get('/services/{}?start={}&end={}'.format(service_id, start, end))

    def read_service_by_id_date_report(self,  service_id, start, end):
        return self.gateway.get('/services/{}/reports/daily/series?start={}&end={}'.format(service_id, start, end))

    def read_product_daily_report(self, product_id, start, end):
        return self.gateway.get('/products/{}/reports/daily/services/series?start={}&end={}&group='.format(product_id, start, end))

    def read_feature(self, feature_id):
        return self.gateway.get('/features/{}'.format(feature_id))

    def read_features(self, product_id):
        return self.gateway.get('/features?productId={}'.format(product_id))

    def read_features_by_date(self, product_id, start, end):
        return self.gateway.get('/features?productId={}&start={}&end={}'.format(product_id, start, end))

    def read_sources(self, product_id, start, end):
        return self.gateway.get('/sources?productId={}&start={}&end={}'.format(product_id, start, end))

    def download_backup(self, filename):
        return self.gateway.get_backup(filename)

    def restore_backup(self, filename):
        return self.gateway.post_restore(filename)










