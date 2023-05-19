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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from collections import Counter
import traceback

startTS = datetime.datetime.now(timezone.utc).strftime("%Y/%m/%d %H:%M:%S %Z")
#startTS = datetime.datetime.now(timezone.utc).strftime("%Y/%m/%d %I:%M:%S %p %Z")
print("Process started at " + datetime.datetime.now().strftime("%H:%M:%S"))

participants = open("participants", "r")
  
# reading the file
data = participants.read()
  
# replacing end splitting the text 
# when newline ('\n') is seen.
PSN_IDS = data.split("\n")
participants.close()

EVENT_START = datetime.datetime.strptime('2023/05/01', "%Y/%m/%d")
EVENT_END = datetime.datetime.strptime('2023/06/01', "%Y/%m/%d")

ff_profile = "C:\\Users\\dillo\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\8lk0om2z.default"
options = Options()
options.add_argument("-profile")
options.add_argument(ff_profile)
driver = webdriver.Firefox(options=options)

filetime = datetime.datetime.now().strftime("%b-%d-%H%M")
file_out = open(f'C:\\Users\\dillo\\Documents\\Python\\PST_TimeEvent\\output\\{filetime}.html', "w", encoding='utf-8')
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
CLAIMED_TROPHIES = []
LEADERBOARD = []
USERS_TROPHIES = []
HOUR_BREAKDOWN = []
HOUR_0 = []
HOUR_1 = []
HOUR_2 = []
HOUR_3 = []
HOUR_4 = []
HOUR_5 = []
HOUR_6 = []
HOUR_7 = []
HOUR_8 = []
HOUR_9 = []
HOUR_10 = []
HOUR_11 = []
HOUR_12 = []
HOUR_13 = []
HOUR_14 = []
HOUR_15 = []
HOUR_16 = []
HOUR_17 = []
HOUR_18 = []
HOUR_19 = []
HOUR_20 = []
HOUR_21 = []
HOUR_22 = []
HOUR_23 = []

ALL_TROPHIES_STATS = []
HOUR_BUCKET_STATS = []
RAIRTY_RANGE_STATS = []
CLAIMED_TROPHIES_STATS = []
CLAIMED_RAIRTY_RANGE_STATS = []

class Trophy:
    def __init__(self, psn, logNum, tDate, tTime, tRarity, tType) -> None:
        self.psn = psn
        self.logNum = logNum
        self.tDate = tDate
        self.tTime = tTime
        self.tRarity = tRarity
        self.tType = tType
    
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

    def setTType(self, tType):
        self.tType = tType

    def getTTypeTxt(self):
        return self.tType

    def getTType(self):
        return f"<img src='images\{self.tType}.png' alt='{self.tType}' title='{self.tType}' />"

    def getPSTLogHtml(self):
        return f'<a href="https://www.playstationtrophies.org/profiles/{self.psn}/log?id={self.logNum}">{self.logNum}</a>'

    def printTrophy(self):
        tString = self.tTime.strftime('%I:%M:%S %p')
        retStr = f'{self.pst},{self.logNum},{self.tDate},{tString}'
        return retStr

