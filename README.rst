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

All **API** methods have the same names as the Kraken API, that is, for the **API** method
*QueryTrades* there is the corresponding function ``query_trades`` and for
the method *AddOrder* there is the corresponding function ``add_order``.

Instance of `Kapi`
------------------

To create an instance of `Kapi` simply do:

.. code::

    import kraken_api
    from kraken_api import Kapi
    kapi = Kapi()


The ``__init__`` parameters are:

* `test_session`: if it is to be a test session or not, this will by default only **validate** and not post orders
* `account_type`: your type of account if connecting to your use account in kraken, three types are possibles (this will affect certain API calls parameters):
    * ``"starter"``
    * ``"intermediate"``
    * ``"pro"``
* ``key`` and ``secret``: if you are effectively connecting to your kraken account then you must generate an API key for this library to connect to Kraken.

Return form
-----------

Whenever possible (*and useful*) the returned information is given in form of a
pandas_ *dataframe*.

.. _pandas : https://pandas.pydata.org

The call

.. code::

    import kraken_api
    from kraken_api import Kapi

    kapi = Kapi()
    result = kapi.asset_pairs()

will produce an answer alike to this:

.. code::

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


API methods implemented
-----------------------
Go see the documentation_ for a full description of each API call.

.. _documentation: https://docs.kraken.com/rest


.. |check| raw:: html

    <input checked=""  type="checkbox">

.. |check_| raw:: html

    <input checked=""  disabled="" type="checkbox">

.. |uncheck| raw:: html

    <input type="checkbox">

.. |uncheck_| raw:: html

    <input disabled="" type="checkbox">


* Public
    * |check| Time
    * |check| SystemStatus
    * |check| Assets
    * |check| AssetPairs
    * |check| Ticker
    * |check| OHLC
    * |check| Depth
    * |check| Trades
    * |check| Spread
* Private
    * User Data:
        * |check| Balance
        * |check| TradeBalance
        * |check| OpenOrders
        * |check| ClosedOrders
        * |check| QueryOrders
        * |check| TradesHistory
        * |check| QueryTrades
    * User Trading:
        * |check| AddOrder
        * |check| CancelOrder
        * |uncheck| CancelAll
        * |uncheck| CancelAllOrdersAfter
    * User Funding:
        * ...
    * User Staking:
        * ...
    * Websockets Authentication
        * ...


In development
--------------

* all missing methods
* an api and rate counter to allow know if we are near the limit, see `rate limits`_
* tests for each method
* correctly parsing of errors returned by Kraken

.. _rate limits: https://docs.kraken.com/rest/#section/Rate-Limits
    