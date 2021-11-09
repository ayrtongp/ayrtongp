from django.shortcuts import render
from django.http import HttpResponse, response
import json
from urllib.request import urlopen
import requests, locale
from pycoingecko import CoinGeckoAPI

# Create your views here.
def home(request):
  return render(request, 'index.html')

def gold_mining(request):

  locale.setlocale( locale.LC_ALL, '')

  msg_total_job = []
  array_heroes = []
  data = {}
  total_gold_day = []

  cg = CoinGeckoAPI()
  gold_price = cg.get_coin_ticker_by_id('cyberdragon-gold')['tickers'][0]['last']
  data['btc_price'] = cg.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd']
  data['cbr_dragon_price'] = gold_price
  data['bnx_price'] = cg.get_coin_ticker_by_id('binaryx')['tickers'][0]['last']

  if request.GET.get('adressid') is not None:
    adress_personal = str(request.GET.get('adressid'))
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    work_adresses = {
    'part_time': "0xfA65a5751ef6079C1022Aa10b9163d7A2281360A",
    'warrior': "0x3a4D27B77B253bdb9AFec082D8f5cDE5A4D713E1,0x4713A70db9AD47780EFC3300c08C17c4013DCa57",
    'thief': "0x480d503B12ae928e8DcCd820CE45B2f6F39Ad598",
    'mage': "0x21D4Da5833d93944B8340788C6b463ED8420838B",
    'ranger': "0x81E9aCe9511A7d56fd31940d1C49425CA3a2B8f8"
    }

    level_multiplier = {
      1: 1,     2: 2,    3: 4,      4: 8,     5:16
    }

    page = "1"
    page_size = "10000"
    direction = "asc"
    main_url = "https://game.binaryx.pro/info/getWorks2?address="



    for key, value in work_adresses.items():

      job_url = main_url + adress_personal + "&work_type=" + value + "&page=" + page + "&page_size=" + page_size + "&direction=" + direction
      job_result = requests.get(job_url, headers=headers).json()  
      total_in_job = job_result['data']['result']['total']
      array_job = job_result['data']['result']['items']

      # print(total_in_job)

      if total_in_job > 0:

        for hero in array_job:
          tokenId = hero['token_id']
          url = "https://game.binaryx.pro/info/getAttr?tokenId="+tokenId
          result = requests.get(url, headers=headers)
          # print(result.json())
          dated = result.json()['data']['result'][0]
          # print(tokenId)

          array_stats = []

          array_stats.append(int(dated['strength']))
          array_stats.append(int(dated['agility']))
          array_stats.append(int(dated['physique']))
          array_stats.append(int(dated['volition']))
          array_stats.append(int(dated['brains']))
          array_stats.append(int(dated['charm']))
          array_stats.append(sum(array_stats))
          array_stats.append(int(dated['level']))
          array_stats.append(key)

          if key == 'mage':
            msg_total_job.append(str(total_in_job) + " herói(s) em Scrollscribe")
            formula = ((1 + ((int(dated['brains']) - 85)/2)) * 288) * level_multiplier[int(dated['level'])]
            array_stats.append(formula)
          if key == 'warrior':
            msg_total_job.append(str(total_in_job) + " herói(s) em Lumberjack")
            formula = ((1 + ((int(dated['strength']) - 85)/2)) * 288) * level_multiplier[int(dated['level'])]
            array_stats.append(formula)
          if key == 'thief':
            msg_total_job.append(str(total_in_job) + " herói(s) em Winemaker")
            formula = ((1 + ((int(dated['agility']) - 85)/2)) * 288) * level_multiplier[int(dated['level'])]
            array_stats.append(formula)
          if key == 'ranger':
            msg_total_job.append(str(total_in_job) + " herói(s) em Hunting")
            formula = ((1 + ((int(dated['strength']) - 85)/2)) * 288) * level_multiplier[int(dated['level'])]
            array_stats.append(formula)
          if key == 'part_time':
            msg_total_job.append(str(total_in_job) + " herói(s) em Part-Time")
            formula = 288 * level_multiplier[int(dated['level'])]
            array_stats.append(formula)
          
          total_gold_day.append(formula)
          array_heroes.append(array_stats)
  
  if len(array_heroes) > 0:
    data['db'] = array_heroes
    data['total_gold'] = sum(total_gold_day)
    data['gold_in_day_usd'] = locale.currency(sum(total_gold_day) * gold_price, grouping=True)
    data['gold_in_week_usd'] = locale.currency(sum(total_gold_day) * gold_price * 7, grouping=True)
    data['gold_in_month_usd'] = locale.currency(sum(total_gold_day) * gold_price * 30, grouping=True)
  else:
    data['db'] = [0,0,0,0,0,0,0,0,0,0]
    data['total_gold'] = 0
    data['gold_in_day_usd'] = 0
    data['gold_in_week_usd'] = 0
    data['gold_in_month_usd'] = 0

  return render(request, 'gold_mining.html', data)