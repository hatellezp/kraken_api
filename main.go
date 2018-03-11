package main

import (
	"fmt"
	"log"

	"github.com/beldur/kraken-go-api-client"
)

func main() {
	fmt.Println("----------------------------------------------------------")
	fmt.Println("api := krakenapi.New(\"Hello\", \"There\")")
	api := krakenapi.New("Hello", "There")

	fmt.Println("---------------------------------------------------------")
	fmt.Println("krakenapi.Time() -> krakenapi.TimeResponse")
	result_Time, err_Time := api.Time()
	if err_Time != nil {
		log.Fatal(err_Time)
	}
	fmt.Printf("(string)       : krakenapi.TimeReponse.Rfc1123 : %s\n", result_Time.Rfc1123)
	fmt.Printf("(int)          : krakenapi.TimeReponse.Unix : %d\n", result_Time.Unixtime)

	fmt.Println("----------------------------------------------------------")
	fmt.Println("krakenapi.Assets() -> krakenapi.AssetsResponse")
	result_Assets, err_Assets := api.Assets()
	if err_Assets != nil {
		log.Fatal(err_Assets)
	}
	fmt.Printf("(string)       : krakenapi.AssetsResponse.BCH.Altname : %s\n", result_Assets.BCH.Altname)
	fmt.Printf("(string)       : krakenapi.AssetsResponse.BCH.AssetClass : %s\n", result_Assets.BCH.AssetClass)
	fmt.Printf("(int)          : krakenapi.AssetsResponse.BCH.Decimals : %d\n", result_Assets.BCH.Decimals)
	fmt.Printf("(int)          : krakenapi.AssetsResponse.BCH.DisplayDecimals : %d\n", result_Assets.BCH.DisplayDecimals)

	fmt.Println("----------------------------------------------------------")
	fmt.Println("krakenapi.AssetPairs() -> krakenapi.AssetPairsResponse")
	result_AssetPairs, err_AssetPairs := api.AssetPairs()
	if err_AssetPairs != nil {
		log.Fatal(err_AssetPairs)
	}
	fmt.Printf("(string)       : krakenapi.AssetPairsResponse.BCHEUR.Altname : %s\n", result_AssetPairs.BCHEUR.Altname)
	fmt.Printf("(string)       : krakenapi.AssetPairsResponse.BCHEUR.AssetClassBase : %s\n", result_AssetPairs.BCHEUR.AssetClassBase)
	fmt.Printf("(string)       : krakenapi.AssetPairsResponse.BCHEUR.Base : %s\n", result_AssetPairs.BCHEUR.Base)
	fmt.Printf("(string)       : krakenapi.AssetPairsResponse.BCHEUR.AssetClassQuote : %s\n", result_AssetPairs.BCHEUR.AssetClassQuote)
	fmt.Printf("(string)       : krakenapi.AssetPairsResponse.BCHEUR.Quote : %s\n", result_AssetPairs.BCHEUR.Quote)
	fmt.Printf("(string)       : krakenapi.AssetPairsResponse.BCHEUR.Lot : %s\n", result_AssetPairs.BCHEUR.Lot)
	fmt.Printf("(int)          : krakenapi.AssetClassQuote.BCHEUR.PairDecimals : %d\n", result_AssetPairs.BCHEUR.PairDecimals)
	fmt.Printf("(int)          : krakenapi.AssetPairsResponse.BCHEUR.LotDecimals : %d\n", result_AssetPairs.BCHEUR.LotDecimals)
	fmt.Printf("(int)          : krakenapi.AssetPairsResponse.BCHEUR.LotMultiplier : %d\n", result_AssetPairs.BCHEUR.LotMultiplier)
	fmt.Print("([]float32)    : krakenapi.AssetPairsResponse.BCHEUR.LeverageBuy : ")
	fmt.Println(result_AssetPairs.BCHEUR.LeverageBuy)
	fmt.Print("([]float32)    : krakenapi.AssetPairsResponse.BCHEUR.LeverageSell : ")
	fmt.Println(result_AssetPairs.BCHEUR.LeverageSell)
	fmt.Print("([][]float64)  : krakenapi.AssetPairsResponse.BCHEUR.Fees : ")
	fmt.Println(result_AssetPairs.BCHEUR.Fees)
	fmt.Print("([][]float64)  : krakenapi.AssetPairsResponse.BCHEUR.FeesMaker : ")
	fmt.Println(result_AssetPairs.BCHEUR.FeesMaker)
	fmt.Printf("(string)       : krakenapi.AssetPairsResponse.BCHEUR.FeeVolumeCurrency : %s\n", result_AssetPairs.BCHEUR.FeeVolumeCurrency)
	fmt.Printf("(int)          : krakenapi.AssetPairsResponse.BCHEUR.MarginCall : %d\n", result_AssetPairs.BCHEUR.MarginCall)
	fmt.Printf("(int)          : krakenapi.AssetPairsResponse.BCHEUR.MarginStop : %d\n", result_AssetPairs.BCHEUR.MarginStop)

	fmt.Println("----------------------------------------------------------")
	fmt.Println("krakenapi.Ticker(krakenapi.XXBTZEUR, krakenapi.XXRPZEUR) -> krakenapi.TickerResponse")
	result_Ticker, err_Ticker := api.Ticker(krakenapi.XXBTZEUR, krakenapi.XXRPZEUR)
	if err_Ticker != nil {
		log.Fatal(err_Ticker)
	}
	fmt.Print("([]string)      : krakenapi.TickerResponse.XXBTZEUR.Ask : ")
	fmt.Println(result_Ticker.XXBTZEUR.Ask)
	fmt.Print("([]string)      : krakenapi.TickerResponse.XXBTZEUR.Bid : ")
	fmt.Println(result_Ticker.XXBTZEUR.Bid)
	fmt.Print("([]string)      : krakenapi.TickerResponse.XXBTZEUR.Close : ")
	fmt.Println(result_Ticker.XXBTZEUR.Close)
	fmt.Print("([]string)      : krakenapi.TickerResponse.XXBTZEUR.Volume : ")
	fmt.Println(result_Ticker.XXBTZEUR.Volume)
	fmt.Print("([]string)      : krakenapi.TickerResponse.XXBTZEUR.VolumeAveragePrice : ")
	fmt.Println(result_Ticker.XXBTZEUR.VolumeAveragePrice)
	fmt.Print("([]int)         : krakenapi.TickerResponse.XXBTZEUR.Trades : ")
	fmt.Println(result_Ticker.XXBTZEUR.Trades)
	fmt.Print("([]string)      : krakenapi.TickerResponse.XXBTZEUR.Low : ")
	fmt.Println(result_Ticker.XXBTZEUR.Low)
	fmt.Print("([]string)      : krakenapi.TickerResponse.XXBTZEUR.High : ")
	fmt.Println(result_Ticker.XXBTZEUR.High)
	fmt.Print("(float32)       : krakenapi.TickerResponse.XXBTZEUR.OpeningPrice : ")
	fmt.Println(result_Ticker.XXBTZEUR.OpeningPrice)
}
