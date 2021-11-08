from django.shortcuts import render
from django.http import HttpResponse, response
import json
from urllib.request import urlopen
import requests

# Create your views here.
def home(request):
  return render(request, 'index.html')

def gold_mining(request):

  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
  
  # URL FOR JOB ADRESSES
  adress = "0xF38C9C59536730a4118f1e9c1FcbaEDf48bCcd07"
  warrior_job = "0x3a4D27B77B253bdb9AFec082D8f5cDE5A4D713E1,0x4713A70db9AD47780EFC3300c08C17c4013DCa57"
  part_time_job = "0xfA65a5751ef6079C1022Aa10b9163d7A2281360A"
  page = "1"
  page_size = "10"
  direction = "asc"
  job_url = "https://game.binaryx.pro/info/getWorks2?address=0xF38C9C59536730a4118f1e9c1FcbaEDf48bCcd07&work_type=0xfA65a5751ef6079C1022Aa10b9163d7A2281360A&page=1&page_size=100&direction=asc"
  job_result = requests.get(job_url, headers=headers).json()
  print(job_result)

  # URL FOR HERO MINING AND ATTRIBUTES
  tokenId = "80303894492192783130042507832564791829654306464206166768664418307148710157945"
  url = "https://game.binaryx.pro/info/getAttr?tokenId="+tokenId

  result = requests.get(url, headers=headers)
  # print(result.json())
  return render(request, 'gold_mining.html')