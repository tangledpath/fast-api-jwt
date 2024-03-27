import yaml


class Config:
    """ Create service config with given service (or none)"""

    def __init__(self):
        with open("config/config.yaml", "r") as yaml_file:
            self.settings = yaml.safe_load(yaml_file)

        # if service:
        #   service_address_key = f"{service.upper()}_SERVICE_ADDRESS"
        #   self.settings["WEB_SERVER_ADDRESS"] = self.settings[service_address_key]
