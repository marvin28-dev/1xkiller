
from random import choice
import sys
import threading
import requests as r
import json

from time import sleep,time

from wakepy import  unset_keepawake



clock = 10 # in sec
waitingtimes = [1, 2, 3, 4, 5, 4, 3, 2, 1]

ARR = list()
numberoftrials = 10



def threaded(fn):
    def wrapper(id):
        threading.Thread(target=fn, args=(id,)).start()
    return wrapper

# class BalanceSheet():
#     def __init__(self) -> None:
#         self.url = "https://cm1xbet.com/user/balance"
#         self.current_amount = 0
#         self.active = True
#         self.unplaced_bets = 0
#         self.cumm_unplaced_bets = 0
#         self.hist_unplaced_bets = dict()
#         self.currency = "XAF"
        
    
#     @threaded
#     def run(self):
        
#         while True:
#             res = self.get_balance()["balance"][0]
#             self.current_amount = res["money"]
#             # self.active = True
#             self.summ_unplaced_bets = res['summ_unplaced_bets']
#             # self.cumm_unplaced_bets = 0
#             # self.hist_unplaced_bets = dict()
#             # self.currency = "XAF"
#             sleep(1)
            
#     def get_balance(self):
#         count = 0
#         while True:
#             try: return r.post(url=self.url,cookies=COOKIES).json()
#             except:
#                 if(numberoftrials == count):
#                     print("Check your internet connection")
#                     sys.exit(-1)
#                 else:
#                     count += 1       

        
# Balancesheet = object()
# Balancesheet = BalanceSheet()
# Balancesheet.run()           


def get_rodd(i:dict, player):
    player -= 1
    for j in range(20):
        try: return i['GE'][j]['E'][player][0]['C']
        except:pass
            

class Match:
    def __init__(self, i:dict):
        
        # all var concerning identification
        self.id = i['I']
        self.game_cat = i["L"]
        self.player_1 = i['O1']
        self.player_2 = i['O2']
        self.hasupdated = False
        

        
        # all var concerning round/time
        try: self.strround = i['SC']['CPS']
        except: self.strround = None
        try: self.round = i['SC']['CP']
        except: self.round = None
        try: self.score_per_round = i['SC']['FS']
        except: self.score_per_round = None
        try: self.time = i['SC']['TS']
        except: self.time = None
        try:tmp = i['SC']['I']
        except: tmp = None

        if tmp == "Pre-game betting":
            self.prebetting = tmp
            self.prebetting = None
        
        # all var concerning markets
        self.hasbet = False
        
        
        # all var convering urls
        self.game_url = f"https://cm1xbet.com/LiveFeed/GetGameZip?id={self.id}&lng=en&cfview=0&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&partner=55&marketType=1&isNewBuilder=true"
        
        # timeout var
        self.timeout = int(time()) + int(10 * 60)

    @threaded
    def run(self):
        """_summary_"""
        sleep(choice(waitingtimes))

        while True:
            
            print(self.id, " has been updated")
            # update and create vars 
            res = get(self.game_url)
            res = res['Value']
            
            try:self.strround = res['SC']['CPS']
            except:self.strround = None
            
            try: self.time = res['SC']['TS']
            except: self.time = None
            try: self.score_per_round = res['SC']['FS']
            except: self.score_per_round = None
            self.rodd_1 = get_rodd(res,1)
            self.rodd_2 = get_rodd(res,2)
            
            try:hasattr(self, self.link)
            except:
                try: self.ref_link = "https://cm1xbet.com/en/live/Mortal-Kombat/"  + str(res['LI']) + "-" +str(res['LE']).replace(" ", "-") + "/" + str(res['I']) + "-" + str(res["O1E"]).replace("'","").replace(" ","-") + "-" + str(res["O2E"]).replace("'","").replace(" ","-") + "/"
                except Exception as e: print(e)
            
            
            # terminates the thread when necessary
            if self.strround == 'Game finished' or not self.game_cat == 'Mortal Kombat X':
                break
            else:
                try:
                    if self.ref_link:
                        self.hasbeenupdated = True
                except: pass
                sleep(3)

