import json
import os
from pathlib import Path
import sys
from time import sleep

from monitor import get_balance, place_bet, start_monitor, ARR
# from monitor import Balancesheet
# start monitor
start_monitor(0)

from wakepy import set_keepawake

ratio = 0.2

COOKIES = "is_rtl=1; tzo=1; fast_coupon=true; flaglng=en; typeBetNames=full; auid=LYd6cmOpzhMW38cABd8VAg==; che_g=a1cfbfa5-1608-2cc6-360d-e28b91b93cf5; pushfree_status=canceled; sh.session=d0fce1cc-99bb-436e-af7b-87194d9e5bc4; right_side=right; SESSION=f21a382cfb5045cb558412a048e8aa52; dnb=1; visit=2-cda5018324496d826d823f36024fd9e9; v3fr=1; lng=en; ggru=153; completed_user_settings=true; proofOfAge=1; uhash=60e3eb7a4fc12c5ba40ae6f4dcf5bca0; cur=XAF; _glhf=1672610858; coefview=0; ua=152159655; disallow_sport=; game_cols_count=2"

def get_file(filenm) -> str:
    """A simple function that returns the filepath independent of the platform"""

    if not sys.platform == "win32":
        path = Path(os.path.realpath(os.path.dirname(__file__)))
        return path.absolute().__str__() + "/" + filenm
    else:
        path = Path(os.path.realpath(os.path.dirname(__file__)))
        return path.absolute().__str__() + "\\" + filenm

def checkmatchR12(p1,p2,sep):
    
    found = False
    key = str(p1) + str(sep) + str(p2)
    with open(file=get_file("mkx_R12finish.json")) as f:
        data = json.loads(f.read())
    
    for d in data:
        if key in d:
            return True
    return found
        
        
def main() -> None:
    count = 0
    
    while True:
        print(count)
        # print(Balancesheet.current_amount)
        for match in ARR:
            if not match.hasbet and match.hasbeenupdated and (match.round == None or match.round == 1):
                if checkmatchR12(match.player_1, match.player_2, " - "):
                    print(" a bet is possible between", match.player_1," - ", match.player_2)
                    balance = get_balance(cookies=COOKIES)
                    balace = int(ratio * balance)
                    place_bet(cookies=COOKIES, referal_link=match.ref_link, summ=str(90), rodd=str(match.rodd_1), gameid=match.id, param=match.round, type=2140)# player 1 will win
                    match.hasbet = True
                    count = count + 1
                else:
                    print(" a bet is possible between the reverse", match.player_1," - ", match.player_2)
                    balance = get_balance(cookies=COOKIES)
                    balace = int(ratio * balance)
                    place_bet(cookies=COOKIES, referal_link=match.ref_link, summ=str(90), rodd=str(match.rodd_2), gameid=match.id, param=match.round, type=2141)# player 2 will win
                    match.hasbet = True
                    count = count + 1                  
        sleep(1)

if __name__ == "__main__":
    set_keepawake(keep_screen_awake=False)
    # do stuff that takes long time
    main()
    
    # unset_keepawake()