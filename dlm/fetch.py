from oef.agents import OEFAgent
from oef.schema import AttributeSchema, DataModel, Description
from oef.messages import CFP_TYPES, PROPOSE_TYPES
from oef.query import Query, Constraint, NotEq
from typing import List
import json


class FetchAgent(OEFAgent):

    def __init__(self, public_key, oef_addr, oef_port, metadata = {}, save_path = '', price = 0):
        OEFAgent.__init__(self, public_key, oef_addr, oef_port)
        if metadata != {} and save_path != '':
            try:
                self.service, self.data = self.load_service(metadata, save_path)
                self.price = abs(int(price))
            except Exception as e:
                print('Invalid dataset, metadata or price: ', e)
                exit(1)
    
    def load_service(self, metadata, save_path):
        dataset_info = metadata['base']
        attributes = description = {}
        for item in dataset_info['tags']:
            attributes[item] = description[item] = 'Tagged: ' + item
        attribute_list = []
        for key, value in attributes.items():
            attribute_list.append(AttributeSchema(key, str, False, value))
        data_model = DataModel(dataset_info['name'], attribute_list, dataset_info['description'])
        service = Description(description, data_model)
        with open(save_path) as infile:
            data = json.load(infile)
        return service, data

    def publish(self):
        self.register_service(0, self.service)
    
    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode('utf-8'))
        print('[{0}]: Received measurement from {1}: {2}'.format(self.public_key, origin, data))
        self.stop()
        return data


    '''
    PROVIDER FUNCTIONS
    '''

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
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

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print('[{0}]: Received decline from {1}.'.format(self.public_key, origin))
        self.stop()


    '''
    CONSUMER FUNCTIONS
    '''

    def search(self, terms_string):
        search_terms = terms_string.split(' ')
        query_array = []
        for term in search_terms:
            query_array.append(Constraint(term, NotEq(None)))
        query = Query(query_array)
        self.search_services(0, query)

    def on_search_result(self, search_id: int, agents: List[str]):
        if len(agents) == 0:
            print('[{}]: No agent found. Stopping...'.format(self.public_key))
            self.stop()
            return
        print('[{0}]: Agent found: {1}'.format(self.public_key, agents))
        # 'None' query returns all the resources the prover can propose.
        for agent in agents:
            print('[{0}]: Sending to agent {1}'.format(self.public_key, agent))
            query = None
            self.send_cfp(1, 0, agent, 0, query)
    
    def on_propose(self, max_price: int, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES) -> bool:
        print('[{0}]: Received propose from agent {1}'.format(self.public_key, origin))
        for i, p in enumerate(proposals):
            print('[{0}]: Proposal {1}: {2}'.format(self.public_key, i, p.values))
            if abs(int(p.values['price'])) > max_price:
                print('[{0}]: Declining Propose.'.format(self.public_key))
                self.send_decline(msg_id, dialogue_id, origin, msg_id + 1)
                self.stop()
                return False
        print('[{0}]: Accepting Propose.'.format(self.public_key))
        self.send_accept(msg_id, dialogue_id, origin, msg_id + 1)
        self.stop()
        return True



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
    data_path = '../test/data/iris.json'

    agent = FetchAgent('OV_DLM', oef_addr = '127.0.0.1', oef_port = 3333, metadata = meta, save_path = data_path)
    agent.connect()
    agent.publish()
    print('Service offered.')
    try:
        agent.run()
    finally:
        agent.stop()
        agent.disconnect()
