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

def get_cf_ratings_raw_someone(handle: str) -> str:
    API = f'https://codeforces.com/api/user.info?handles={handle}'
    raw_data = requests.get(API)
    return raw_data.text

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

def get_cf_rating_change() -> str:
    lst = secret_tokens.RATING_LIST
    res = []
    for user in lst:
        url = f'https://codeforces.com/api/user.rating?handle={user}'
        raw_data = requests.get(url)
        if raw_data.status_code != 200:
            continue
        vals = json.loads(raw_data.text)
        last_record = vals['result'][-1] if vals['result'] and len(vals['result']) > 0 else None
        if last_record:
            res.append(last_record)
    res.sort(key=lambda x : -int(x['contestId']))
    last_contest, last_contest_name = res[0]['contestId'], res[0]['contestName']
    last_contest_res = []
    for r in res:
        if r['contestId'] == last_contest:
            last_contest_res.append((r['handle'], int(r['oldRating']), int(r['newRating'])))
    last_contest_res.sort(key=lambda x: (x[1] - x[2], -x[2], x[0]))
    ret = f'最近一次竞赛排名（{last_contest_name}）变化：\n'
    for row in last_contest_res:
        ret += f'{row[0]}: {row[1]} -> {row[2]} ({row[2] - row[1] if row[1] - row[2] > 0 else "+" + str(row[2] - row[1])})\n'
    return ret.strip()

if __name__ == '__main__':
    print(get_cf_rating_change())

