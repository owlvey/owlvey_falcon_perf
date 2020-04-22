from datetime import datetime, timedelta
from app.components.ConfigurationComponent import ConfigurationComponent
from app.components.OwlveyComponent import OwlveyComponent
import random
import unittest
from specs.LiveServerSession import LiveServerSession

organization_name, product_name = 'test_A001_org', 'test_A001_prod'


def start_case_a001(owlvey):
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

    return product


def build_context(owlvey):
    organizations = owlvey.read_organizations()
    organization = next((e for e in organizations if e['name'] == organization_name))
    products = owlvey.read_products(organization['id'])
    product = next((e for e in products if e['name'] == product_name))
    product['services'] = owlvey.read_services(product['id'])
    product['features'] = list()

    for fea in owlvey.read_features(product['id']):
        feature = owlvey.read_feature(fea["id"])
        product['features'].append(feature)

    return product


def load_case_a001(owlvey, product):
    base = datetime(2020, 1, 1)
    for feature in product["features"]:
        for indicator in feature["indicators"]:
            for temp in range(0, 180):
                source = dict()
                source['id'] = indicator['sourceId']
                target = base + timedelta(days=temp)
                good = random.randint(800, 1000)
                total = 1000
                owlvey.send_source_item(source, target, total, good)


class TargetTest(unittest.TestCase):

    def setUp(self) -> None:
        self.configuration = ConfigurationComponent()
        self.session = LiveServerSession(self.configuration.api)
        self.owlvey = OwlveyComponent(self.session, self.configuration)

    def test_load(self):
        start_case_a001(self.owlvey)
        build_context(self.owlvey)

    def test_complete(self):
        start_case_a001(self.owlvey)
        product = build_context(self.owlvey)
        load_case_a001(self.owlvey, product)
