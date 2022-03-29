from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time
import pandas as pd
import asyncio
import nest_asyncio
from keepAlive import keep_alive
nest_asyncio.apply()
import discord

DISCORD_TOKEN="OTU4MTc3NDUxNjI2ODY0NzQw.YkJiSg.2kYaX-WfC_0B_hAx47EUgLsgJv4"

finalDictionary={}
finalSorterdArray=[]
finalHourArray=[]
def fetchDetails():
    coinArray=[]
    priceArray=[]
    hourChangeArray=[]
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)  
    for page in range(1,10):
        url="https://coinalyze.net/?quotecoin=USDT&exchange=A&market_type=futures&page={}".format(page)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
        dfs = pd.read_html(str(tables))
        coinName=(dfs[0][0])
        price=(dfs[0][1])
        hourChange=(dfs[0][2])
        index=0
        for i in coinName:
            i=str(i)
            if i.endswith("USDT Perp Binance"):
                splitstring=i.split('/')
                coin=splitstring[0].strip()
                coinArray.append(coin)
                priceArray.append(float(price[index]))
                hourChangeArray.append(float(hourChange[index]))
            index=index+1
    dataDictionary={'Ticker':coinArray,'Price':priceArray,'1H':hourChangeArray}
    sortedChangeArray=[]
    for change in hourChangeArray:
        if change > 2:
            sortedChangeArray.append(change)
    sortedChangeArray=sorted(sortedChangeArray,reverse=True)
    # for change in sortedChangeArray:
    #     index=hourChangeArray.index(change)
    return dataDictionary,sortedChangeArray,hourChangeArray
        # print("{} {} {}".format(dataDictionary['Ticker'][index],dataDictionary['Price'][index],dataDictionary['1H'][index]))


DISCORD_TOKEN="OTU4MTc3NDUxNjI2ODY0NzQw.YkJiSg.2kYaX-WfC_0B_hAx47EUgLsgJv4"
bot=discord.Client()
async def sendDetails():
    while(True):  
      finalDictionary,finalSorterdArray,finalHourArray=fetchDetails()
      curr_time = time.localtime()
      curr_clock = time.strftime("%H:%M:%S", curr_time)
      finalString='----------------'+'\n'+curr_clock+'\n'
      for chan in finalSorterdArray:
        ind=finalHourArray.index(chan)
        currentString="{} {} {}\n".format(finalDictionary['Ticker'][ind],finalDictionary['Price'][ind],finalDictionary['1H'][ind])
        finalString=finalString + currentString
        print(currentString)
      channel=bot.get_channel(958244891798953984)
      finalString=finalString+'\n'+'----------------'
      await channel.send(finalString)
      await asyncio.sleep(300)
      
@bot.event
async def on_ready():
	await sendDetails()

bot.run(DISCORD_TOKEN)
