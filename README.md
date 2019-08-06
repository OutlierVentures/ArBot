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

oa = OceanAgent('../dlm/config.ini')
results = oa.ocean_search('flowers')
first_result_ddo = results[0]['ddo']
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

oa = OceanAgent('../dlm/config.ini')
oa.ocean_publish(name = 'Iris Dataset',
                 description = 'Multivariate Iris flower dataset for linear discriminant analysis.',
                 price = 0,
                 url = 'https://pkgstore.datahub.io/machine-learning/iris/iris_json/data/23a7b3de91da915b506f7ca23f6d1141/iris_json.json',
                 license = 'CCO: Public Domain',
                 tags = ['flowers', 'classification', 'plants'])
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

Use the environment variable `NET`, setting it to `TEST` or `MAIN` as needed.

## Debugging struct.error: unpack requires a buffer of 4 bytes

Intermittent OEF issue: restart your OEF node. If using the included scripts:
```
cd nodes
./stop_nodes.sh
./start_nodes.sh
```

## Components

1. FetchAgent / OceanAgent: push / pull data agents, allowing data onboarding from Fetch to Ocean and vice versa.
2. ArBot: Automated triangular arbitrage with Fetch.AI tokens, Ocean tokens and data. The software executes in cases where the highest bidder on Fetch pays more than the lowest cost of the dataset on Ocean and vice versa.

<p align="center">
    <img src="./img/dlm_stack.png" width="550" />
</p>

## Debugging

Run `pytest` with both nodes running to test. 

`secret_store_client.client.RPCError: Failed to generate server key: Bad Gateway`: the Ocean node is still spinning up. Wait a few minutes.

