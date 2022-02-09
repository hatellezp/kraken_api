### Documentation for the krapi library.

This library is a convenient wrapper over the krakenex lib to communicate with
the Kraken Crypto exchange platform.

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
  
    