class User:
    def __init__(self, psn) -> None:
        self.psn = psn
        self.trophies = []
        self.individualProgress = []
        self.individualTimes = []
        self.stats = []
        self.allTrophiesStats = []
        self.hourBucketStats = []
        self.rarityRangeStats = []
        self.claimedTrophiesStats = []
        self.completedTrophies = 0
        for i in range(60):
            if i < 10:
                i = f"0{i}"
                self.individualTimes.append(f"{i}")
            else:
                self.individualTimes.append(f"{i}")

    def setPSN(self, psn):
        self.psn = psn
    
    def getPSN(self):
        return self.psn
    
    def getTrophies(self):
        return self.trophies
    
    def getIndividualProgress(self):
        return self.individualProgress

    def addTrophy(self, trophy):
        self.trophies.append(trophy)
    
    def setCompletedTrophies(self, num):
        self.completedTrophies = num

    def getCompletedTrophies(self):
        return self.completedTrophies

    def calculateStats(self):
        t_sum = 0.0
        bronze_count = 0
        silver_count = 0
        gold_count = 0
        platinum_count = 0
        hundred_percents = 0
        zero_to_ten = 0
        ten_to_twenty = 0
        twenty_to_thirty = 0
        thirty_to_fourty = 0
        fourty_to_fifty = 0
        fifty_to_sixty = 0
        sixty_to_seventy = 0
        seventy_to_eighty = 0
        eighty_to_ninety = 0
        ninety_to_hundred = 0
        hour_0_total = 0
        hour_1_total = 0
        hour_2_total = 0
        hour_3_total = 0
        hour_4_total = 0
        hour_5_total = 0
        hour_6_total = 0
        hour_7_total = 0
        hour_8_total = 0
        hour_9_total = 0
        hour_10_total = 0
        hour_11_total = 0
        hour_12_total = 0
        hour_13_total = 0
        hour_14_total = 0
        hour_15_total = 0
        hour_16_total = 0
        hour_17_total = 0
        hour_18_total = 0
        hour_19_total = 0
        hour_20_total = 0
        hour_21_total = 0
        hour_22_total = 0
        hour_23_total = 0
        for t in user.getTrophies():
            trarity = float(t.getTRarity())
            t_sum += trarity
            if trarity == 100:
                hundred_percents += 1
            elif trarity >= 90:
                ninety_to_hundred += 1
            elif trarity >= 80:
                eighty_to_ninety += 1
            elif trarity >= 70:
                seventy_to_eighty += 1
            elif trarity >= 60:
                sixty_to_seventy += 1
            elif trarity >= 50:
                fifty_to_sixty += 1
            elif trarity >= 40:
                fourty_to_fifty += 1
            elif trarity >= 30:
                thirty_to_fourty += 1
            elif trarity >= 20:
                twenty_to_thirty += 1
            elif trarity >= 10:
                ten_to_twenty += 1
            elif trarity >= 0:
                zero_to_ten += 1
            else:
                continue

            if (t.getTTypeTxt() == "Bronze"):
                bronze_count += 1
            elif (t.getTTypeTxt() == "Silver"):
                silver_count += 1
            elif (t.getTTypeTxt() == "Gold"):
                gold_count += 1
            elif (t.getTTypeTxt() == "Platinum"):
                platinum_count += 1
            else:
                continue

            ttime = t.getTTime().strftime("%H:%M")
            if ttime.startswith("00:"):
                hour_0_total+= 1
            elif ttime.startswith("01:"):
                hour_1_total+= 1
            elif ttime.startswith("02:"):
                hour_2_total+= 1
            elif ttime.startswith("03:"):
                hour_3_total+= 1
            elif ttime.startswith("04:"):
                hour_4_total+= 1
            elif ttime.startswith("05:"):
                hour_5_total+= 1
            elif ttime.startswith("06:"):
                hour_6_total+= 1
            elif ttime.startswith("07:"):
                hour_7_total+= 1
            elif ttime.startswith("08:"):
                hour_8_total+= 1
            elif ttime.startswith("09:"):
                hour_9_total+= 1
            elif ttime.startswith("10:"):
                hour_10_total+= 1
            elif ttime.startswith("11:"):
                hour_11_total+= 1
            elif ttime.startswith("12:"):
                hour_12_total+= 1
            elif ttime.startswith("13:"):
                hour_13_total+= 1
            elif ttime.startswith("14:"):
                hour_14_total+= 1
            elif ttime.startswith("15:"):
                hour_15_total+= 1
            elif ttime.startswith("16:"):
                hour_16_total+= 1
            elif ttime.startswith("17:"):
                hour_17_total+= 1
            elif ttime.startswith("18:"):
                hour_18_total+= 1
            elif ttime.startswith("19:"):
                hour_19_total+= 1
            elif ttime.startswith("20:"):
                hour_20_total+= 1
            elif ttime.startswith("21:"):
                hour_21_total+= 1
            elif ttime.startswith("22:"):
                hour_22_total+= 1
            elif ttime.startswith("23:"):
                hour_23_total+= 1
            else:
                print("We should not have gotten here, oh dear...")

        # Total trophies
        self.allTrophiesStats.append(["Total trophies earned", len(user.getTrophies())])

        # Average rarity
        self.allTrophiesStats.append(["Average rarity of all trophies earned", round(t_sum / len(user.getTrophies()),2)])

        # Most rare trophy - percentage, who earned it, link to trophy
        user.getTrophies().sort(key=lambda r: float(r.tRarity))
        self.allTrophiesStats.append(["Rarest (PSNP rarity) trophy earned", user.getTrophies()[0].getPSN() + " #" + user.getTrophies()[0].getPSTLogHtml() + " - " + user.getTrophies()[0].getTRarity() + " " + user.getTrophies()[0].getTType()])

        # Count of 100% rarity trophies
        self.allTrophiesStats.append(["Number of 100% rarity trophies", hundred_percents])

        # Most earned time slot
        self.allTrophiesStats.append(["Most earned hour slot", max(hour_0_total,
                                                                hour_1_total,
                                                                hour_2_total,
                                                                hour_3_total,
                                                                hour_4_total,
                                                                hour_5_total,
                                                                hour_6_total,
                                                                hour_7_total,
                                                                hour_8_total,
                                                                hour_9_total,
                                                                hour_10_total,
                                                                hour_11_total,
                                                                hour_12_total,
                                                                hour_13_total,
                                                                hour_14_total,
                                                                hour_15_total,
                                                                hour_16_total,
                                                                hour_17_total,
                                                                hour_18_total,
                                                                hour_19_total,
                                                                hour_20_total,
                                                                hour_21_total,
                                                                hour_22_total,
                                                                hour_23_total) ])

        # Number of each type
        self.allTrophiesStats.append(["Number of bronze trophies", bronze_count])
        self.allTrophiesStats.append(["Number of silver trophies", silver_count])
        self.allTrophiesStats.append(["Number of gold trophies", gold_count])
        self.allTrophiesStats.append(["Number of platinum trophies", platinum_count])

        # Rarity range counts
        self.rarityRangeStats.append(["< 10%", zero_to_ten])
        self.rarityRangeStats.append(["10% - 19.9%", ten_to_twenty])
        self.rarityRangeStats.append(["20% - 29.9%", twenty_to_thirty])
        self.rarityRangeStats.append(["30% - 39.9%", thirty_to_fourty])
        self.rarityRangeStats.append(["40% - 49.9%", fourty_to_fifty])
        self.rarityRangeStats.append(["50% - 59.9%", fifty_to_sixty])
        self.rarityRangeStats.append(["60% - 69.9%", sixty_to_seventy])
        self.rarityRangeStats.append(["70% - 79.9%", seventy_to_eighty])
        self.rarityRangeStats.append(["80% - 89.9%", eighty_to_ninety])
        self.rarityRangeStats.append(["90% - 100%", ninety_to_hundred])

        # Hour buckets
        self.hourBucketStats.append(["Hour 0", hour_0_total])
        self.hourBucketStats.append(["Hour 1", hour_1_total])
        self.hourBucketStats.append(["Hour 2", hour_2_total])
        self.hourBucketStats.append(["Hour 3", hour_3_total])
        self.hourBucketStats.append(["Hour 4", hour_4_total])
        self.hourBucketStats.append(["Hour 5", hour_5_total])
        self.hourBucketStats.append(["Hour 6", hour_6_total])
        self.hourBucketStats.append(["Hour 7", hour_7_total])
        self.hourBucketStats.append(["Hour 8", hour_8_total])
        self.hourBucketStats.append(["Hour 9", hour_9_total])
        self.hourBucketStats.append(["Hour 10", hour_10_total])
        self.hourBucketStats.append(["Hour 11", hour_11_total])
        self.hourBucketStats.append(["Hour 12", hour_12_total])
        self.hourBucketStats.append(["Hour 13", hour_13_total])
        self.hourBucketStats.append(["Hour 14", hour_14_total])
        self.hourBucketStats.append(["Hour 15", hour_15_total])
        self.hourBucketStats.append(["Hour 16", hour_16_total])
        self.hourBucketStats.append(["Hour 17", hour_17_total])
        self.hourBucketStats.append(["Hour 18", hour_18_total])
        self.hourBucketStats.append(["Hour 19", hour_19_total])
        self.hourBucketStats.append(["Hour 20", hour_20_total])
        self.hourBucketStats.append(["Hour 21", hour_21_total])
        self.hourBucketStats.append(["Hour 22", hour_22_total])
        self.hourBucketStats.append(["Hour 23", hour_23_total])

    def getAllTrophiesStats(self):
        return self.allTrophiesStats
    
    def getHourBucketStats(self):
        return self.hourBucketStats
    
    def getRarityRangeStats(self):
        return self.rarityRangeStats
    
    def getClaimedTrophiesStats(self):
        return self.claimedTrophiesStats

    def calculateIndividualGoal(self):
        self.trophies.sort(key=lambda r: float(r.tRarity))
        for troph in self.trophies:
            cTime = troph.getTTime().strftime("%S")
            if cTime in self.individualTimes:
                self.individualProgress.append([troph.getPSTLogHtml(), troph.getTRarity() + " " + troph.getTType(), cTime])
                self.individualTimes.remove(cTime)
        self.completedTrophies = len(self.individualProgress)
        if len(self.individualProgress) < 60:
            for ip in range(60):
                if ip < 10:
                    ip = f"0{ip}"
                else:
                    ip = f"{ip}"
                if ip in self.individualTimes:
                    self.individualProgress.append(["MISSING","MISSING",str(ip)])
        def sortByThirdIndex(a):
            return a[2]
        self.individualProgress.sort(key=sortByThirdIndex)

