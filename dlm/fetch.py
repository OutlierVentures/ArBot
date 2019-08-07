from oef.agents import OEFAgent
from oef.schema import AttributeSchema, DataModel, Description
from oef.messages import CFP_TYPES, PROPOSE_TYPES
from oef.query import Query, Constraint, NotEq
from dlm.utils import Utils
from typing import List
import json, os, time


class FetchAgent(OEFAgent):

    def __init__(self):
        ''' MAIN/TEST ADDRESSES NOT RELEASED YET
        net = os.getenv('NET', '')
        oef = 'oef.economicagents.com' if (net == 'MAIN' or net == 'TEST') else '127.0.0.1'
        '''
        oef = '127.0.0.1'
        OEFAgent.__init__(self, public_key = 'DataBridge', oef_addr = oef, oef_port = 10000)
        self.open_proposals = []
        self.search = []
        
    def fetch_search(self, terms):
        # Reject any old proposals and reset for a new set of proposals
        self.try_respond_n(self.open_proposals, False)
        self.open_proposals = []
        self.save_path = ''
        self.search = []
        search_terms = terms.split(' ')
        self.search = search_terms
        query_array = []
        for term in search_terms:
            query_array.append(Constraint(term, NotEq('')))
        query = Query(query_array)
        self.search_services(0, query)
    
    def fetch_get_search_results(self):
        return self.open_proposals

    # Consumes the cheapest n proposals
    def fetch_consume(self, number_to_consume, save_path):
        self.save_path = save_path
        number_to_consume = int(number_to_consume)
        number_of_proposals = len(self.open_proposals)
        print(number_to_consume, number_of_proposals)
        if number_of_proposals == 0 or number_to_consume <= 0:
            print('No proposals to accept.')
            return False
        if number_to_consume >= number_of_proposals:
            print('Consuming all proposals.')
            result = self.try_respond_n(self.open_proposals, True)
        else:
            print('Consuming ' + str(number_to_consume) + ' proposals.')
            to_accept = self.open_proposals[:(number_to_consume - 1)]
            to_decline = self.open_proposals[number_to_consume:]
            result_accepts = self.try_respond_n(to_accept, True)
            result_declines = self.try_respond_n(to_decline, False)
            result = result_accepts or result_declines
        return result

    def fetch_publish(self, name, description, price, load_path, tags = ['outlier ventures']):
        metadata = { 'base': { 'name': name, 'description': description, 'tags': tags } }
        return self.fetch_publish_from_ocean_meta(metadata, price, load_path)
    
    def fetch_publish_from_ocean_meta(self, metadata, price, load_path):
        try:
            self.service, self.data = self.load_service(metadata, load_path)
            self.price = abs(int(price))
        except Exception as e:
            print('Invalid dataset, metadata or price:', e)
            return False
        try:
            self.register_service(0, self.service)
            return True
        except Exception as e:
            print('Agent has no data or metadata:', e)
            return False
    
    '''
    Only back-end functions from here on.
    '''

    def load_service(self, metadata, load_path):
        dataset_info = metadata['base']
        attributes = description = {}
        for item in dataset_info['tags']:
            attributes[item] = description[item] = 'Tagged: ' + item
        attribute_list = []
        for key, value in attributes.items():
            attribute_list.append(AttributeSchema(key, str, False, value))
        data_model = DataModel(dataset_info['name'], attribute_list, dataset_info['description'])
        service = Description(description, data_model)
        data = Utils.load_json(load_path)
        return service, data

    # on_message is used to receive datasets and datapoints
    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode('utf-8'))
        print('[{0}] Received measurement from {1}: {2}'.format(self.public_key, origin, data))
        # If we've specified that we want to be saving data, then save incoming data.
        # Otherwise we can be bombarded at any time.
        if self.save_path:
            Utils.write_json(data, self.save_path)
        #self.stop()
        return data

    def on_search_result(self, search_id: int, agents: List[str]):
        if len(agents) == 0:
            print('[{}]: No agent found. Stopping...'.format(self.public_key))
            #self.stop()
            return
        print('[{0}]: Agent found: {1}'.format(self.public_key, agents))
        # 'None' query returns all the resources the prover can propose.
        for agent in agents:
            print('[{0}]: Sending to agent {1}'.format(self.public_key, agent))
            query = None
            self.send_cfp(1, 0, agent, 0, query)

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        print('[{0}]: Received CFP from {1}'.format(self.public_key, origin))
        proposal = Description({'price': self.price})
        print('[{}]: Sending propose at price: {}'.format(self.public_key, self.price))
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, proposals = [proposal])

    # Stores proposals in self.open_proposals
    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES) -> bool:
        print('[{0}]: Received propose from agent {1}'.format(self.public_key, origin))
        these_proposals = []
        for i, p in enumerate(proposals):
            print('[{0}]: Proposal {1}: {2}'.format(self.public_key, i, p.values))
            proposal = {
                'categories': self.search,
                'price': abs(int(p.values['price'])),
                'network': 'fetch',
                'ids': {
                    'origin': origin,
                    'msg_id': msg_id,
                    'dialogue_id': dialogue_id
                }
            }
            these_proposals.append(proposal)
        sorted_proposals = sorted(these_proposals, key = lambda k: k['price'])
        self.open_proposals = sorted_proposals

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print('[{0}]: Received accept from {1}.'.format(self.public_key, origin))
        encoded_data = json.dumps(self.data).encode('utf-8')
        print('[{0}]: Sending data to {1}: {2}'.format(self.public_key, origin, self.data))
        self.send_message(0, dialogue_id, origin, encoded_data)
        #self.stop()

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print('[{0}]: Received decline from {1}.'.format(self.public_key, origin))
        #self.stop()

    def try_respond_n(self, proposals, is_accept):
        fail_count = 0
        index = 0
        for proposal in proposals:
            try:
                ids = proposal['ids']
                if is_accept:
                    self.send_accept(ids['msg_id'], ids['dialogue_id'], ids['origin'], ids['msg_id'] + 1)
                    print('Accepting proposal from ' + ids['origin'])
                else:
                    self.send_decline(ids['msg_id'], ids['dialogue_id'], ids['origin'], ids['msg_id'] + 1)
                    print('Declining proposal from ' + ids['origin'])
            except Exception as e:
                fail_count += 1
                print('Failed to respond to proposal from ' + str(index))
                print(e)
            index += 1
        result = True if fail_count != len(proposals) else False
        return result


if __name__ == '__main__':

    fa = FetchAgent()
    fa.connect()
    try:
        fa.run()
    finally:
        fa.stop()
        fa.disconnect()
