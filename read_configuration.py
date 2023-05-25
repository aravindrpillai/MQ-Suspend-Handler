import xml.etree.ElementTree as ET

class Configuration:
    _instance = None
    _root = None
    _file = 'configuration.xml'
    
    @staticmethod
    def get_instance():
        if Configuration._instance is None:
            Configuration()
        return Configuration._instance

    def __init__(self):
        if Configuration._instance is not None:
            raise Exception("Class cannot be instantiated multiple times.")
        Configuration._instance = self
        Configuration._root = ET.parse(Configuration._file).getroot()

    def read_file(self):
        content = []
        for app_elem in Configuration._root.iter('app'):
            app_name = app_elem.get('name')
            app_url = app_elem.get('app_url')
            for queue_elem in app_elem.iter('queue'):
                queue_id = queue_elem.get('id')
                queue_name = queue_elem.get('name')
                ping_value = queue_elem.find('ping').text.strip()
                content.append((app_name, app_url, queue_id, queue_name, ping_value))
        return content