class TimeItem():
    def __init__(self, tHour, tMinute, tTrophy) -> None:
        self.tHour = tHour
        self.tMinute = tMinute
        self.tTtrophy = tTrophy

ALL_TROPHIES = []

try:
    for psn in PSN_IDS:
        user = User(psn)
        ## Get Hidden Trophy count
        url = f"https://psnprofiles.com/{psn}"
        try:
            driver.get(url)
            hmm = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "recent-trophies")))
            m = driver.find_element(By.ID, "hidden-trophies")
            #hover over element
            actions = ActionChains(driver)
            actions.move_to_element(m).perform()
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            hiddenTrophies = int(soup.find("div", id="tiptip_content").find("b").text)
        except NoSuchElementException as nsee:
            hiddenTrophies = int(0)
        except Exception as err:
            traceback.print_exc()
            raise ProcessLookupError(f"Had an issue looking up {psn}")

        end_of_event = 0
        page = 1
        plat_count = 0
        while end_of_event < 1:
            ## Get Log
            url = f"https://psnprofiles.com/{psn}/log?page={page}"
            #print("Now on " + url)
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
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
                trophy_type=row_info[9].find("img")['title']
                if trophy_date >= EVENT_END:
                    continue
                elif trophy_date >= EVENT_START:
                    trophy = Trophy(psn, log_num, trophy_date.date(), trophy_time, trophy_rarity, trophy_type)
                    ALL_TROPHIES.append(trophy)
                    user.addTrophy(trophy)
                else:
                    end_of_event = 1
            page = page + 1
        USERS_TROPHIES.append(user)

    ALL_TROPHIES.sort(key=lambda r: r.tTime)

    for troph in ALL_TROPHIES:
        #print(troph.printTrophy())
        #print (troph.getPSN() + "," + troph.getTTime().strftime('%H:%M'))
        psid = troph.getPSN()
        cTime = troph.getTTime().strftime("%H:%M")
        if cTime in TIME_ARRAY:
            # Check the rest of the times for the rarest trophy
            TMP_LIST= []
            for x in ALL_TROPHIES:
                if x.getTTime().strftime('%H:%M') == cTime:
                    TMP_LIST.append(x)
            TMP_LIST.sort(key=lambda r: float(r.tRarity))
            #print(f"{cTime},{psid}!")
            psid = TMP_LIST[0].getPSN()
            file_out.write(f"{cTime}|{psid}\n")
            CLAIMED_TIME.append([cTime, psid, TMP_LIST[0].getPSTLogHtml(), TMP_LIST[0].getTRarity() + " " + TMP_LIST[0].getTType()])
            CLAIMED_TROPHIES.append(troph)
            LEADERBOARD.append(psid)
            TIME_ARRAY.remove(cTime)

    # Split apart time array
    for i in TIME_ARRAY:
        if i.startswith("00:"):
            HOUR_0.append(i)
        elif i.startswith("01:"):
            HOUR_1.append(i)
        elif i.startswith("02:"):
            HOUR_2.append(i)
        elif i.startswith("03:"):
            HOUR_3.append(i)
        elif i.startswith("04:"):
            HOUR_4.append(i)
        elif i.startswith("05:"):
            HOUR_5.append(i)
        elif i.startswith("06:"):
            HOUR_6.append(i)
        elif i.startswith("07:"):
            HOUR_7.append(i)
        elif i.startswith("08:"):
            HOUR_8.append(i)
        elif i.startswith("09:"):
            HOUR_9.append(i)
        elif i.startswith("10:"):
            HOUR_10.append(i)
        elif i.startswith("11:"):
            HOUR_11.append(i)
        elif i.startswith("12:"):
            HOUR_12.append(i)
        elif i.startswith("13:"):
            HOUR_13.append(i)
        elif i.startswith("14:"):
            HOUR_14.append(i)
        elif i.startswith("15:"):
            HOUR_15.append(i)
        elif i.startswith("16:"):
            HOUR_16.append(i)
        elif i.startswith("17:"):
            HOUR_17.append(i)
        elif i.startswith("18:"):
            HOUR_18.append(i)
        elif i.startswith("19:"):
            HOUR_19.append(i)
        elif i.startswith("20:"):
            HOUR_20.append(i)
        elif i.startswith("21:"):
            HOUR_21.append(i)
        elif i.startswith("22:"):
            HOUR_22.append(i)
        elif i.startswith("23:"):
            HOUR_23.append(i)
        else:
            print("We should not have gotten here, oh dear...")

    cnt = Counter()
    for lb in LEADERBOARD:
        cnt[lb] += 1

    tcnt = Counter()
    for et in ALL_TROPHIES:
        cTime = et.getTTime().strftime("%H:%M")
        tcnt[cTime] += 1

    USERS_TROPHIES.sort(key=lambda r: r.psn.lower())
    for user in USERS_TROPHIES:
        #print(f"{user.getPSN()} has earned {len(user.getTrophies())} trophies")
        user.calculateStats()
        user.calculateIndividualGoal()

    ######################################################
    #
    #   Do some stats stuff
    #
    ######################################################

    ###########################
    # OVERALL, use ALL_TROPHIES
    ###########################
    
    # Total trophies earned
    ALL_TROPHIES_STATS.append(["Total trophies earned", len(ALL_TROPHIES)])
    
    t_sum = 0.0
    bronze_count = 0
    silver_count = 0
    gold_count = 0
    platinum_count = 0
    hundred_percents = 0
    zero_to_ten = 0
    ten_to_twenty = 0
    twenty_to_thirty = 0
    thirty_to_fourty = 0
    fourty_to_fifty = 0
    fifty_to_sixty = 0
    sixty_to_seventy = 0
    seventy_to_eighty = 0
    eighty_to_ninety = 0
    ninety_to_hundred = 0
    hour_0_total = 0
    hour_1_total = 0
    hour_2_total = 0
    hour_3_total = 0
    hour_4_total = 0
    hour_5_total = 0
    hour_6_total = 0
    hour_7_total = 0
    hour_8_total = 0
    hour_9_total = 0
    hour_10_total = 0
    hour_11_total = 0
    hour_12_total = 0
    hour_13_total = 0
    hour_14_total = 0
    hour_15_total = 0
    hour_16_total = 0
    hour_17_total = 0
    hour_18_total = 0
    hour_19_total = 0
    hour_20_total = 0
    hour_21_total = 0
    hour_22_total = 0
    hour_23_total = 0

    # Loop through ALL_TROPHIES to find stats
    for t in ALL_TROPHIES:
        trarity = float(t.getTRarity())
        t_sum += trarity
        if trarity == 100:
            hundred_percents += 1
        elif trarity >= 90:
            ninety_to_hundred += 1
        elif trarity >= 80:
            eighty_to_ninety += 1
        elif trarity >= 70:
            seventy_to_eighty += 1
        elif trarity >= 60:
            sixty_to_seventy += 1
        elif trarity >= 50:
            fifty_to_sixty += 1
        elif trarity >= 40:
            fourty_to_fifty += 1
        elif trarity >= 30:
            thirty_to_fourty += 1
        elif trarity >= 20:
            twenty_to_thirty += 1
        elif trarity >= 10:
            ten_to_twenty += 1
        elif trarity >= 0:
            zero_to_ten += 1
        else:
            continue

        ttype = t.getTTypeTxt()
        if (ttype == "Bronze"):
            bronze_count += 1
        elif (ttype == "Silver"):
            silver_count += 1
        elif (ttype == "Gold"):
            gold_count += 1
        elif (ttype == "Platinum"):
            platinum_count += 1
        else:
            continue

        ttime = t.getTTime().strftime("%H:%M")
        if ttime.startswith("00:"):
            hour_0_total+= 1
        elif ttime.startswith("01:"):
            hour_1_total+= 1
        elif ttime.startswith("02:"):
            hour_2_total+= 1
        elif ttime.startswith("03:"):
            hour_3_total+= 1
        elif ttime.startswith("04:"):
            hour_4_total+= 1
        elif ttime.startswith("05:"):
            hour_5_total+= 1
        elif ttime.startswith("06:"):
            hour_6_total+= 1
        elif ttime.startswith("07:"):
            hour_7_total+= 1
        elif ttime.startswith("08:"):
            hour_8_total+= 1
        elif ttime.startswith("09:"):
            hour_9_total+= 1
        elif ttime.startswith("10:"):
            hour_10_total+= 1
        elif ttime.startswith("11:"):
            hour_11_total+= 1
        elif ttime.startswith("12:"):
            hour_12_total+= 1
        elif ttime.startswith("13:"):
            hour_13_total+= 1
        elif ttime.startswith("14:"):
            hour_14_total+= 1
        elif ttime.startswith("15:"):
            hour_15_total+= 1
        elif ttime.startswith("16:"):
            hour_16_total+= 1
        elif ttime.startswith("17:"):
            hour_17_total+= 1
        elif ttime.startswith("18:"):
            hour_18_total+= 1
        elif ttime.startswith("19:"):
            hour_19_total+= 1
        elif ttime.startswith("20:"):
            hour_20_total+= 1
        elif ttime.startswith("21:"):
            hour_21_total+= 1
        elif ttime.startswith("22:"):
            hour_22_total+= 1
        elif ttime.startswith("23:"):
            hour_23_total+= 1
        else:
            print("We should not have gotten here, oh dear...")

    # Average rarity
    ALL_TROPHIES_STATS.append(["Average rarity of all trophies earned", round(t_sum / len(ALL_TROPHIES),2)])

    # Most rare trophy - percentage, who earned it, link to trophy
    ALL_TROPHIES.sort(key=lambda r: float(r.tRarity))
    ALL_TROPHIES_STATS.append(["Rarest (PSNP rarity) trophy earned", ALL_TROPHIES[0].getPSN() + " #" + ALL_TROPHIES[0].getPSTLogHtml() + " - " + ALL_TROPHIES[0].getTRarity() + " " + ALL_TROPHIES[0].getTType()])

    # Count of 100% rarity trophies
    ALL_TROPHIES_STATS.append(["Number of 100% rarity trophies", hundred_percents])

    # Most earned time slot
    ALL_TROPHIES_STATS.append(["Most earned hour slot", max(hour_0_total,
                                                               hour_1_total,
                                                               hour_2_total,
                                                               hour_3_total,
                                                               hour_4_total,
                                                               hour_5_total,
                                                               hour_6_total,
                                                               hour_7_total,
                                                               hour_8_total,
                                                               hour_9_total,
                                                               hour_10_total,
                                                               hour_11_total,
                                                               hour_12_total,
                                                               hour_13_total,
                                                               hour_14_total,
                                                               hour_15_total,
                                                               hour_16_total,
                                                               hour_17_total,
                                                               hour_18_total,
                                                               hour_19_total,
                                                               hour_20_total,
                                                               hour_21_total,
                                                               hour_22_total,
                                                               hour_23_total) ])

    mcom1 = str(tcnt.most_common(1)[0][0])
    mcom2 = str(tcnt.most_common(1)[0][1])

    # Most contested time slot
    ALL_TROPHIES_STATS.append(["Most contested time slot", mcom1 + " [" + mcom2 + "]"])

    # Number of each type
    ALL_TROPHIES_STATS.append(["Number of bronze trophies", bronze_count])
    ALL_TROPHIES_STATS.append(["Number of silver trophies", silver_count])
    ALL_TROPHIES_STATS.append(["Number of gold trophies", gold_count])
    ALL_TROPHIES_STATS.append(["Number of platinum trophies", platinum_count])

    # Rarity range counts
    RAIRTY_RANGE_STATS.append(["< 10%", zero_to_ten])
    RAIRTY_RANGE_STATS.append(["10% - 19.9%", ten_to_twenty])
    RAIRTY_RANGE_STATS.append(["20% - 29.9%", twenty_to_thirty])
    RAIRTY_RANGE_STATS.append(["30% - 39.9%", thirty_to_fourty])
    RAIRTY_RANGE_STATS.append(["40% - 49.9%", fourty_to_fifty])
    RAIRTY_RANGE_STATS.append(["50% - 59.9%", fifty_to_sixty])
    RAIRTY_RANGE_STATS.append(["60% - 69.9%", sixty_to_seventy])
    RAIRTY_RANGE_STATS.append(["70% - 79.9%", seventy_to_eighty])
    RAIRTY_RANGE_STATS.append(["80% - 89.9%", eighty_to_ninety])
    RAIRTY_RANGE_STATS.append(["90% - 100%", ninety_to_hundred])

    # Hour buckets
    HOUR_BUCKET_STATS.append(["Hour 0", hour_0_total])
    HOUR_BUCKET_STATS.append(["Hour 1", hour_1_total])
    HOUR_BUCKET_STATS.append(["Hour 2", hour_2_total])
    HOUR_BUCKET_STATS.append(["Hour 3", hour_3_total])
    HOUR_BUCKET_STATS.append(["Hour 4", hour_4_total])
    HOUR_BUCKET_STATS.append(["Hour 5", hour_5_total])
    HOUR_BUCKET_STATS.append(["Hour 6", hour_6_total])
    HOUR_BUCKET_STATS.append(["Hour 7", hour_7_total])
    HOUR_BUCKET_STATS.append(["Hour 8", hour_8_total])
    HOUR_BUCKET_STATS.append(["Hour 9", hour_9_total])
    HOUR_BUCKET_STATS.append(["Hour 10", hour_10_total])
    HOUR_BUCKET_STATS.append(["Hour 11", hour_11_total])
    HOUR_BUCKET_STATS.append(["Hour 12", hour_12_total])
    HOUR_BUCKET_STATS.append(["Hour 13", hour_13_total])
    HOUR_BUCKET_STATS.append(["Hour 14", hour_14_total])
    HOUR_BUCKET_STATS.append(["Hour 15", hour_15_total])
    HOUR_BUCKET_STATS.append(["Hour 16", hour_16_total])
    HOUR_BUCKET_STATS.append(["Hour 17", hour_17_total])
    HOUR_BUCKET_STATS.append(["Hour 18", hour_18_total])
    HOUR_BUCKET_STATS.append(["Hour 19", hour_19_total])
    HOUR_BUCKET_STATS.append(["Hour 20", hour_20_total])
    HOUR_BUCKET_STATS.append(["Hour 21", hour_21_total])
    HOUR_BUCKET_STATS.append(["Hour 22", hour_22_total])
    HOUR_BUCKET_STATS.append(["Hour 23", hour_23_total])

    ###########################
    # CLAIMED, use CLAIMED_TROPHIES
    ###########################

    c_sum = 0.0
    c_bronze_count = 0
    c_silver_count = 0
    c_gold_count = 0
    c_platinum_count = 0
    c_hundred_percents = 0
    c_zero_to_ten = 0
    c_ten_to_twenty = 0
    c_twenty_to_thirty = 0
    c_thirty_to_fourty = 0
    c_fourty_to_fifty = 0
    c_fifty_to_sixty = 0
    c_sixty_to_seventy = 0
    c_seventy_to_eighty = 0
    c_eighty_to_ninety = 0
    c_ninety_to_hundred = 0
    
    for c in CLAIMED_TROPHIES:
        crarity = float(c.getTRarity())
        c_sum += crarity

        if crarity == 100:
            c_hundred_percents += 1
        elif crarity >= 90:
            c_ninety_to_hundred += 1
        elif crarity >= 80:
            c_eighty_to_ninety += 1
        elif crarity >= 70:
            c_seventy_to_eighty += 1
        elif crarity >= 60:
            c_sixty_to_seventy += 1
        elif crarity >= 50:
            c_fifty_to_sixty += 1
        elif crarity >= 40:
            c_fourty_to_fifty += 1
        elif crarity >= 30:
            c_thirty_to_fourty += 1
        elif crarity >= 20:
            c_twenty_to_thirty += 1
        elif crarity >= 10:
            c_ten_to_twenty += 1
        elif crarity >= 0:
            c_zero_to_ten += 1
        else:
            continue

        ctype = c.getTTypeTxt()
        if (ctype == "Bronze"):
            c_bronze_count += 1
        elif (ctype == "Silver"):
            c_silver_count += 1
        elif (ctype == "Gold"):
            c_gold_count += 1
        elif (ctype == "Platinum"):
            c_platinum_count += 1
        else:
            continue

    CLAIMED_TROPHIES_STATS.append(["Total trophies claimed", len(CLAIMED_TROPHIES)])

    # Average rarity
    CLAIMED_TROPHIES_STATS.append(["Average rarity of all time slots claimed", round(t_sum / len(CLAIMED_TROPHIES),2)])

    # Most rare trophy - percentage, who earned it, link to trophy
    CLAIMED_TROPHIES.sort(key=lambda r: float(r.tRarity))
    CLAIMED_TROPHIES_STATS.append(["Rarest (PSNP rarity) time slots claimed", CLAIMED_TROPHIES[0].getPSN() + " #" + CLAIMED_TROPHIES[0].getPSTLogHtml() + " - " + CLAIMED_TROPHIES[0].getTRarity() + " " + CLAIMED_TROPHIES[0].getTType()])

    # Count of 100% rarity trophies
    CLAIMED_TROPHIES_STATS.append(["Number of 100% rarity time slots", c_hundred_percents])

    # Number of each type
    CLAIMED_TROPHIES_STATS.append(["Number of bronze trophies", c_bronze_count])
    CLAIMED_TROPHIES_STATS.append(["Number of silver trophies", c_silver_count])
    CLAIMED_TROPHIES_STATS.append(["Number of gold trophies", c_gold_count])
    CLAIMED_TROPHIES_STATS.append(["Number of platinum trophies", c_platinum_count])

    # Rarity range counts
    CLAIMED_RAIRTY_RANGE_STATS.append(["< 10%", zero_to_ten])
    CLAIMED_RAIRTY_RANGE_STATS.append(["10% - 19.9%", c_ten_to_twenty])
    CLAIMED_RAIRTY_RANGE_STATS.append(["20% - 29.9%", c_twenty_to_thirty])
    CLAIMED_RAIRTY_RANGE_STATS.append(["30% - 39.9%", c_thirty_to_fourty])
    CLAIMED_RAIRTY_RANGE_STATS.append(["40% - 49.9%", c_fourty_to_fifty])
    CLAIMED_RAIRTY_RANGE_STATS.append(["50% - 59.9%", c_fifty_to_sixty])
    CLAIMED_RAIRTY_RANGE_STATS.append(["60% - 69.9%", c_sixty_to_seventy])
    CLAIMED_RAIRTY_RANGE_STATS.append(["70% - 79.9%", c_seventy_to_eighty])
    CLAIMED_RAIRTY_RANGE_STATS.append(["80% - 89.9%", c_eighty_to_ninety])
    CLAIMED_RAIRTY_RANGE_STATS.append(["90% - 100%", c_ninety_to_hundred])

    ######################################################
    #
    #   Start writing our HTML
    #
    ######################################################

    current_file = open(f'C:\\Users\\dillo\\Documents\\Python\\PST_TimeEvent\\tracker.html', "w", encoding='utf-8')
    current_file.write("<!DOCTYPE html>\n<head>\n<link rel='stylesheet' href='styles/styles.css'>\n</head>\n"
                        + "<body>\n<script src='js/jquery.js'></script>\n<script src='js/script.js'></script>\n<img src=\"images\\banner.png\" alt=\"PST's Wait a Minute Event\" title=\"PST's Wait a Minute Event\">\n"
                        + f"<h3 value=\"utc\" onClick=\"swapTime(event)\">as of {startTS}</h3>\n"
                        + f"<h4>as of {startTS}</h3>\n"
                        + "<div>Times are tracked and claimed automatically.<br>"
                        + "Post in the <a href='https://www.playstationtrophies.org/forum/topic/334336-wait-a-minute-~-discussion/'>discussion thread</a> "
                        + "if you see any discrepancies and for further rules.</div><br>\n")

    ###########################
    # Progress bar and tabs
    ###########################

    current_file.write("<div id=\"goal-count\"><table><thead><tr class='percentageFill'><th>Current</th><th>Remaining</th><th>Progress</th></tr></thead>\n"
                        + f"<tbody><tr class='percentageFill'><td>{len(CLAIMED_TIME)}</td><td>{1440-len(CLAIMED_TIME)}</td><td id=\"goalPercentage\">{round(len(CLAIMED_TIME)/1440 * 100,2)}%</td></tr></tbody></table></div><br>\n"
                        + "<div class=\"tab\"><button class=\"tablinks active\" onclick=\"openTab(event, 'remaining')\">Remaining</button>\n"
                        + "<button class=\"tablinks\" onclick=\"openTab(event, 'claimed')\">Claimed</button>\n"
                        + "<button class=\"tablinks\" onclick=\"openTab(event, 'leaderboard')\">LB</button>\n"
                        + "<button class=\"tablinks\" onclick=\"openTab(event, 'individual')\">Individual</button>\n"
                        + "<button class=\"tablinks\" onclick=\"openTab(event, 'stats')\">Stats</button></div>\n")

    ###########################
    # Overall remaining table cells
    ###########################                        
                        
    current_file.write("<div id=\"remaining\" class=\"tabcontent\" style=\"display:block\">\n"
                        + "<h2>REMAINING TIMES</h2>\n")
    
    current_file.write("<div id=\"hourly_total_summary\"><table><tbody>\n")
    current_file.write(f"<tr><td id='cell_0' class='sum_cell {'complete' if len(HOUR_0) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_0')\">Hour 00: {len(HOUR_0)}</td>\n")
    current_file.write(f"<td id='cell_1' class='sum_cell {'complete' if len(HOUR_1) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_1')\">Hour 01: {len(HOUR_1)}</td>\n")
    current_file.write(f"<td id='cell_2' class='sum_cell {'complete' if len(HOUR_2) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_2')\">Hour 02: {len(HOUR_2)}</td>\n")
    current_file.write(f"<td id='cell_3' class='sum_cell {'complete' if len(HOUR_3) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_3')\">Hour 03: {len(HOUR_3)}</td>\n")
    current_file.write(f"<td id='cell_4' class='sum_cell {'complete' if len(HOUR_4) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_4')\">Hour 04: {len(HOUR_4)}</td>\n")
    current_file.write(f"<td id='cell_5' class='sum_cell {'complete' if len(HOUR_5) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_5')\">Hour 05: {len(HOUR_5)}</td></tr>\n")
    current_file.write(f"<tr><td id='cell_6' class='sum_cell {'complete' if len(HOUR_6) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_6')\">Hour 06: {len(HOUR_6)}</td>\n")
    current_file.write(f"<td id='cell_7' class='sum_cell {'complete' if len(HOUR_7) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_7')\">Hour 07: {len(HOUR_7)}</td>\n")
    current_file.write(f"<td id='cell_8' class='sum_cell {'complete' if len(HOUR_8) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_8')\">Hour 08: {len(HOUR_8)}</td>\n")
    current_file.write(f"<td id='cell_9' class='sum_cell {'complete' if len(HOUR_9) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_9')\">Hour 09: {len(HOUR_9)}</td>\n")
    current_file.write(f"<td id='cell_10' class='sum_cell {'complete' if len(HOUR_10) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_10')\">Hour 10: {len(HOUR_10)}</td>\n")
    current_file.write(f"<td id='cell_11' class='sum_cell {'complete' if len(HOUR_11) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_11')\">Hour 11: {len(HOUR_11)}</td></tr>\n")
    current_file.write(f"<tr><td id='cell_12' class='sum_cell {'complete' if len(HOUR_12) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_12')\">Hour 12: {len(HOUR_12)}</td>\n")
    current_file.write(f"<td id='cell_13' class='sum_cell {'complete' if len(HOUR_13) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_13')\">Hour 13: {len(HOUR_13)}</td>\n")
    current_file.write(f"<td id='cell_14' class='sum_cell {'complete' if len(HOUR_14) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_14')\">Hour 14: {len(HOUR_14)}</td>\n")
    current_file.write(f"<td id='cell_15' class='sum_cell {'complete' if len(HOUR_15) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_15')\">Hour 15: {len(HOUR_15)}</td>\n")
    current_file.write(f"<td id='cell_16' class='sum_cell {'complete' if len(HOUR_16) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_16')\">Hour 16: {len(HOUR_16)}</td>\n")
    current_file.write(f"<td id='cell_17' class='sum_cell {'complete' if len(HOUR_17) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_17')\">Hour 17: {len(HOUR_17)}</td></tr>\n")
    current_file.write(f"<tr><td id='cell_18' class='sum_cell {'complete' if len(HOUR_18) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_18')\">Hour 18: {len(HOUR_18)}</td>\n")
    current_file.write(f"<td id='cell_19' class='sum_cell {'complete' if len(HOUR_19) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_19')\">Hour 19: {len(HOUR_19)}</td>\n")
    current_file.write(f"<td id='cell_20' class='sum_cell {'complete' if len(HOUR_20) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_20')\">Hour 20: {len(HOUR_20)}</td>\n")
    current_file.write(f"<td id='cell_21'  class='sum_cell {'complete' if len(HOUR_21) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_21')\">Hour 21: {len(HOUR_21)}</td>\n")
    current_file.write(f"<td id='cell_22' class='sum_cell {'complete' if len(HOUR_22) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_22')\">Hour 22: {len(HOUR_22)}</td>\n")
    current_file.write(f"<td id='cell_23' class='sum_cell {'complete' if len(HOUR_23) == 0 else ''}' onClick=\"showHourSummary(event, 'hour_23')\">Hour 23: {len(HOUR_23)}</td>\n")
    current_file.write("</tbody></table></div>\n<br>")

    ###########################
    # Remaining hourly tables
    ###########################

    current_file.write("<div id=\"hour_0\" class=\"hour_summary\">\n<table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_0:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")
    current_file.write("<div id=\"hour_1\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_1:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_2\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_2:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_3\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_3:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_4\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_4:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_5\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_5:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_6\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_6:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_7\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_7:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_8\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_8:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_9\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_9:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_10\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_10:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_11\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_11:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_12\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_12:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_13\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_13:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_14\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_14:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_15\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_15:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_16\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_16:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_17\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_17:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_18\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_18:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_19\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_19:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_20\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_20:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_21\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_21:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_22\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_22:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n")

    current_file.write("<div id=\"hour_23\" class=\"hour_summary\"><table>\n<thead>\n<tr><th>Time</th></tr>\n</thead>\n<tbody>\n")
    for ttime in HOUR_23:
        current_file.write(f"<tr><td>{ttime}</tr></td>\n")
    current_file.write("</tbody>\n</table>\n</div>\n</div>\n")

    ###########################
    # Claimed times leaderboard
    ###########################

    current_file.write("<div id=\"claimed\" class=\"tabcontent\">\n<h2>CLAIMED TIMES</h2>\n")
    current_file.write(tabulate(CLAIMED_TIME, headers=["Time","User","Log#","Rarity"], tablefmt='unsafehtml'))
    current_file.write("\n</div>\n<div id=\"leaderboard\" class=\"tabcontent\">\n<h2>LEADERBOARD</h2>\n")
    current_file.write(tabulate(cnt.most_common(), headers=["User","Count"], tablefmt='unsafehtml'))
    current_file.write("\n</div>\n")

    ###########################
    # Individual goal progress
    ###########################

    current_file.write("<div id=\"individual\" class=\"tabcontent\">\n<div class=\"dropdown\">")
    current_file.write("<button id='dropbtn_individual' class=\"dropbtn\">Select a PSN ID</button>\n<div class=\"dropdown-content\">\n")
    for user in USERS_TROPHIES:
        current_file.write(f"<button class='individualPercentage' value='{round(user.getCompletedTrophies() / 60 * 100,2)}' onclick=\"showUser(event, '{user.getPSN()}', '{user.getCompletedTrophies()}', '{round(user.getCompletedTrophies() / 60 * 100,2)}')\">{user.getPSN()} - {user.getCompletedTrophies() if user.getCompletedTrophies() < 60 else '✅'}</button><br>\n")
    current_file.write("</div></div><h2>INDIVIDUAL GOALS</h2>\n")
    for user in USERS_TROPHIES:
        current_file.write(f"<div id=\"{user.getPSN()}\" class=\"user_table\" style=\"display:none\">\n")
        current_file.write(tabulate(user.getIndividualProgress(), headers=["Log#","Rarity","Seconds"], tablefmt='unsafehtml'))
        current_file.write("</div>\n")
    current_file.write("</div>\n")

    ###########################
    # Stats tab
    ###########################
 
    current_file.write("<div id='stats' class='tabcontent'>\n"
                       + "<div class='dropdown'><button id='dropbtn_stat' class='dropbtn'>Overall</button>\n"
                       + "<div class='dropdown-content'>\n"
                       + "<button onclick=\"showStat(event, 'Overall')\">Overall</button><br>\n"
                       + "<button onclick=\"showStat(event, 'Claimed')\">Claimed</button><br>\n")
    
    ###########################
    # Dropdown menu
    ###########################

    for psn in PSN_IDS:
        current_file.write(f"<button onclick=\"showStat(event, '{psn}')\">{psn}</button><br>\n")
    
    current_file.write("</div></div>\n")
    
    ###########################
    # General stats
    ###########################

    current_file.write("<div id='Overall_stats' class='stats_table'>\n")
    current_file.write("<h2>GENERAL STATS</h2>\n")
    current_file.write(tabulate(ALL_TROPHIES_STATS, headers=["Info","Stat"], tablefmt='unsafehtml')+"\n")
    current_file.write("<br><h2>MOST CONTESTED TIME SLOTS</h2>\n")
    current_file.write(tabulate(tcnt.most_common(25), headers=["Slot","Count"], tablefmt='unsafehtml'))
    current_file.write("<br><h2>TIME SLOT STATS</h2>\n")
    current_file.write(tabulate(HOUR_BUCKET_STATS, headers=["Hour Bucket","Count"], tablefmt='unsafehtml')+"\n")
    current_file.write("<br><h2>RARITY STATS</h2>\n")
    current_file.write(tabulate(RAIRTY_RANGE_STATS, headers=["Rarity","Count"], tablefmt='unsafehtml')+"\n</div>")

    ###########################
    # Claimed stats
    ###########################
    
    current_file.write("<div id='Claimed_stats' class='stats_table'>\n")
    current_file.write("<h2>GENERAL STATS</h2>\n")
    current_file.write(tabulate(CLAIMED_TROPHIES_STATS, headers=["Info","Stat"], tablefmt='unsafehtml')+"\n")
    current_file.write("<br><h2>RARITY STATS</h2>\n")
    current_file.write(tabulate(CLAIMED_RAIRTY_RANGE_STATS, headers=["Rarity","Count"], tablefmt='unsafehtml')+"\n</div>")

    ###########################
    # Individual stats
    ###########################

    for user in USERS_TROPHIES:
        current_file.write(f"\n<div id='{user.getPSN()}_stats' class='stats_table' style=\"display:none\">")
        current_file.write("<h2>GENERAL STATS</h2>\n")
        current_file.write(tabulate(user.getAllTrophiesStats(), headers=["Info","Stat"], tablefmt='unsafehtml')+"\n")
        current_file.write("<br><h2>TIME SLOT STATS</h2>\n")
        current_file.write(tabulate(user.getHourBucketStats(), headers=["Hour Bucket","Count"], tablefmt='unsafehtml')+"\n")
        current_file.write("<br><h2>RARITY STATS</h2>\n")
        current_file.write(tabulate(user.getRarityRangeStats(), headers=["Rarity","Count"], tablefmt='unsafehtml')+"\n</div>")

    current_file.write("\n</div>\n</body>")
    print("Process complete at " + datetime.datetime.now().strftime("%H:%M:%S"))
    driver.quit()
except Exception as inst:
    print("Process failed at " + datetime.datetime.now().strftime("%H:%M:%S"))
    print(inst)
    traceback.print_exc()
    driver.quit()