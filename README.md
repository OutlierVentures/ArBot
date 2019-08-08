<p align="center">
    <img src="./img/dlm_logo.png" width="200" />
    <br><br>
    Move datasets between Fetch.AI and Ocean Protocol.<br>
    Earn tokens from arbitrage with datasets.<br><br>
    <i>An app in the Convergence Stack.</i>
</p>


## Requirements

- Linux or MacOS
- Docker
- Latest `protobuf`: install binary [from source](https://github.com/protocolbuffers/protobuf/releases)

## Install

```
pip3 install .
pytest
```

## Usage

You will need a running Fetch.AI and Ocean Protocol node. If you don't want to set these up yourself:
```
cd nodes
```
Then use any of the following as appropriate:
```
./get_nodes.sh
./start_nodes.sh
./stop_nodes.sh
```
These need to be run from the `nodes` folder.

**Note that for publishing on Ocean, which is a requirement of the data arbitrage component, you will need to host your own data. This means spinning up a webserver with a publicly accessible URL - see any function arguments marked URL. The simplest solution is a [plain nginx server](https://nginxconfig.io/?0.index=index.html&0.fallback_html), just hosting any sets at the top level.**

Fetch-side publishing demands JSON-formatted sets.


### Ocean Protocol to Fetch.AI

```python
from dlm.ocean import OceanAgent
from dlm.fetch import FetchAgent

oa = OceanAgent('/path/to/ocean/config.ini')
results = oa.ocean_search('flowers')
first_result_ddo = results[0]['ids']['ddo']
path_to_data, _ = oa.ocean_consume(first_result_ddo)

fa = FetchAgent()
fa.connect()
fa.fetch_publish_from_ocean_meta(metadata = oa.ocean_get_meta_from_ddo(first_result_ddo),
                                 price = 0,
                                 load_path = path_to_data)
try:
    fa.run()
finally:
    fa.stop()
    fa.disconnect()
```

### Fetch.AI to Ocean Protocol

```python
from dlm.fetch import FetchAgent
from dlm.ocean import OceanAgent

fa = FetchAgent()
fa.connect()
fa.fetch_search('flowers')
search_results = fa.fetch_get_search_results()
fa.fetch_consume(number_to_consume = 1, save_path = './')
try:
    fa.run()
finally:
    fa.stop()
    fa.disconnect()

oa = OceanAgent('/path/to/ocean/config.ini')
oa.ocean_publish(name = 'Iris Dataset',
                 description = 'Multivariate Iris flower dataset for linear discriminant analysis.',
                 price = 0,
                 url = 'https://mywebserverurl.io/iris.json',
                 license = 'CCO: Public Domain',
                 tags = ['flowers', 'classification', 'plants'])
```


### Arbitrage

```python
from dlm.arbot import ArBot

ab = ArBot('/path/to/ocean/config.ini', '/path/to/webserver/root', 'https://yourhosting.url')
ab.arb('iris categorical')
```

### Examples

See the `demo` folder for some super simple examples.

For a full Ocean -> Fetch -> Ocean flow:

Terminal 1:
```
python3 o2f.py
```
Terminal 2:
```
python3 f2o.py
```

### Specifying mainnet / testnet / local deployment

By default all components will run locally.

Use the environment variable `NET`, setting it to `TEST` or `MAIN` as needed.

## Components

1. FetchAgent / OceanAgent: push / pull data agents, allowing data onboarding from Fetch to Ocean and vice versa.
2. ArBot: Automated triangular arbitrage with Fetch.AI tokens, Ocean tokens and data. The software executes in cases where the highest bidder on Fetch pays more than the lowest cost of the dataset on Ocean and vice versa.

<p align="center">
    <img src="./img/dlm_stack.png" width="550" />
</p>

## Debugging

Run `pytest` with both nodes running to test. Ensure

`secret_store_client.client.RPCError: Failed to generate server key: Bad Gateway`: the Ocean node is still spinning up. Wait a few minutes.

`requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=8545): Max retries exceeded with url`: as above.

`struct.error: unpack requires a buffer of 4 bytes`: Intermittent OEF issue - restart your OEF node. If using the included scripts:
```
cd nodes
./stop_nodes.sh
./start_nodes.sh
```

