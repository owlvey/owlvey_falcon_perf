import unittest
import requests
from app.components.ConfigurationComponent import ConfigurationComponent
from app.components.OwlveyComponent import OwlveyComponent
from functools import partial
from specs.LiveServerSession import LiveServerSession
from datetime import datetime, timedelta
import random


class OrganizationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.configuration = ConfigurationComponent()
        self.session = LiveServerSession(self.configuration.api)
        self.owlvey = OwlveyComponent(self.session, self.configuration)

    def test_ensure_organization(self):
        self.owlvey.ensure_organization_product("utest_org", "utest_prod")

    def test_ensure_service_feature(self):
        org, prod, ser, fea = self.owlvey.ensure_organization_product_service_feature("utest_org",
                                                                                      "utest_prod",
                                                                                      "utest_service",
                                                                                      "utest_feature"
                                                                                      )

    def test_ensure_source(self):
        org, prod, ser, fea = self.owlvey.ensure_organization_product_service_feature("utest_org",
                                                                                      "utest_prod",
                                                                                      "utest_service",
                                                                                      "utest_feature"
                                                                                      )
        self.owlvey.ensure_source(prod, fea, "utest_source")

    def test_send_source_item(self):
        org, prod, ser, fea = self.owlvey.ensure_organization_product_service_feature("utest_org",
                                                                                      "utest_prod",
                                                                                      "utest_service",
                                                                                      "utest_feature"
                                                                                      )
        source = self.owlvey.ensure_source(prod, fea, "utest_source")

        base = datetime(2020, 1, 1)
        for temp in range(0, 365):
            target = base + timedelta(days=temp)
            good = random.randint(800, 1000)
            total = 1000
            self.owlvey.send_source_item(source, target, total, good)


if __name__ == '__main__':
    unittest.main()


