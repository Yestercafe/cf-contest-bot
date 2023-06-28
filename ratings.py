from secret_tokens import RATING_LIST
import json
import requests
import secret_tokens

def get_cf_ratings() -> list[(str, int)]:
    API = 'https://codeforces.com/api/user.info?handles='
    raw_data = requests.get(API + ';'.join(RATING_LIST))
    if raw_data.status_code != 200:
        return []
    vals = json.loads(raw_data.text)
    ret = []
    for user_info in vals['result']:
        try:
            ret.append((user_info['handle'], int(user_info['rating'])))
        except KeyError:
            ret.append((user_info['handle'], -1))
    ret.sort(key=lambda x: (-x[1], x[0].lower()))
    print(ret)
    return ret

def get_cf_ratings_raw() -> str:
    API = 'https://codeforces.com/api/user.info?handles='
    raw_data = requests.get(API + ';'.join(RATING_LIST))
    return raw_data.text

def wrap_rat() -> str:
    kvs = get_cf_ratings()
    if len(secret_tokens.RATING_LIST) == 0:
        return 'rating list 为空'
    elif len(kvs) == 0:
        return '爬虫炸了'
    else:
        msg = 'Codeforces 竞赛分排名榜:\n'
        for name, rating in kvs:
            msg += f'{name} - '
            rating = int(rating)
            if rating < 0:
                msg += 'unrated'
            else:
                level = 'newbie - 灰名'
                if rating >= 1200:
                    level = 'pupil - 绿名'
                if rating >= 1400:
                    level = 'specialist - 青名'
                if rating >= 1600:
                    level = 'expert - 蓝名'
                if rating >= 1900:
                    level = 'candidate master - 紫名'
                if rating >= 2100:
                    level = 'master - 浅橙名'
                if rating >= 2300:
                    level = 'international master - 深橙名'
                if rating >= 2400:
                    level = 'grandmaster - 浅红名'
                if rating >= 2600:
                    level = 'international grandmaster - 深红名'
                if rating >= 3000:
                    level = 'legendary master - 黑红名'
                msg += f'{rating} - {level}'
            msg += '\n'
        return msg

if __name__ == '__main__':
    print(wrap_rat())

