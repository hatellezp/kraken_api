Introduction
============

The exchange platform Kraken_ allows to trade cryptocurrencies and
some other features.

This library tries to implement most of the methods of the `Kraken API`_.
It uses the well done library krakenex_  to make the queries.

.. _Kraken: https://www.kraken.com
.. _Kraken API: https://docs.kraken.com/rest
.. _krakenex: https://github.com/veox/python3-krakenex

Implementation
==============

Methods detailed
----------------

All **API** methods have the *query* word prefixed, that is, for te **API** method
*QueryTrades* there is the corresponding function ``query_query_trades`` and for
the method *AddOrder* there is the corresponding function ``query_add_order``.

Instance of `Kapi`
------------------

To create an instance of `Kapi` simply do:
.. code::

    import kraken_api
    from kraken_api import Kapi
    kapi = Kapi()

The ``__init__`` parameters are:
    * `test_session`: if it is to be a test session or not, this will by default **only validate and not post orders**
    * `account_type`: your type of account if connecting to your use account in kraken, three types are possibles (this will affect certain API calls parameters):
        * `"starter"`
        * `"intermediate"`
        * `"pro"`
    * `key` and `secret`: if you are effectively connecting to your kraken account then you must generate an API key for this library to connect to Kraken.

### Return form

Whenever possible (_and useful_) the returnded information is given in form of a 
[pandas](https://pandas.pydata.org) _dataframe_.
The call

```python
import kraken_api
from kraken_api import Kapi 

kapi = Kapi()

result = kapi.query_asset_pairs()
```

will produce an answer alike to this:

```jupyterpython
      altname     wsname aclass_base   base  ... fee_volume_currency margin_call margin_stop ordermin
0    1INCHEUR  1INCH/EUR    currency  1INCH  ...                ZUSD          80          40        1
1    1INCHUSD  1INCH/USD    currency  1INCH  ...                ZUSD          80          40        1
2     AAVEAUD   AAVE/AUD    currency   AAVE  ...                ZUSD          80          40     0.02
3     AAVEETH   AAVE/ETH    currency   AAVE  ...                ZUSD          80          40     0.02
4     AAVEEUR   AAVE/EUR    currency   AAVE  ...                ZUSD          80          40     0.02
..        ...        ...         ...    ...  ...                 ...         ...         ...      ...
430    ZRXGBP    ZRX/GBP    currency    ZRX  ...                ZUSD          80          40        5
431    ZRXUSD    ZRX/USD    currency    ZRX  ...                ZUSD          80          40        5
432    ZRXXBT    ZRX/XBT    currency    ZRX  ...                ZUSD          80          40        5
433    USDCAD    USD/CAD    currency   ZUSD  ...                ZUSD          80          40       10
434    USDJPY    USD/JPY    currency   ZUSD  ...                ZUSD          80          40       10

```



### API methods implemented
Go see the [documentaion](https://docs.kraken.com/rest) for a full description of each
API call.

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
  
    