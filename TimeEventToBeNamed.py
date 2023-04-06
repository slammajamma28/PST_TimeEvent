import requests
import datetime
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from datetime import timedelta

#PSN_IDS = [ "Adorabears", "AffectatiousDonk", "Alindawyl", "AlterArchuria", "AppleKratue", "Asher1985", "Barra333", "BinkUncia", "Blood_Velvet", "BUYDJMAXRESPECT", "cbchaos67", "clayser", "daco_1979", "Da-Eastside", "dagobahhh", "danc97-", "Dark_Adonis", "Darth_Krid", "Dino_Roar", "Dipsy_Doodle_", "diskdocx", "Dolken_swe", "ff_pennysticks", "fisty123", "guylian", "HaoleDave", "hBLOXs", "Hemming87", "ImStylinOnYaBro", "Izularia", "Jerry_Appleby", "JMeeks1875", "jvaferreira", "kinjall", "Laburnski", "lion1325478", "Martz4040", "mattigummi45", "Meikoro", "Mikel93", "NewYorkUgly", "Nox123", "NyarlathQtep", "olsen77", "pathtoninja", "PayneKillerTears", "Pokkit_", "RemingtonInk", "Road2unner", "russelguppy", "Savenger", "ShadowEpyon10", "Shady_Wombat", "slammajamma28", "staytrue1985", "stgermain", "stpatty", "sum1_worsethan_u", "SylarTheNinja", "THE--ALCHEMlST", "themindisacity", "TheRealClayman", "Tuffinz_", "Vapion", "Vo1cl", "Wdog-999", "XxDecieverxX", "Zetberg" ]
#PSN_IDS = ["slammajamma28", "staytrue1985", "XxDecieverxX", "Zetberg" ]
PSN_IDS = ["Road2unner", "slammajamma28", "Blood_Velvet", "staytrue1985", "XxDecieverxX", "Zetberg"]
EVENT_START = datetime.datetime.strptime('2023/02/01', "%Y/%m/%d")
EVENT_END = datetime.datetime.strptime('2023/02/28', "%Y/%m/%d")

file_out = open(f'C:\\Users\\dillo\\Documents\\Python\\RATAS\\output\\users-{filetime}.csv', "w", encoding='utf-8')
file_out.write("sep=|\n")

TIME_ARRAY = []
for i in range(24):
    if i < 10:
        i = f"0{i}"
    for y in range(60):
        if y < 10:
            y = f"0{y}"
        #TIME_ARRAY.append(datetime.datetime.strptime(f"{i}:{y}", "%H:%M"))
        TIME_ARRAY.append(f"{i}:{y}")

CLAIMED_TIME = []

class Trophy:
    def __init__(self, pst, logNum, tDate, tTime) -> None:
        self.pst = pst
        self.logNum = logNum
        self.tDate = tDate
        self.tTime = tTime
    
    def setPST(self, pst):
        self.pst = pst
    
    def getPst(self):
        return self.pst
    
    def setLogNum(self, logNum):
        self.logNum = logNum
    
    def getLogNum(self):
        return self.logNum

    def setTDate(self, tDate):
        self.tDate = tDate
    
    def getTDate(self):
        return self.tDate

    def setTTime(self, tTime):
        self.tTime = tTime
    
    def getTTime(self):
        return self.tTime

    def printTrophy(self):
        tString = self.tTime.strftime('%I:%M:%S %p')
        retStr = f'{self.pst},{self.logNum},{self.tDate},{tString}'
        return retStr

class TimeItem():
    def __init__(self, tHour, tMinute, tTrophy) -> None:
        self.tHour = tHour
        self.tMinute = tMinute
        self.tTtrophy = tTrophy

trophyList = []

for psn in PSN_IDS:
    end_of_event = 0
    page = 1
    plat_count = 0
    while end_of_event < 1:
        url = f"https://psnprofiles.com/{psn}/log?page={page}"
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        #print(f'Now on {url}')
        html_content = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_content,"html.parser")
        body = soup.find('tbody')
        trophyLogRows = soup.find_all('tr')
        if len(trophyLogRows) == 0:
            end_of_event = 1
        for i in trophyLogRows:
            row_info=i.find_all('td')
            log_num=row_info[4].get_text().replace("#","").replace(",","").strip()
            trophy_date=row_info[5].find("span", "typo-top-date").get_text()
            trophy_date=datetime.datetime.strptime(trophy_date.replace('st ', ' ').replace('nd ', ' ').replace('rd ', ' ').replace('th ', ' '), '%d %b %Y')
            trophy_time=datetime.datetime.strptime(row_info[5].find("span", "typo-bottom-date").get_text().strip(), '%I:%M:%S %p' ) # 2:00:59 AM
            if trophy_date >= EVENT_END:
                continue
            elif trophy_date >= EVENT_START:
                trophyList.append(Trophy(psn, log_num, trophy_date.date(), trophy_time))
            else:
                end_of_event = 1
        page = page + 1

trophyList.sort(key=lambda r: r.tTime)

for troph in trophyList:
    #print(troph.printTrophy())
    #print (troph.getPst() + "," + troph.getTTime().strftime('%H:%M'))
    psid = troph.getPst()
    cTime = troph.getTTime().strftime("%H:%M")
    if cTime in TIME_ARRAY:
        print(f"{cTime},{psid}!")
        CLAIMED_TIME.append([troph, cTime])
        TIME_ARRAY.remove(cTime)