from secret_tokens import RATING_LIST
import json
import requests

def get_cf_ratings() -> list[(str, int)]:
    API = 'https://codeforces.com/api/user.info?handles='
    raw_data = requests.get(API + ';'.join(RATING_LIST))
    if raw_data.status_code != 200:
        return []
    vals = json.loads(raw_data.text)
    ret = []
    for user_info in vals['result']:
        ret.append((user_info['handle'], int(user_info['rating'])))
    ret.sort(key=lambda x: -x[1])
    print(ret)
    return ret
