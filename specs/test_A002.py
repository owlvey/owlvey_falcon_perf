from datetime import datetime, timedelta
from app.components.ConfigurationComponent import ConfigurationComponent
from app.components.OwlveyComponent import OwlveyComponent
import random
import unittest
from specs.LiveServerSession import LiveServerSession

organization_name, product_name = 'test_A002_org', 'test_A002_prod'


def start_case_a002(owlvey):
    org, product = owlvey.ensure_organization_product(organization_name, product_name)
    product['services'] = list()
    product['features'] = list()

    for j in range(1, 11):
        fea_inst = owlvey.ensure_feature(product, 'test_001_fea__{}'.format(j))
        fea_inst["sources"] = list()
        product['features'].append(fea_inst)
        for s in range(1, 11):
            source_instance = owlvey.ensure_source(product, fea_inst, "test_source_{}".format(s))
            fea_inst["sources"].append(source_instance)

    for i in range(1, 21):
        ser_inst = owlvey.ensure_service(product, 'test_001_ser__{}'.format(i))
        ser_inst["features"] = list()
        product['services'].append(ser_inst)
        for fea in product["features"]:
            owlvey.ensure_feature_service(ser_inst, fea)

    base = datetime(2020, 1, 1)
    for feature in product["features"]:
        for source in feature["sources"]:
            for temp in range(0, 180):
                target = base + timedelta(days=temp)
                good = random.randint(800, 1000)
                total = 1000
                owlvey.send_source_item(source, target, total, good)
    return product


def build_context(owlvey):
    organizations = owlvey.read_organizations()
    organization = next((e for e in organizations if e['name'] == organization_name))
    products = owlvey.read_products(organization['id'])
    product = next((e for e in products if e['name'] == product_name))
    product['services'] = owlvey.read_services(product['id'])
    product['features'] = owlvey.read_features(product['id'])
    return product


def read_case_a002(owlvey, product):
    start = '2020-02-01T19:52:41.727Z'
    end = '2020-04-10T19:52:41.727Z'
    owlvey.read_organizations()
    owlvey.read_organization(product["customerId"])
    owlvey.read_products(product["customerId"])
    owlvey.read_product(product["id"])
    owlvey.read_product_daily(product["id"], start, end)
    services = owlvey.read_services_by_date(product["id"], start, end)

    for service in services[:2]:
        owlvey.read_service_by_id_date(service["id"], start, end)
        owlvey.read_service_by_id_date_report(service["id"], start, end)

    owlvey.read_product_daily_report(product["id"], start, end)

    owlvey.read_features_by_date(product["id"], start, end)
    owlvey.read_sources(product["id"], start, end)


def download_backup(owlvey):
    owlvey.download_backup("A002.backup")


def restore_backup(owlvey):
    owlvey.restore_backup("A002.backup")


class TargetTest(unittest.TestCase):

    def setUp(self) -> None:
        self.configuration = ConfigurationComponent()
        self.session = LiveServerSession(self.configuration.api)
        self.owlvey = OwlveyComponent(self.session, self.configuration)

    def test_load(self):
        start_case_a002(self.owlvey)
        build_context(self.owlvey)
        download_backup(self.owlvey)

    def test_restore(self):
        restore_backup(self.owlvey)

    def test_complete(self):
        start_case_a002(self.owlvey)
        product = build_context(self.owlvey)
        read_case_a002(self.owlvey, product)



