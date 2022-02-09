## Introduction

The exchange platform [Kraken](https://www.kraken.com) allows to trade cryptocurrencies and
some other features.

This library tries to implement most of the methods of the 
[Kraken API](https://docs.kraken.com/rest).
It uses the well done library [krakenex](https://github.com/veox/python3-krakenex) to make 
the queries.

## Implementation

### Methods detailed

All __API__ methods have the _query_ word prefixed, that is for te __API__ method
_QueryTrades_ there is the corresponding function `query_query_trades` and for the method
_AddOrder_ there is the correspoding function `query_add_order`. 

### Instance of `Kapi`

To create an instance of `Kapi` simply do:
```python
import kraken_api                            
from kraken_api import Kapi

kapi = Kapi()  
```

The `__init__` parameters are:
  - `test_session`: if it is to be a test session or not, this will by default 
  __only validate and not post orders__
  - `account_type`: your type of account if connecting to your use account in kraken,
  three types are possibles (this will affect certain API calls parameters):
    - `"starter"`
    - `"intermediate"`
    - `"pro"`
  - `key` and `secret`: if you are effectively connecting to your kraken account then
  you must

### Return form

Whenever possible (_and useful_) the returnded information is given in form of a 
[pandas](https://pandas.pydata.org) _dataframe_.



### API methods implemented
- Public
  - [x] Time
  - [x] SystemStatus
  - [x] Assets
  - [x] AssetPairs
  - [x] Ticker
  - [x] OHLC
  - [x] Depth
  - [x] Trades
  - [x] Spread
- Private
  - User Data:
    - [x] Balance
    - [x] TradeBalance
    - [x] OpenOrders
    - [x] ClosedOrders
    - [x] QueryOrders
    - [x] TradesHistory
    - [x] QueryTrades
    - [] OpenPositions (__to be tested__)
    - [] Ledgers
    - [] QueryLedgers
    - [] TradeVolume
    - [] AddExport
    - [] ExportStatus
    - [] RetrieveExport
    - [] RemoveExport
  - User Trading:
    - [x] AddOrder
    - [x] CancelOrder
    - [] CancelAll
    - [] CancelAllOrdersAfter
  - User Funding:
    - ...
  - User Staking:
    - ...
  - Websockets Authentication
    - ...
  
    