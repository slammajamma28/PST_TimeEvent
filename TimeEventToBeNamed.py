import requests
import datetime
from datetime import timezone
from bs4 import BeautifulSoup
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from collections import Counter
import numpy

startTS = datetime.datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
print("Process started at " + startTS)

#PSN_IDS = [ "Adorabears", "AffectatiousDonk", "Alindawyl", "AlterArchuria", "AppleKratue", "Asher1985", "Barra333", "BinkUncia", "Blood_Velvet", "BUYDJMAXRESPECT", "cbchaos67", "clayser", "daco_1979", "Da-Eastside", "dagobahhh", "danc97-", "Dark_Adonis", "Darth_Krid", "Dino_Roar", "Dipsy_Doodle_", "diskdocx", "Dolken_swe", "ff_pennysticks", "fisty123", "guylian", "HaoleDave", "hBLOXs", "Hemming87", "ImStylinOnYaBro", "Izularia", "Jerry_Appleby", "JMeeks1875", "jvaferreira", "kinjall", "Laburnski", "lion1325478", "Martz4040", "mattigummi45", "Meikoro", "Mikel93", "NewYorkUgly", "Nox123", "NyarlathQtep", "olsen77", "pathtoninja", "PayneKillerTears", "Pokkit_", "RemingtonInk", "Road2unner", "russelguppy", "Savenger", "ShadowEpyon10", "Shady_Wombat", "slammajamma28", "staytrue1985", "stgermain", "stpatty", "sum1_worsethan_u", "SylarTheNinja", "THE--ALCHEMlST", "themindisacity", "TheRealClayman", "Tuffinz_", "Vapion", "Vo1cl", "Wdog-999", "XxDecieverxX", "Zetberg" ]
PSN_IDS = ["Road2unner", "slammajamma28", "Blood_Velvet", "staytrue1985", "XxDecieverxX", "Zetberg"]
#PSN_IDS = ["slammajamma28", "Blood_Velvet"]
EVENT_START = datetime.datetime.strptime('2023/03/01', "%Y/%m/%d")
EVENT_END = datetime.datetime.strptime('2023/04/01', "%Y/%m/%d")

ff_profile = "C:\\Users\\dillo\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\8lk0om2z.default"
options = Options()
options.add_argument("-profile")
options.add_argument(ff_profile)
driver = webdriver.Firefox(options=options)

filetime = datetime.datetime.now().strftime("%b-%d-%H%M")
file_out = open(f'C:\\Users\\dillo\\Documents\\Python\\PST_TimeEvent\\output\\{filetime}.html', "w", encoding='utf-8')
current_file = open(f'C:\\Users\\dillo\\Documents\\Python\\PST_TimeEvent\\tracker.html', "w", encoding='utf-8')
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
LEADERBOARD = []

class Trophy:
    def __init__(self, psn, logNum, tDate, tTime, tRarity) -> None:
        self.psn = psn
        self.logNum = logNum
        self.tDate = tDate
        self.tTime = tTime
        self.tRarity = tRarity
    
    def setPSN(self, psn):
        self.psn = psn
    
    def getPSN(self):
        return self.psn
    
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

    def setTRarity(self, tRarity):
        self.tRarity = tRarity
    
    def getTRarity(self):
        return self.tRarity

    def getPSTLogHtml(self):
        return f'<a href="https://www.playstationtrophies.org/profiles/{self.psn}/log?id={self.logNum}">{self.logNum}</a>'

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

    ## Get Hidden Trophy count
    url = f"https://psnprofiles.com/{psn}"
    try:
        driver.get(url)
        m = driver.find_element(By.ID, "hidden-trophies")
        #hover over element
        actions = ActionChains(driver)
        actions.move_to_element(m).perform()
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        hiddenTrophies = int(soup.find("div", id="tiptip_content").find("b").text)
    except Exception as err:
        hiddenTrophies = int(0)

    end_of_event = 0
    page = 1
    plat_count = 0
    while end_of_event < 1:
        ## Get Log
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
            log_num = hiddenTrophies + int(row_info[4].get_text().replace("#","").replace(",","").strip())
            trophy_rarity = row_info[8].find("span", "typo-top").get_text().replace('%', '')
            trophy_date=row_info[5].find("span", "typo-top-date").get_text()
            trophy_date=datetime.datetime.strptime(trophy_date.replace('st ', ' ').replace('nd ', ' ').replace('rd ', ' ').replace('th ', ' '), '%d %b %Y')
            trophy_time=datetime.datetime.strptime(row_info[5].find("span", "typo-bottom-date").get_text().strip(), '%I:%M:%S %p' ) # 2:00:59 AM
            if trophy_date >= EVENT_END:
                continue
            elif trophy_date >= EVENT_START:
                trophyList.append(Trophy(psn, log_num, trophy_date.date(), trophy_time, trophy_rarity))
            else:
                end_of_event = 1
        page = page + 1

