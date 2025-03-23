import ccxt
exchange = ccxt.binance()  # Binance borsasına bağlanıyoruz
ticker = exchange.fetch_ticker('ETH/BTC')  # BTC/USDT paritesinin verisini alıyoruz
print(ticker)
#bu bir deneme blogu satırıdır
