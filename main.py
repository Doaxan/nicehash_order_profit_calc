import requests
import json
import time
import operator

import sys

YOBIT_BTC_USD = "https://yobit.io/api/2/btc_usd/ticker"
NICE_PRICE_JSON = "https://api.nicehash.com/api?method=stats.global.24h"
ALL_COINS_JSON = "http://whattomine.com/calculators.json"
kH = 1000.
MH = 1000000.
GH = 1000000000.
TH = 1000000000000.
PH = 1000000000000000.

# parse yobit btc/usd price
r = requests.get(YOBIT_BTC_USD)
parsed_json = json.loads(r.content)
yobit_buy = parsed_json['ticker']['buy']
# print(yobit_buy)

# parse nicehash algo price
r = requests.get(NICE_PRICE_JSON)
parsed_json = json.loads(r.content)
result = parsed_json['result']
algo_price = {}
for x in result['stats']:
    algo_price[x['algo']] = float(x['price'])


def Scrypt(difficulty, block_reward, btc_price):
    BTC_TH_DAY = algo_price[0]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, TH) - BTC_TH_DAY
    return revenue_btc


def SHA256(difficulty, block_reward, btc_price):
    BTC_PH_DAY = algo_price[1]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, PH) - BTC_PH_DAY
    return revenue_btc


def X11(difficulty, block_reward, btc_price):
    BTC_TH_DAY = algo_price[3]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, TH) - BTC_TH_DAY
    return revenue_btc


def X13(difficulty, block_reward, btc_price):
    BTC_GH_DAY = algo_price[4]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, GH) - BTC_GH_DAY
    return revenue_btc


def NeoScrypt(difficulty, block_reward, btc_price):
    BTC_GH_DAY = algo_price[8]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, GH) - BTC_GH_DAY
    return revenue_btc


def Qubit(difficulty, block_reward, btc_price):
    BTC_TH_DAY = algo_price[11]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, TH) - BTC_TH_DAY
    return revenue_btc


def Quark(difficulty, block_reward, btc_price):
    BTC_TH_DAY = algo_price[12]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, TH) - BTC_TH_DAY
    return revenue_btc


def Lyra2REv2(difficulty, block_reward, btc_price):
    BTC_TH_DAY = algo_price[14]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, TH) - BTC_TH_DAY
    return revenue_btc


def Ethash_dagger(difficulty, block_reward, btc_price):
    BTC_GH_DAY = algo_price[20]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, GH) - BTC_GH_DAY
    return revenue_btc


def Decred_blake14r(difficulty, block_reward, btc_price):
    BTC_TH_DAY = algo_price[21]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, TH) - BTC_TH_DAY
    return revenue_btc


def CryptoNight(difficulty, block_reward, btc_price):
    BTC_MH_DAY = algo_price[22]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, MH) - BTC_MH_DAY
    return revenue_btc


def LBRY(difficulty, block_reward, btc_price):
    BTC_TH_DAY = algo_price[23]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, TH) - BTC_TH_DAY
    return revenue_btc


def Equihash(difficulty, block_reward, btc_price):
    BTC_MH_DAY = algo_price[24]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, MH) - BTC_MH_DAY
    return revenue_btc


def Pascal(difficulty, block_reward, btc_price):
    BTC_TH_DAY = algo_price[25]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, TH) - BTC_TH_DAY
    return revenue_btc


def Sia_blake2b(difficulty, block_reward, btc_price):
    BTC_TH_DAY = algo_price[27]
    revenue_btc = btc_reward(difficulty, block_reward, btc_price, TH) - BTC_TH_DAY
    return revenue_btc


def coin_reward(difficulty, block_reward, hashrate):
    block_day = (24 * 60 * 60) / (difficulty * pow(2, 32) / hashrate)
    coin_day = block_day * block_reward
    # print(str(coin_day) + " coins per day")
    return coin_day


def btc_reward(difficulty, block_reward, btc_price, hashrate):
    btc_day = coin_reward(difficulty, block_reward, hashrate) * btc_price
    # print(str(btc_day) + " BTC per day")
    return btc_day


r = requests.get(ALL_COINS_JSON)
parsed_json = json.loads(r.content)
coins = parsed_json['coins']

coin_profit = {}
coin_profit24 = {}

