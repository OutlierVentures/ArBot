<p align="center">
    <img src="./img/dlm_logo.png" width="200" />
    <br><br>
    The Data Liquidity Module (DLM) facilitates Web 3.0<br>
    data liquidity with Fetch.AI and Ocean Protocol.<br><br>
    <i>An app in the Convergence Stack.</i>
</p>


## Requirements and Install

Requires Linux or MacOS and Docker.

Install: `pip3 install .`

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

### Ocean Protocol to Fetch.AI

```python
from dlm.ocean import OceanAgent
from dlm.fetch import FetchAgent

oa = OceanAgent('path/to/config.ini')
list_of_ddos = oa.ocean_search('flowers')
ddo = list_of_ddos[0]
path_to_data, _ = oa.ocean_consume(ddo)

fa = FetchAgent()
fa.connect()
fa.fetch_publish_from_ocean_meta(oa.get_meta_from_ddo(ddo), path_to_data)
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
fa.fetch_search('flowers', 0, 'desired/download/path.json')
try:
    fa.run()
finally:
    fa.stop()
    fa.disconnect()

oa = OceanAgent('path/to/config.ini')
oa.ocean_publish('Iris Dataset',
                 'Multivariate Iris flower dataset for linear discriminant analysis.',
                 0,
                 'https://pkgstore.datahub.io/machine-learning/iris/iris_json/data/23a7b3de91da915b506f7ca23f6d1141/iris_json.json',
                 'CCO: Public Domain',
                 ['flowers', 'classification', 'plants'])
```


See the `demo` folder for some super simple examples. For a full Ocean -> Fetch -> Ocean flow, run both, `o2f.py` first:

Terminal 1:
```
python3 o2f.py
```
Terminal 2:
```
python3 f2o.py
```

Note that Fetch-side publishing demands JSON-formatted sets.

### Specifying mainnet / testnet / local deployment

By default all components will run locally.

## Components

1. FetchAgent / OceanAgent: push / pull data agents, allowing data onboarding from Fetch to Ocean and vice versa.
2. ArBot: Automated triangular arbitrage with Fetch.AI tokens, Ocean tokens and data. The software executes in cases where the highest bidder on Fetch pays more than the lowest cost of the dataset on Ocean and vice versa.

<p align="center">
    <img src="./img/dlm_stack.png" width="550" />
</p>

## Debugging

Run `pytest` with both nodes running to test. 

`secret_store_client.client.RPCError: Failed to generate server key: Bad Gateway`: the Ocean node is still spinning up. Wait a few minutes.

