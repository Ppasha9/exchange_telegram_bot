# Simple ExchangeTelegramBot

# Credits
Author: https://github.com/Ppasha9

Bot Username: `@TestExchangeBot_bot`

## Description
Uses exchange rate data from this web service: https://exchangeratesapi.io. Returns the latest exchange rates list. USD is base currency and converts currency from the list.

## Commands
* `/list or /lst` - returns list of all available rates. Ex.  ● DKK: 6.74 ● HUF: 299.56

  Once the currency data is loaded from the service, it is saved in a local database too. Also, the timestamp of the last request is saved. Next time user requests anything the app bot checks whether 10 minutes elapsed since the last request:
  * If yes, new data is loaded from web service.
  * If no, previously saved data from the local database is loaded.

  In this simple bot json file is using for local database.

* `/exchange 10 USD to CAD` - converts currency to the second currency with two decimal precision and return. Ex.: $15.55
* `/history USD/CAD for 7 days` - return an image graph chart which shows the exchange rate graph/chart of the selected currency for the last 7 days.
