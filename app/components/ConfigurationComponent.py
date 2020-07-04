import os


class ConfigurationComponent:

    def __init__(self):
        self.identity_api = os.getenv("OWLVEY_IDENTITY", "http://identity.owlvey.com:48100/")
        self.api = os.getenv("OWLVEY_API", "http://api.owlvey.com:48100/")
        # self.identity_api = "http://localhost:50000/"
        # self.api = "https://localhost:5001/"
        self.client_id = os.getenv("OWLVEY_CLIENT_API", "CF4A9ED44148438A99919FF285D8B48D")
        self.client_secret = os.getenv("OWLVEY_CLIENT_SECRET", "0da45603-282a-4fa6-a20b-2d4c3f2a2127")
