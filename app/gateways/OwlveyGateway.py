import datetime
import pathlib

import requests
import shutil
from os import path

from app.components.ConfigurationComponent import ConfigurationComponent


class OwlveyGateway:
    def __init__(self, client, configuration: ConfigurationComponent):
        self.client = client
        self.configuration = configuration
        self.token = None
        self.token_on = None

    def generate_token(self):
        payload = {
            "grant_type": "client_credentials",
            "scope": "api",
            "client_id": "CF4A9ED44148438A99919FF285D8B48D",
            "client_secret": "0da45603-282a-4fa6-a20b-2d4c3f2a2127"
        }
        response = requests.post(self.configuration.identity_api + "connect/token",
                                 data=payload)
        self.token_on = datetime.datetime.now()
        self.token = response.json()

    def __build_authorization_header(self):
        if self.token:
            expires_in = self.token["expires_in"]
            if (self.token_on + datetime.timedelta(seconds=expires_in + 30)) > datetime.datetime.now():
                self.generate_token()
        else:
            self.generate_token()

        return {
            "Authorization": "Bearer " + self.token["access_token"]
        }

    def get_organizations(self):
        return self.get('/customers/lite')

    def get_organization(self, organization_id):
        return self.get('/customers/{}'.format(organization_id))

    def get_products(self, organization_id):
        return self.get('/products/lite?customerId={}'.format(organization_id))

    def get_product(self, product_id):
        return self.get('/products/{}'.format(product_id))

    def get(self, url):
        response = self.client.get(url, verify=False,
                                   headers=self.__build_authorization_header())
        if response.status_code > 299:
            raise ValueError(url + " \n " + response.text)
        return response.json()

    def __internal_post(self, url, payload):
        response = self.client.post(url,
                                    json=payload, verify=False,
                                    headers=self.__build_authorization_header())
        if response.status_code > 299:
            raise ValueError(url + " \n " + str(payload) + " \n " + response.text)
        return response.json()

    def __internal_put(self, url, payload):
        response = self.client.put(url,
                                   json=payload, verify=False,
                                   headers=self.__build_authorization_header())
        if response.status_code > 299:
            raise ValueError(str(response.status_code) + " :  " + response.text)
        if response.text:
            return response.json()
        else:
            return {}

    def post_organization(self, name):
        return self.__internal_post('/customers', {"name": name})

    def post_product(self, organization_id, product):
        return self.__internal_post('/products', {"name": product, "customerId": organization_id})

    def post_service(self, product_id, service):
        return self.__internal_post('/services', {"name": service, "productId": product_id})

    def post_feature(self, product_id, feature):
        return self.__internal_post('/features', {"name": feature, "productId": product_id})

    def post_source(self, product_id, source, kind, group):
        return self.__internal_post('/sources', {"name": source, "productId": product_id,
                                                 'kind': kind, 'group': group})

    def put_service_map(self, service_id, feature_id):
        return self.__internal_put('/services/{}/features/{}'.format(service_id, feature_id), {})

    def put_sli(self, feature_id, source_id):
        return self.__internal_put('/features/{}/indicators/{}'.format(feature_id, source_id), {})

    def post_source_item(self, source_id, on, total, good):
        return self.__internal_post('/sourceItems',
                                    {
                                        "sourceId": source_id,
                                        "start": on.isoformat(),
                                        "end": on.isoformat(),
                                        "total": total,
                                        "good": good
                                    })

    def get_backup(self, filename):
        with self.client.get('/migrations/backup/data', verify=False,
                             headers=self.__build_authorization_header(), stream=True) as response:
            path_target = path.join("./../backups", filename)
            if response.status_code > 299:
                raise ValueError(str(response.status_code) + " :  " + response.text)
            with open(path_target, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

    def post_restore(self, filename):
        path_target = path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "backups", filename)
        print(path_target)
        files = {'data': open(path_target, 'rb')}
        with self.client.post('/migrations/restore', files=files,
                              headers=self.__build_authorization_header(), verify=False) as response:
            if response.status_code > 299:
                raise ValueError(str(response.status_code) + " :  " + response.text)