# parse {"365Coin":{"id":74 ...
x = 0
for name in coins:
    x = x + 1
    print('\r', "[", x, "/", len(coins), "]", end='')
    sys.stdout.flush()
    # parse {'id': 74, 'tag': '365', ...
    ids = coins[name]['id']
    coin_url = "http://whattomine.com/coins/" + str(ids) + ".json"
    # print(name + ": " + coin_url)
    while True:
        try:
            time.sleep(0.5)
            r = requests.get(coin_url)
            coin_json = json.loads(r.content)
        except json.decoder.JSONDecodeError:
            print("ban")
            time.sleep(2)
            continue
        break

    try:
        # TODO: Fix print's
        if coin_json['algorithm'] == 'Scrypt':
            # print(coin_json['name'] + "[Scrypt]:", Scrypt(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[Scrypt]:"] = [float(Scrypt(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[Scrypt]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[Scrypt]:"] = [float(Scrypt(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[Scrypt]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'SHA-256':
            if coin_json['name'] == 'Bitcoin': continue
            # print(coin_json['name'] + "[SHA256]:", SHA256(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[SHA-256]:"] = [float(SHA256(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[SHA-256]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[SHA-256]:"] = [float(SHA256(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[SHA-256]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'X11':
            # print(coin_json['name'] + "[X11]:", X11(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[X11]:"] = [float(X11(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[X11]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[X11]:"] = [float(X11(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[X11]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'X13':
            # print(coin_json['name'] + "[X13]:", X13(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[X13]:"] = [float(X13(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[X13]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[X13]:"] = [float(X13(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[X13]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'NeoScrypt':
            # print(coin_json['name'] + "[NeoScrypt]:", NeoScrypt(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[NeoScrypt]:"] = [float(NeoScrypt(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[NeoScrypt]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[NeoScrypt]:"] = [float(NeoScrypt(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[NeoScrypt]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'Qubit':
            # print(coin_json['name'] + "[Qubit]:", Qubit(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[Qubit]:"] = [float(Qubit(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[Qubit]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[Qubit]:"] = [float(Qubit(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[Qubit]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'Quark':
            # print(coin_json['name'] + "[Quark]:", Quark(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[Quark]:"] = [float(Quark(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[Quark]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[Quark]:"] = [float(Quark(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[Quark]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'Lyra2REv2':
            # print(coin_json['name'] + "[Lyra2REv2]:", Lyra2REv2(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[Lyra2REv2]:"] = [float(Lyra2REv2(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[Lyra2REv2]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[Lyra2REv2]:"] = [float(Lyra2REv2(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[Lyra2REv2]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'Ethash':
            # print(coin_json['name'] + "[Ethash_dagger]:", Ethash_dagger(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[Ethash_dagger]:"] = [float(Ethash_dagger(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[Ethash_dagger]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[Ethash_dagger]:"] = [float(Ethash_dagger(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[Ethash_dagger]:"].append(coin_json['lagging'])
            continue
        if coin_json['name'] == 'Decred':
            # print(coin_json['name'] + "[Decred]:", Decred_blake14r(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[Decred]:"] = [float(Decred_blake14r(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[Decred]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[Decred]:"] = [float(Decred_blake14r(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[Decred]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'CryptoNight':
            # print(coin_json['name'] + "[CryptoNight]:", CryptoNight(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[CryptoNight]:"] = [float(CryptoNight(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[CryptoNight]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[CryptoNight]:"] = [float(CryptoNight(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[CryptoNight]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'LBRY':
            # print(coin_json['name'] + "[LBRY]:", LBRY(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[LBRY]:"] = [float(LBRY(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[LBRY]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[LBRY]:"] = [float(LBRY(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[LBRY]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'Equihash':
            # print(coin_json['name'] + "[Equihash]:", Equihash(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[Equihash]:"] = [float(Equihash(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[Equihash]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[Equihash]:"] = [float(Equihash(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[Equihash]:"].append(coin_json['lagging'])
            continue
        if coin_json['algorithm'] == 'Pascal':
            # print(coin_json['name'] + "[Pascal]:", Pascal(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[Pascal]:"] = [float(Pascal(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[Pascal]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[Pascal]:"] = [float(Pascal(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[Pascal]:"].append(coin_json['lagging'])
            continue
        if coin_json['name'] == 'Sia':
            # print(coin_json['name'] + "[Sia]:", Sia_blake2b(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))
            coin_profit24[coin_json['name'] + "[Sia]:"] = [float(Sia_blake2b(coin_json['difficulty24'], coin_json['block_reward'], coin_json['exchange_rate24']))]
            coin_profit24[coin_json['name'] + "[Sia]:"].append(coin_json['lagging'])

            coin_profit[coin_json['name'] + "[Sia]:"] = [float(Sia_blake2b(coin_json['difficulty'], coin_json['block_reward'], coin_json['exchange_rate']))]
            coin_profit[coin_json['name'] + "[Sia]:"].append(coin_json['lagging'])
            continue
    except KeyError:
        continue

