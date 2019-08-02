# API reference

## FetchAgent

```python
from dlm.fetch import FetchAgent
```

Initialise:
```python
fa = FetchAgent(public_key = 'Provider',
                oef_addr = '127.0.0.1', # Use oef.economicagents.com for testnet
                oef_port = 10000,
                load_path = 'data/path.json',
                metadata = DICT_AS_BELOW,
                price = 0)
```
The last three arguments are optional and used to instantiate an agent with a dataset.
Metadata is in the format:
```JSON
{
    "base": {
        "name": "Iris Dataset",
        "description": "Multivariate Iris flower dataset for linear discriminant analysis.",
        "tags": [
            "flowers",
            "classification",
            "plants"
        ]
    }
}
```
An Ocean Protocol metadata object can also be passed to `FetchAgent`.