trophyList.sort(key=lambda r: r.tTime)

for troph in trophyList:
    #print(troph.printTrophy())
    #print (troph.getPSN() + "," + troph.getTTime().strftime('%H:%M'))
    psid = troph.getPSN()
    cTime = troph.getTTime().strftime("%H:%M")
    if cTime in TIME_ARRAY:
        # Check the rest of the times for the rarest trophy
        TMP_LIST= []
        for x in trophyList:
            if x.getTTime().strftime('%H:%M') == cTime:
                TMP_LIST.append(x)
        TMP_LIST.sort(key=lambda r: r.tRarity)
        #print(f"{cTime},{psid}!")
        psid = TMP_LIST[0].getPSN()
        file_out.write(f"{cTime}|{psid}\n")
        CLAIMED_TIME.append([cTime, psid, TMP_LIST[0].getPSTLogHtml(), TMP_LIST[0].getTRarity()])
        LEADERBOARD.append(psid)
        TIME_ARRAY.remove(cTime)

cnt = Counter()
for lb in LEADERBOARD:
    cnt[lb] += 1

current_file.write("<!DOCTYPE html>\n<head>\n<link rel='stylesheet' href='styles/styles.css'>\n</head>\n"
                    + f"<body>\n<script src='js/script.js'></script>\n<h1>PST TIME EVENT</h1>\n<h3>as of {startTS} UTC</h3>\n"
                    + "<div>Times are tracked and claimed automatically.<br>"
                    + "Post in the <a href='https://www.playstationtrophies.org'>discussion thread</a> "
                    + "if you see any discrepancies and for further rules.</div><br>"
                    + "<div class=\"tab\"><button class=\"tablinks active\" onclick=\"openTab(event, 'remaining')\">Remaining</button>\n"
                    + "<button class=\"tablinks\" onclick=\"openTab(event, 'claimed')\">Claimed</button>\n"
                    + "<button class=\"tablinks\" onclick=\"openTab(event, 'leaderboard')\">LB</button></div>\n"
                    + "<div id=\"remaining\" class=\"tabcontent\" style=\"display:block\">"
                    + "<h2>REMAINING TIMES</h2>\n<table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
#current_file.write(tabulate(TIME_ARRAY, headers=["Time"], tablefmt='unsafehtml'))
for ttime in TIME_ARRAY:
    current_file.write(f"<tr><td>{ttime}</tr></td>\n")
current_file.write("</tbody>\n</table>\n</div>\n<div id=\"claimed\" class=\"tabcontent\">\n<h2>CLAIMED TIMES</h2>\n")
current_file.write(tabulate(CLAIMED_TIME, headers=["Time","User","Log#","Rarity"], tablefmt='unsafehtml'))
current_file.write("\n</div>\n<div id=\"leaderboard\" class=\"tabcontent\">\n<h2>LEADERBOARD</h2>\n")
current_file.write(tabulate(cnt.items(), headers=["User","Count"], tablefmt='unsafehtml'))
current_file.write("\n</div>\n</body>")

print("Process complete at " + datetime.datetime.now(timezone.utc).strftime("%H:%M:%S"))
driver.quit()