# print(sorted(coin_profit.values(), reverse=True))

print("24H:")
coin_profit24_sorted = sorted(coin_profit24.items(), key=operator.itemgetter(1), reverse=True)
# print(coin_profit_sorted)
for (key, value) in coin_profit24_sorted:
    if value[1]: continue
    if value[0] < 0: continue
    print(key, value[0], "BTC", "=", yobit_buy*value[0], "$USD")

print("CURRENT:")
coin_profit_sorted = sorted(coin_profit.items(), key=operator.itemgetter(1), reverse=True)
# print(coin_profit_sorted)
for (key, value) in coin_profit_sorted:
    if value[1]: continue
    if value[0] < 0: continue
    print(key, value[0], "BTC", "=", yobit_buy*value[0], "$USD")


# calc profit
while True:
    print("\r\n")
    coin_calc = input('Enter COIN: ')
    price = float(input('Enter PRICE: '))
    speed = float(input('Enter Max SPEED: '))
    val_speed = input('Enter TH/GH/MH...: ')
    if val_speed == 'kh':
        val_speed = kH
    elif val_speed == 'mh':
        val_speed = MH
    elif val_speed == 'gh':
        val_speed = GH
    elif val_speed == 'th':
        val_speed = TH
    elif val_speed == 'ph':
        val_speed = PH
    summ = float(input('Enter Sum: '))

    for name in coins:
        # parse {'id': 74, 'tag': '365', ...
        if name != coin_calc: continue
        id = coins[name]['id']
        coin_url = "http://whattomine.com/coins/" + str(id) + ".json"
        # print(name + ": " + coin_url)
        while True:
            try:
                time.sleep(0.5)
                r = requests.get(coin_url)
                coin_curr = json.loads(r.content)
            except json.decoder.JSONDecodeError:
                print("ban")
                time.sleep(2)
                continue
            break
        break
    calc = btc_reward(coin_curr['difficulty'], coin_curr['block_reward'], coin_curr['exchange_rate'], val_speed*speed) - summ
    calc3 = btc_reward(coin_curr['difficulty3'], coin_curr['block_reward3'], coin_curr['exchange_rate3'], val_speed*speed) - summ
    calc7 = btc_reward(coin_curr['difficulty7'], coin_curr['block_reward7'], coin_curr['exchange_rate7'], val_speed*speed) - summ
    calc24 = btc_reward(coin_curr['difficulty24'], coin_curr['block_reward24'], coin_curr['exchange_rate24'], val_speed*speed) - summ
    coin_rew = coin_reward(coin_curr['difficulty'], coin_curr['block_reward'], val_speed*speed)
    coin_rew3 = coin_reward(coin_curr['difficulty3'], coin_curr['block_reward3'], val_speed*speed)
    coin_rew7 = coin_reward(coin_curr['difficulty7'], coin_curr['block_reward7'], val_speed*speed)
    coin_rew24 = coin_reward(coin_curr['difficulty24'], coin_curr['block_reward24'], val_speed*speed)
    print("Current:", coin_curr['name'], "=", coin_rew, "coins =", calc, "BTC = ", yobit_buy*calc, "$USD")
    print("24H:", coin_curr['name'], "=", coin_rew24, "coins =", calc24, "BTC = ", yobit_buy*calc24, "$USD")
    print("3D:", coin_curr['name'], "=", coin_rew3, "coins =", calc3, "BTC = ", yobit_buy*calc3, "$USD")
    print("7D:", coin_curr['name'], "=", coin_rew7, "coins =", calc7, "BTC = ", yobit_buy*calc7, "$USD")
