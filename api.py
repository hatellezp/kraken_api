import krakenex
import pandas as pd
import time

# documentation for:
# - krakenex: https://python3-krakenex.readthedocs.io/en/stable/
# - kraken: https://docs.kraken.com/rest/


class Kapi:

    def __init__(
            self,
            max_amount,
            test_session=True,
            account_type="starter",
            key="",
            secret=""):
        """
        in fact all functions work in the same way, if the Kapi
        object is not live, each function will make a call to
        connection

        :param live_connection:
        :param test_session:
        :param max_amount: max amount allowed to use for trade
        :param key: the key used for kraken authentication
        :param secret: the secret used for kraken authentication
        """

        if account_type not in ["starter", "intermediate", "pro"]:
            raise Exception(
                f"Invalid parameter for account_type: {account_type}")

        if not isinstance(max_amount, int) and not isinstance(
                max_amount, float):
            raise Exception(f"Invalid parameter for max_amount: {max_amount}")

        if not isinstance(test_session, bool):
            raise Exception(
                f"Invalid parameter for test_section: {test_session}")

        self._api = krakenex.API(key, secret)
        self._test_session = test_session
        self._max_amount = max_amount
        self._account_type = account_type

        self._max_api_counter = {
            "starter": 15,
            "intermediate": 20,
            "pro": 20,
        }[self._account_type]
        self._api_call_counter = 0

        self._max_num_orders = {
            "starter": 60,
            "intermediate": 80,
            "pro": 225,
        }[self._account_type]
        self._order_counter = 0

        self._max_rate_count = {
            "starter": 60,
            "intermediate": 125,
            "pro": 180,
        }[self._account_type]
        self._order_rate_counter = 0

        self._api_counter_decay = {
            "starter": 0.33,
            "intermediate": 0.5,
            "pro": 1.,
        }[self._account_type]

        self._ratecount_decay = {
            "starter": 1.,
            "intermediate": 2.34,
            "pro": 3.75,
        }[self._account_type]

        self._last_pair_used = None
        self._last_query_time = None

    def _update_counters(self, type_query, pair=None):
        if type_query not in ["ledge/trade",
                              "add_order", "other", "cancel_order"]:
            raise Exception(f"Invalid type query parameter: {type_query}")

        if type_query == ["cancel_order", "add_order"] and pair is None:
            raise Exception(f"You must provide a pair when adding or cancelling orders")

        if self._last_query_time is None:
            self._last_query_time = time.time()
            return

        last_last_time = self._last_query_time
        self._last_query_time = time.time()
        delta = self._last_query_time - last_last_time

        self._api_call_counter -= delta * self._api_counter_decay
        self._order_rate_counter -= delta * self._ratecount_decay

        if type_query in ["add_order", "cancel_order"]:
            self._order_counter += 1

        if type_query == "ledge/trade":
            self._api_call_counter += 2
        elif type_query == "other":
            self._api_call_counter += 1
        elif type_query == "add_order":
            self._order_rate_counter += 1
        elif type_query == "cancel_order" and pair is not None:
            if self._last_pair_used is None or self._last_pair_used != pair:
                self._last_pair_used = pair
                return
            else:
                augment = 0
                if delta < 5:
                    augment = 8
                elif delta < 10:
                    augment = 6
                elif delta < 15:
                    augment = 5
                elif delta < 45:
                    augment = 4
                elif delta < 90:
                    augment = 2
                elif delta < 300:
                    augment = 1

                self._order_rate_counter += augment



    # wrapper over all other public query methods
    def _public_query(self, method, data=None):
        """

        :param method: method asked to kraken: Ticker, Assets,...
        :param data: data passed to the method as asset pair
        :return: the error else the result wrapped in a dict
        """
        res = self._api.query_public(method, data)

        if res["error"]:
            return res["error"]
        else:
            return {"result": res["result"]}

    def _private_query(self, method, data=None):
        res = self._api.query_private(method, data)

        if res["error"]:
            return res["error"]
        else:
            return {"result": res["result"]}

    # ===========================================================================
    # these are all the market data methods of the kraken api

    def query_time(self):
        res = self._public_query("Time")
        self._update_counters("other")
        return res

    def query_system_status(self):
        res = self._public_query("SystemStatus")
        self._update_counters("other")
        return res

    def query_assets(self, asset=None, aclass="currency"):
        """
        Get information about the assets that are available for deposit,
        withdrawal, trading and staking.
        :param asset: a particular pair to get the info on or a list of pairs,
                      if None is passed then gets all pairs
        :return: a data frame with the information:
        """
        data = {"aclass": aclass}

        if asset is not None:
            data["pair"] = output_or_join_list(asset)

        res = self._public_query("Assets", data=data)
        self._update_counters("other")

        if "result" in res:
            columns = [
                "cryptocurrency",
                "aclass",
                "altname",
                "decimals",
                "display_decimals"]
            data = pd.DataFrame(columns=columns)
            data_raw = res["result"]
            for currency in data_raw:
                inner_df = pd.DataFrame([[
                    currency.startswith("X"),
                    data_raw[currency]["aclass"],
                    data_raw[currency]["altname"],
                    data_raw[currency]["decimals"],
                    data_raw[currency]["display_decimals"],
                ]], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            return data
        else:
            return res

    def query_asset_pairs(self, pair=None, info="info"):
        """

        :param pair: a list of pairs to get info on or a lone pair as a string,
                     if None is provided it defaults to get for all the pairs
        :return: a dataframe with all the info
        """

        if info not in ["info", "leverage", "fees", "margin"]:
            raise Exception(f"Invalid parameter for info: {info}")
        data = {"info": info}

        if pair is not None:
            data["pair"] = output_or_join_list(pair)

        res = self._public_query("AssetPairs", data)
        self._update_counters("other")

        if "result" in res:
            columns = [
                "altname",
                "wsname",
                "aclass_base",
                "base",
                "aclass_quote",
                "quote",
                "lot",
                "pair_decimals",
                "lot_decimals",
                "lot_multiplier",
                "fees_0",
                "fees_50000",
                "fees_100000",
                "fees_250000",
                "fees_1000000",
                "fees_maker_0",
                "fees_maker_50000",
                "fees_maker_100000",
                "fees_maker_250000",
                "fees_maker_1000000",
                "fee_volume_currency",
                "margin_call",
                "margin_stop",
                "ordermin"]

            data = pd.DataFrame(columns=columns)
            data_raw = res["result"]

            for currency in data_raw:
                inner_df = pd.DataFrame([[
                    data_raw[currency]["altname"],
                    data_raw[currency]["wsname"],
                    data_raw[currency]["aclass_base"],
                    data_raw[currency]["base"],
                    data_raw[currency]["aclass_quote"],
                    data_raw[currency]["quote"],
                    data_raw[currency]["lot"],
                    data_raw[currency]["pair_decimals"],
                    data_raw[currency]["lot_decimals"],
                    data_raw[currency]["lot_multiplier"],
                    data_raw[currency]["fees"][0][1],
                    data_raw[currency]["fees"][1][1],
                    data_raw[currency]["fees"][2][1],
                    data_raw[currency]["fees"][3][1],
                    data_raw[currency]["fees"][4][1],
                    data_raw[currency]["fees_maker"][0][1],
                    data_raw[currency]["fees_maker"][1][1],
                    data_raw[currency]["fees_maker"][2][1],
                    data_raw[currency]["fees_maker"][3][1],
                    data_raw[currency]["fees_maker"][4][1],
                    data_raw[currency]["fee_volume_currency"],
                    data_raw[currency]["margin_call"],
                    data_raw[currency]["margin_stop"],
                    data_raw[currency]["ordermin"],
                ]], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            return data
        else:
            return res

    def query_ticker(self, pair):
        """

        :param pair: a pair to get the current ticker info on
        :return: a dataframe with the info
        """
        res = self._public_query("Ticker", {"pair": pair})
        self._update_counters("other")

        if "result" in res:
            columns = [
                "ask",
                "ask_whole_lot_volume",
                "ask_lot_volume",
                "bid",
                "bid_whole_lot_volume",
                "a_lot_volume",
                "last_trade_closed_price",
                "last_trade_closed_lot_volume",
                "volume_today",
                "volume_last_24_hours",
                "wa_volume_price_today",
                "wa_volume_price_last_24_hours",
                "number_of_trades_today",
                "number_of_trades_last_24_hours",
                "low_today",
                "low_last_24_hours",
                "high_today",
                "high_last_24_hours",
                "today_opening_price",
            ]

        data = pd.DataFrame(columns=columns)
        data_raw = res["result"]

        for currency in data_raw:
            inner_df = pd.DataFrame([[
                data_raw[currency]["a"][0],
                data_raw[currency]["a"][1],
                data_raw[currency]["a"][2],
                data_raw[currency]["b"][0],
                data_raw[currency]["b"][1],
                data_raw[currency]["b"][2],
                data_raw[currency]["c"][0],
                data_raw[currency]["c"][1],
                data_raw[currency]["v"][0],
                data_raw[currency]["v"][1],
                data_raw[currency]["p"][0],
                data_raw[currency]["p"][1],
                data_raw[currency]["t"][0],
                data_raw[currency]["t"][1],
                data_raw[currency]["l"][0],
                data_raw[currency]["l"][1],
                data_raw[currency]["h"][0],
                data_raw[currency]["h"][1],
                data_raw[currency]["o"],
            ]], columns=columns)
            data = pd.concat([data, inner_df], ignore_index=True)

            return data
        else:
            return res

    def query_ohlc(self, pair, interval=1, since=None):
        """

        :param pair: pair to the the OHLC data on
        :param since: get the data since given 'since' ID, defaults to max

        :return: a tuple (a dataframe with the result, time of last commit OHLC)
        """
        if int(interval) not in [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]:
            raise Exception(f"Invalid interval for query: {interval}")

        data = {"pair": pair, "interval": interval}
        if since is not None:
            data["since"] = since

        res = self._public_query("OHLC", data=data)
        self._update_counters("other")

        if "result" in res:
            columns = [
                "pair",
                "time",
                "open",
                "high",
                "low",
                "close",
                "vwap",
                "volume",
                "count"
            ]

            data = pd.DataFrame(columns=columns)
            data_raw = res["result"][pair]
            last = res["result"]["last"]

            for currency in data_raw:
                inner_df = pd.DataFrame([[
                    pair,
                    currency[0],
                    currency[1],
                    currency[2],
                    currency[3],
                    currency[4],
                    currency[5],
                    currency[6],
                    currency[7]
                ]], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            return data, last
        else:
            return res

    def query_depth(self, pair, count=100):
        """
        get the order book for a given pair

        :param pair: the pair to get the order book on
        :param count: number of orders to get, defaults to 100

        :return: a dataframe with the info in
        """
        if not 1 <= count <= 500:
            raise Exception(
                f"Invalid count parameter, count must be in the invterval [1, 500], count provided: {count}")

        data = {"pair": pair, "count": count}

        res = self._public_query("Depth", data=data)
        self._update_counters("other")

        if "result" in res:
            columns = [
                "pair",
                "time",
                "ask_price",
                "ask_volume",
                "bid_price",
                "bid_volume"
            ]

            data = pd.DataFrame(columns=columns)
            data_raw = res["result"][pair]
            asks = data_raw["asks"]
            bids = data_raw["bids"]

            asks.sort(key=lambda x: x[2])
            bids.sort(key=lambda x: x[2])

            for index in range(len(asks)):
                values = [
                    pair,
                    asks[index][2],
                    asks[index][0],
                    asks[index][1],
                    bids[index][0],
                    bids[index][1],
                ]
                inner_df = pd.DataFrame([values], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            return data
        else:
            return res

    def query_trades(self, pair, since=None):
        """

        return the last trades (last 1000 trades by default)
        :param pair: the pair to get the trades on
        :param since: return the trades since the given timestamp
        """

        data = {"pair": pair}
        if since is not None:
            data["since"] = since

        res = self._public_query("Trades", data=data)
        self._update_counters("other")

        if "result" in res:
            columns = [
                "pair",
                "time",
                "volume",
                "price",
                "is_sell",
                "is_buy",
                "market_limit",
                "miscellaneous",
            ]

            data = pd.DataFrame(columns=columns)
            data_raw = res["result"][pair]
            last = res["result"]["last"]

            for li in data_raw:
                values = [
                    pair,
                    li[2],
                    li[1],
                    li[0],
                    "s" in li,
                    "b" in li,
                    li[4],
                    li[5]
                ]

                inner_df = pd.DataFrame([values], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            return data, last
        else:
            return res

    def query_spread(self, pair, since=None):
        """

        :param pair: the asset pair to get the data on
        :param since: return the spread data since 'since'

        :return: a tuple(a dataframe wit the info on, the time of the last item)
        """

        data = {"pair": pair}
        if since is not None:
            data["since"] = since

        res = self._public_query("Spread", data=data)
        self._update_counters("other")

        if "result" in res:
            columns = [
                "pair",
                "time",
                "bid",
                "ask",
            ]

            data = pd.DataFrame(columns=columns)
            data_raw = res["result"][pair]
            last = res["result"]["last"]

            for li in data_raw:
                values = [
                    pair,
                    li[0],
                    li[1],
                    li[2],
                ]

                inner_df = pd.DataFrame([values], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            return data, last
        else:
            return res

    # ==========================================================================
    # query user data

    def query_balance(self):
        """

        get the balance of the account in a data frame
        :return: a dataframe
        """
        res = self._private_query("Balance")
        self._update_counters("other")

        if "result" in res:
            columns = [
                "currency",
                "amount",
            ]

            data = pd.DataFrame(columns=columns)
            data_raw = res["result"]

            for currency in data_raw:
                inner_df = pd.DataFrame([[
                    currency,
                    data_raw[currency]
                ]], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            return data
        else:
            return res

    def query_trade_balance(self, asset="ZEUR"):
        """

        :param asset: the asset to get the trade info on
        :return: a dataframe
        """

        # the default is "ZUSD" but me I'm more interested in "ZEUR"
        res = self._private_query("TradeBalance", data={"asset": asset})
        self._update_counters("other")

        if "result" in res:
            columns = [
                "eb",
                "tb",
                "m",
                "n",
                "c",
                "v",
                "e",
                "mf",
            ]

            column_names = [
                "equivalent_balance",
                "trade_balance",
                "margin",
                "unrealized_profit_loss",
                "cost_basis_open",
                "current_floating_valuation_open",
                "equity",
                "free_margin",
            ]

            data = pd.DataFrame(columns=column_names)
            data_raw = res["result"]

            to_append = [data_raw[column] for column in columns]
            inner_df = pd.DataFrame([
                to_append
            ], columns=column_names)
            data = pd.concat([data, inner_df], ignore_index=True)

            return data
        else:
            return res

    def query_open_orders(self, trades=False, userref=None):
        """

        get info on the current open orders
        :param trades: to include trades if available
        :param userref: restrict results ot given user reference id

        :return: a dataframe of transactions
        """
        if trades not in [False, True] or not is_none_or_type(userref, int):
            raise Exception(f"Invalid parameters : {trades}, {userref}")

        data = {"trades": str(trades).lower()}
        if userref is not None:
            data["userref"] = userref

        res = self._private_query("OpenOrders", data=data)
        self._update_counters("other")

        if "result" in res:
            columns = [
                "order_id",
                "refid",
                "userref",
                "status",
                "opentm",
                "starttm",
                "expiretim",
                "pair",
                "type",
                "order_type",
                "price",
                "price_2",
                "leverage",
                "order",
                "close",
                "volume",
                "volume_executed",
                "cost",
                "fee",
                "price",
                "stop_price",
                "limit_price",
                "misc",
                "oflags"
            ]

            data = pd.DataFrame(columns=columns)
            data_raw = res["result"]["open"]

            for order in data_raw:
                values = [
                    order,
                    data_raw[order]["refid"],
                    data_raw[order]["userref"],
                    data_raw[order]["status"],
                    data_raw[order]["opentm"],
                    data_raw[order]["starttm"],
                    data_raw[order]["expiretm"],
                    data_raw[order]["descr"]["pair"],
                    data_raw[order]["descr"]["type"],
                    data_raw[order]["descr"]["ordertype"],
                    data_raw[order]["descr"]["price"],
                    data_raw[order]["descr"]["price2"],
                    data_raw[order]["descr"]["leverage"],
                    data_raw[order]["descr"]["order"],
                    data_raw[order]["descr"]["close"],
                    data_raw[order]["vol"],
                    data_raw[order]["vol_exec"],
                    data_raw[order]["cost"],
                    data_raw[order]["fee"],
                    data_raw[order]["price"],
                    data_raw[order]["stopprice"],
                    data_raw[order]["limitprice"],
                    data_raw[order]["misc"],
                    data_raw[order]["oflags"],
                ]

                inner_df = pd.DataFrame([values], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            return data
        else:
            return res

    def query_closed_orders(
            self,
            trades=False,
            userref=None,
            start=None,
            end=None,
            ofs=None,
            closetime="both"):
        """

        get the info on the closed orders
        :param trades: to include trades or not
        :param userref: restrict to given user reference id
        :param start: starting unit timestamp or order tx (exclusive)
        :param end: ending unix timestamp or order tx (inclusive)
        :param ofs: result offset for pagination
        :param: closetime: wich time to use to search ("both", "open", "close")
        """
        if (trades not in [False, True] or
                not is_none_or_type(userref, int) or
                not is_none_or_type(start, int) or
                not is_none_or_type(end, int) or
                not is_none_or_type(ofs, int) or
                closetime not in ["both", "open", "close"]):
            raise Exception(f"Invalid parameter, please verify: {trades}, {userref}, {start}, {end}, {ofs}, {closetime}")

        data = {"trades": str(trades).lower(), "closetime": closetime}

        if userref is not None:
            data["userref"] = userref
        if start is not None:
            data["start"] = start
        if end is not None:
            data["end"] = start
        if ofs is not None:
            data["ofs"] = ofs

        res = self._private_query("ClosedOrders", data=data)
        self._update_counters("other")

        if "result" in res:
            columns = [
                "order_id",
                "refid",
                "userref",
                "reason",
                "status",
                "opentm",
                "starttm",
                "expiretim",
                "pair",
                "type",
                "order_type",
                "price",
                "price_2",
                "leverage",
                "order",
                "close",
                "volume",
                "volume_executed",
                "cost",
                "fee",
                "price",
                "stop_price",
                "limit_price",
                "misc",
                "oflags"
            ]

            data = pd.DataFrame(columns=columns)
            data_raw = res["result"]["closed"]

            for order in data_raw:
                values = [
                    order,
                    data_raw[order]["refid"],
                    data_raw[order]["userref"],
                    data_raw[order]["status"],
                    data_raw[order]["reason"],
                    data_raw[order]["opentm"],
                    data_raw[order]["starttm"],
                    data_raw[order]["expiretm"],
                    data_raw[order]["descr"]["pair"],
                    data_raw[order]["descr"]["type"],
                    data_raw[order]["descr"]["ordertype"],
                    data_raw[order]["descr"]["price"],
                    data_raw[order]["descr"]["price2"],
                    data_raw[order]["descr"]["leverage"],
                    data_raw[order]["descr"]["order"],
                    data_raw[order]["descr"]["close"],
                    data_raw[order]["vol"],
                    data_raw[order]["vol_exec"],
                    data_raw[order]["cost"],
                    data_raw[order]["fee"],
                    data_raw[order]["price"],
                    data_raw[order]["stopprice"],
                    data_raw[order]["limitprice"],
                    data_raw[order]["misc"],
                    data_raw[order]["oflags"],
                ]

                inner_df = pd.DataFrame([values], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            return data
        else:
            return res

    def query_query_orders(self, txid, trades=False, userref=None):
        """
        retrieve information about specific orders

        :param trades: to onluce trades related to the position or not
        :param userref: restrict results to user reference id
        :txid: comma delimited transaction ids (MAXIMUM 50)

        :return: a dataframe
        """

        if trades not in [False, True] or not is_none_or_type(userref, int):
            raise Exception(f"Invalid parameters: {trades}, {userref}")

        if not isinstance(txid, str) and not isinstance(txid, list):
            raise Exception(
                f"Invalid parameter txid: {txid}, must be list or string")

        txid_parsed = output_or_join_list(txid)

        data = {"txid": txid_parsed, "trades": str(trades).lower()}

        if userref is not None:
            data["userref"] = userref

        res = self._private_query("QueryOrders", data=data)
        self._update_counters("other")

        if "result" in res:
            columns = [
                "order_id",
                "refid",
                "userref",
                "status",
                "opentm",
                "starttm",
                "expiretim",
                "pair",
                "type",
                "order_type",
                "price",
                "price_2",
                "leverage",
                "order",
                "close",
                "volume",
                "volume_executed",
                "cost",
                "fee",
                "price",
                "stop_price",
                "limit_price",
                "misc",
                "oflags"
            ]

            data = pd.DataFrame(columns=columns)
            data_raw = res["result"]

            for order in data_raw:
                values = [
                    order,
                    data_raw[order]["refid"],
                    data_raw[order]["userref"],
                    data_raw[order]["status"],
                    data_raw[order]["opentm"],
                    data_raw[order]["starttm"],
                    data_raw[order]["expiretm"],
                    data_raw[order]["descr"]["pair"],
                    data_raw[order]["descr"]["type"],
                    data_raw[order]["descr"]["ordertype"],
                    data_raw[order]["descr"]["price"],
                    data_raw[order]["descr"]["price2"],
                    data_raw[order]["descr"]["leverage"],
                    data_raw[order]["descr"]["order"],
                    data_raw[order]["descr"]["close"],
                    data_raw[order]["vol"],
                    data_raw[order]["vol_exec"],
                    data_raw[order]["cost"],
                    data_raw[order]["fee"],
                    data_raw[order]["price"],
                    data_raw[order]["stopprice"],
                    data_raw[order]["limitprice"],
                    data_raw[order]["misc"],
                    data_raw[order]["oflags"],
                ]

                inner_df = pd.DataFrame([values], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            return data
        else:
            return res

    def query_trades_history(
            self,
            type="all",
            trades=False,
            start=None,
            end=None,
            ofs=None):
        """
        retrive information about trades/fills 50 results are returned at a
        time

        :param type: type of trade ("any position", "closed position",
                                    "closing position", "no position", "all")
                                    default is all
        :param trades: to include trades or not
        :param start: starting unix timestamp or trade ID (exclusive)
        :param end: ending unix timestamp or trade ID (inclusive)
        :param ofs: result offset for pagination

        :return: a dataframe
        """

        if type not in [
                "all",
                "any position",
                "closed position",
                "closing position",
                "no position"] or trades not in [
                False,
                True] or not is_none_or_type(
                start,
                int) or not is_none_or_type(
                    end,
                    int) or not is_none_or_type(
                        ofs,
                int):
            raise Exception(f"Invalid parameters: {type}, {trades}, {start}, {end}, {ofs}")

        data = {"trades": str(trades).lower(), "type": type}
        if start is not None:
            data["start"] = start
        if end is not None:
            data["end"] = end
        if ofs is not None:
            data["ofs"] = ofs

        res = self._private_query("TradesHistory", data=data)
        self._update_counters("ledger/trade")

        if "result" in res:
            data_raw = res["result"]["trades"]
            count = res["result"]["count"]

            columns = [
                "trade_id",
                "ordertxid",
                "postxid",
                "pair",
                "time",  # I'm going to cast to int !!!
                "type",
                "ordertype",
                "price",
                "cost",
                "fee",
                "vol",
                "margin",
                "misc"
            ]

            data = pd.DataFrame(columns=columns)

            for trade in data_raw:
                values = [trade]
                values.extend([
                    (data_raw[trade][column] if column in data_raw[trade] else None) for column in columns if column != "trade_id"])

                inner_df = pd.DataFrame([values], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            data = data.rename(columns={"ordertxid": "order_id"})
            data["time"] = data["time"].apply(int)

            return data, count
        else:
            return res

    def query_query_trades(self, txid, trades=False):
        """
        retrieve information about specific trades/fills

        :param txid: tx ot get info about
        :param trades: include or not the trades
        :return: a dataframe
        """
        if trades not in [False, True]:
            raise Exception(f"Invalid 'trades' parameter: {trades}")

        txid_parsed = output_or_join_list(txid)

        data = {"txid": txid_parsed, "trades": str(trades).lower()}
        res = self._private_query("QueryTrades", data=data)
        self._update_counters("other")

        if "result" in res:
            data_raw = res["result"]

            columns = [
                "trade_id",
                "ordertxid",
                "postxid",
                "pair",
                "time",  # I'm going to cast to int !!!
                "type",
                "ordertype",
                "price",
                "cost",
                "fee",
                "vol",
                "margin",
                "misc"
            ]

            data = pd.DataFrame(columns=columns)

            for trade in data_raw:
                values = [trade]
                values.extend([
                    (data_raw[trade][column] if column in data_raw[trade] else None) for column in columns if
                    column != "trade_id"])

                inner_df = pd.DataFrame([values], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            data = data.rename(columns={"ordertxid": "order_id"})
            data["time"] = data["time"].apply(int)

            return data
        else:
            return res

    def query_open_positions(self, txid, docalcs=False,
                             consolidation="market"):
        """
        get information about open margin positions

        :param txid: transactions to which limit the output to
        :param docalcs: wheter to include P&L calculations
        :param consolidation: consolidate positions by market/pair
        """

        if docalcs not in [False, True] or consolidation not in [
                "market", "pair"]:
            raise Exception(f"Invalid parameters {docalcs}, {consolidation}")

        data = {
            "txid": output_or_join_list(txid),
            "docalcs": str(docalcs).lower(),
            "consolidation": consolidation,
        }

        res = self._private_query("OpenPositions", data=data)
        self._update_counters("other")

        if "result" in res:
            data_raw = res["result"]

            columns = [
                "trade_id",
                "ordertxid",
                "posstatus",
                "pair",
                "time",
                "type",
                "ordertype",
                "cost",
                "fee",
                "vol",
                "vol_closed",
                "margin",
                "value",
                "net",
                "terms",
                "rollovterm",
                "misc",
                "oflags"
            ]

            data = pd.DataFrame(columns=columns)

            for trade in data_raw:
                values = [trade]
                values.extend([
                    (data_raw[trade][column] if column in data_raw[trade] else None) for column in columns if
                    column != "trade_id"])

                inner_df = pd.DataFrame([values], columns=columns)
                data = pd.concat([data, inner_df], ignore_index=True)

            data = data.rename(columns={"ordertxid": "order_id"})
            data["time"] = data["time"].apply(int)

            return data
        else:
            return res

    # end of query user data
    # ==========================================================================

    # ==========================================================================
    # query user trading

    def query_add_order(self,
                        ordertype,
                        buy_or_sell,
                        volume,
                        pair,
                        price,
                        price2=None,
                        trigger="last",
                        userref=None,
                        leverage=None,
                        oflags=None,
                        timeinforce="GTC",
                        starttm=0,
                        expiretm=0,
                        close_ordertype=None,
                        close_price=None,
                        close_price2=None,
                        deadline=None,
                        validate=False,
                        ):

        if ordertype not in ["market", "limit", "stop-loss", "take-profit", "stop-loss-limit",
                             "take-profit-limit", "settle-position"]:
            raise Exception(f"Invalid parameter for ordertype: {ordertype}")

        if buy_or_sell not in ["buy", "sell"]:
            raise Exception(f"Invalid parameter buy_or_sell: {buy_or_sell}")

        if volume < 0:
            raise Exception("Invalid parameter volume, the volume must be positive")

        if ordertype in ["stop-loss-limit", "take-profit-limit"] and price2 is None:
            raise Exception("Invalid parameters, price2 must be specified for the given ordertype")

        if trigger not in ["last", "index"]:
            raise Exception(f"Invalid parameter trigger: {trigger}")

        if timeinforce not in ["GTC", "IOC", "GTD"]:
            raise Exception(f"Invalid parameter timeinforce: {timeinforce}")

        if close_ordertype is not None and close_ordertype not in ["limit", "stop-loss", "take-profit", "stop-loss-limit", "take-profit-limit"]:
            raise Exception(f"Invalid parameter close_ordertype: {close_ordertype}")

        if validate not in [False, True]:
            raise Exception(f"Invalid parameter validate: {validate}")

        # defaults to True in the case of a test session
        validate = True if self._test_session else validate

        data = {
            "ordertype": ordertype,
            "type": buy_or_sell,
            "pair": pair,
            "volume": volume,
            "price": price,
            # "trigger": trigger,  # this argument does not see to work
            # "timeinforce": timeinforce,  # this argument does not work
            "starttm": starttm,
            "expiretm": expiretm,
            "validate": str(validate).lower(),
        }

        if userref is not None:
            data["userref"] = userref
        if price2 is not None:
            data["price2"] = price2
        if leverage is not None:
            data["leverage"] = leverage
        if oflags is not None:
            data["oflags"] = oflags
        if close_ordertype is not None and close_price is not None:
            data["close[ordertype]"] = close_ordertype
            data["close[price]"] = close_price

            if close_price2 is not None:
                data["close[price2]"] = close_price2
        if deadline is not None:
            data["deadline"] = deadline

        res = self._private_query("AddOrder", data=data)
        self._update_counters("add_order", pair)

        if "result" in res:
            return res["result"]
        else:
            return res



    def query_cancel_order(self, txid):
        data = {"txid": txid}

        res = self._private_query("CancelOrder", data=data)
        self._update_counters("cancel_order")

        if "result" in res:
            return res["result"]
        else:
            return res

    def query_cancel_all(self):
        pass

    def query_cancel_all_orders_after(self, timeout):
        pass

    # end of query user trading
    # ==========================================================================

    # ==========================================================================
    # useful methods

    def test_connection(self):
        """
        test the connection to the server
        :return: True if the connection is alive and the server online,
                 False otherwise
        """
        res = self.query_system_status()
        return "result" in res and res["result"]["status"] == "online"

    def is_test_session(self):
        return self._test_session

    def user_counters(self):
        return {
            "api_counter": self._api_call_counter,
            "api_counter_decay": self._api_counter_decay,
            "max_api_counter": self._max_api_counter,
            "order_counter": self._order_counter,
            "order_counter_decay": self._ratecount_decay,
            "max_num_orders": self._max_num_orders,
            "max_ratecount": self._max_rate_count
        }


def is_none_or_type(o, t):
    return o is None or isinstance(o, t)


def output_or_join_list(obj):
    if isinstance(obj, list):
        return ",".join(obj)
    elif isinstance(obj, str):
        return obj
    else:
        raise Exception(f"Unknown objet type: {obj}, {type(obj)}")
