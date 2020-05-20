########################################################################################################################
# author            :   Janakiraman Jothimony
# created date      :   20-05-2019
# modified date     :   20-05-2019
# version           :   1
# description       :   supply configuration parameters to the rest of the modules
########################################################################################################################

import xml.etree.ElementTree as XmlTree
import os


class ConfigManager:
    """
    class to manage the configuration read requests

    The class is a singleton. Holds the reference to the configuration file location
    parses the configuration data, and returns the data for the requests
    """

    __singleton = None

    def __init__(self):
        configu_file_location = "../configurations/network_config.xml"

        if not os.path.isfile(configu_file_location):
            raise FileNotFoundError

        self.data = XmlTree.parse(configu_file_location)

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            cls.__singleton = object.__new__(cls)
        return cls.__singleton

    def get_parameter(self, config_item: str):
        """
        return the config value for the requested config_item

        pass the name of the config item to be read.
        If the tag is nested, use > as delimiter
        EG: "address>host_address"
        :param config_item: configuration tag; if nested, use > for delimiting
        :return: config value; str or int
        """
        # parsing of the input is needed as to create XPath if needed
        tags = config_item.split("%")
        print(tags)
        query = ""

        # if nesting is detected, convert into XPath standard
        if len(tags) > 1:
            query = "."
            for item in tags:
                query = query + "/" + item.strip()
        else:
            query = config_item

        entry = self.data.find(query)

        # check if the tag is available if not raise an error
        if entry is None:
            raise Exception(f"invalid nonexistent parameter {query} requested to be read")

        # if tag is available then read the attrib. If conversion needed convert and return
        if entry.attrib['type'] == "int":
            return int(entry.text)
        else:
            return entry.text
