class Blockref:
    name: str
    attributes: dict

    def __init__(self, name: str, attribute_list: list):
        self.name = name
        self.attributes = dict(attribute_list)
