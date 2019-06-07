from oef.agents import OEFAgent
from oef.schema import AttributeSchema, DataModel, Description
from oef.messages import CFP_TYPES
import json


class FetchAgent(OEFAgent):

    def __init__(self, public_key, oef_addr, oef_port, metadata = {}, path_to_data = '', price = 0):
        OEFAgent.__init__(self, public_key, oef_addr, oef_port)
        if metadata != {} and path_to_data != '':
            try:
                self.service, self.data = self.load_service(metadata, path_to_data)
                self.price = abs(int(price))
            except Exception as e:
                print('Invalid dataset, metadata or price: ', e)
                exit(1)
    
    def load_service(self, metadata, path_to_data):
        dataset_info = metadata['base']
        attributes = description = {}
        for item in dataset_info['tags']:
            attributes[item] = description[item] = 'Tagged: ' + item
        attribute_list = []
        for key, value in attributes.items():
            attribute_list.append(AttributeSchema(key, str, False, value))
        data_model = DataModel(dataset_info['name'], attribute_list, dataset_info['description'])
        service = Description(description, data_model)
        with open(path_to_data) as infile:
            data = json.load(infile)
        return service, data

    def publish(self, service):
        self.register_service(0, service)

    
    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print('[{0}]: Received CFP from {1}'.format(self.public_key, origin))
        proposal = Description({'price': self.price})
        print('[{}]: Sending propose at price: {}'.format(self.public_key, self.price))
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print('[{0}]: Received accept from {1}.'.format(self.public_key, origin))
        encoded_data = json.dumps(self.data).encode('utf-8')
        print('[{0}]: Sending data to {1}: {2}'.format(self.public_key, origin, self.data))
        self.send_message(0, dialogue_id, origin, encoded_data)
        self.stop()

    '''

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print('[{0}]: Received decline from {1}.'.format(self.public_key, origin))
        self.stop()
    '''


if __name__ == '__main__':
    meta = {
        'base': {
            'name': 'Iris Dataset',
            'description': 'Multivariate Iris flower dataset for linear discriminant analysis.',
            'tags': [
                'flowers',
                'classification',
                'plants'
            ]
        }
    }
    data_path = './test/data/iris_meta.json'

    agent = FetchAgent('OV_DLM', oef_addr = '127.0.0.1', oef_port = 3333, metadata = meta, path_to_data = data_path)
    agent.connect()
    agent.register_service(0, agent.service)
    print('service offered')
    try:
        agent.run()
    finally:
        agent.stop()
        agent.disconnect()
