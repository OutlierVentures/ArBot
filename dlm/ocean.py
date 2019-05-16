from squid_py import Ocean, ConfigProvider, Config

class OceanAgent(Ocean):

    # Everything in init belongs to this instance, everything outside to all instances
    def __init__(self, path_to_config):
        ConfigProvider.set_config(Config(path_to_config))
        Ocean.__init__(self)
    
    # Instance methods take self as an argument
    def get_account(self):
        return self.accounts.list()[0]

    def search(self, terms):
        return self.assets.search(terms)


if __name__ == "__main__":
    oa = OceanAgent('./config.ini')
    print(oa.search('Ocean protocol'))