def get(url):
    count = 0

    while True:
        try: return r.get(url=url,).json()
        except:
            if(numberoftrials == count):
                print("Check your internet connection")
                exit_prog(-1)
            else:
                count += 1

def get_balance(cookies)->float :
    
    url = "https://cm1xbet.com/user/balance"
    count = 0
    while True:
        try: return r.post(url=url, headers={"X-Requested-With": "XMLHttpRequest","Cookie": cookies,}).json()['balance'][0]['money']
        except Exception as e:
            if(numberoftrials == count):
                print("Check your internet connection")
                exit_prog(-1)
            else:
                print(e)
                count += 1       

def iisnotfoundinARR(i):
    notfound = True
    if ARR:
        for j in ARR:
            if j.id == i['I']:
                return False
        return notfound
    else:
        return notfound

def cleanARR():
    
    while len(ARR) > 10:

        ARR.__delitem__(0)

def get_matches() -> None:
    

    
    while True:
        
        # MK11
        res = get("https://cm1xbet.com/LiveFeed/Get1x2_VZip?sports=103&champs=1252965&count=50&lng=en&mode=4&country=168&partner=55&getEmpty=true&noFilterBlockEvent=true")
        res = res['Value']
        
        for i in res:
            if iisnotfoundinARR(i):
                x = Match(i)
                x.run()
                ARR.append(x)

        sleep(clock)
        cleanARR()


def place_bet(cookies,referal_link,summ,rodd, gameid,param, type) -> bool: # userid
    
    if param == None:
        param = 1
    else:
        param = param + 1

    url = "https://cm1xbet.com/datalinelive/putbetscommon"
    count = 0
    while True:
        try: 
            response = r.post(
                url,
                headers={
                    "Host": "cm1xbet.mobi",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Language": "en-US;q=0.7,en;q=0.3",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Length": "512",
                    "Origin": "https://cm1xbet.com",
                    "Connection": "keep-alive",
                    "Referer": str(referal_link),
                    "Cookie": cookies,
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "TE": "trailers",
                    }, 
                    data={
                    "UserId":   "152159655", # 325416377
                    "Events[0][GameId]":    str(gameid),
                    "Events[0][Type]":  str(type), # 4059 2140 for player 1 per round and 2141 for player 2 per round, 1 for player 1 overall and 3 for player 2 overall
                    "Events[0][Coef]":	str(rodd),
                    "Events[0][Param]":	str(param),        # Here is the round number
                    "Events[0][PlayerId]":	"0",
                    "Events[0][Kind]":	"1",
                    "Events[0][Expired]":	"0",
                    "Events[0][Price]":	"0",
                    "Events[0][InstrumentId]":	"0",
                    "Events[0][Seconds]":	"0",
                    "partner":	"55",
                    "CfView":	"0",
                    "Summ":	str(summ),       # amount to bet
                    "Lng":	"en",
                    "Vid":	"0",
                    "hash":	"60e3eb7a4fc12c5ba40ae6f4dcf5bca0", #"3f6dc07e2f6f8b4439d22bc36d210d39" 
                    "CheckCf":	"1", #nsjoel changed this from 2 to 0 foyet changed from 0 to 1
                    "Live":	"true",
                    "notWait":	"true",
                    "TimeZone": str(1)
                })

            print("Content:" ,response.json())
            if response.json()['Error'].startswith('A bet has already been placed on this event'): return True

        except:
            if count == 5:
                print("Has tried to bet without success; aborting the operation...")
                exit_prog(-1)
            else:
                print("Trying again to bet")
                sleep(1)
                count +=1


def exit_prog(err_code) -> None:
    
    # try:unset_keepawake()
    # except: print("Couldn't safe exit")
    sys.exit(err_code)
    

@threaded
def start_monitor(id) -> None:
    """Nothing to say"""
    
    if id == 0:get_matches()


