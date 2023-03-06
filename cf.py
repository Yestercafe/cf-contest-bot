import requests
from bs4 import BeautifulSoup
import eventlet
import datetime
import pytz

class CFContest:
    def __init__(self, name: str, start_time: str, length: str):
        self.TIME_FORMAT = r'%b/%d/%Y %H:%M %z'
        self.name = name
        self.start_time = datetime.datetime.strptime(start_time + ' +0300', self.TIME_FORMAT).astimezone(pytz.timezone('Asia/Shanghai'))
        self.length = length
    def __repr__(self):
        return f'{self.name} {self.start_time} {self.length}'
    def __str__(self):
        return f'{self.name} {self.start_time} {self.length}'

    def countdown(self) -> datetime.timedelta:
        curr_time = datetime.datetime.now()
        diff = self.start_time.astimezone(pytz.UTC) - curr_time.astimezone(pytz.UTC)
        return diff

class CFSpider:
    def __init__(self, retry_times: int = 5):
        self.url = r'https://codeforces.com/contests'
        self.retry_times = retry_times
        self.is_fetched = False
        self.prepare()

    def prepare(self):
        for i in range(self.retry_times):
            with eventlet.Timeout(1):
                if i != 0: print(f'Retry {i} times ...')
                try:
                    self.html_raw = requests.get(self.url, timeout=10)
                    if self.html_raw.status_code == 200:
                        self.is_fetched = True
                except:
                    pass
            if self.is_fetched:
                print('Get cf contests succeeded.')
                break
        if not self.is_fetched:
            print('Can`t get cf content info.')
            return

    def get_recent_contest(self, amount: int = 1, countdown_limit_hours: int = 36) -> list[CFContest]:
        if not self.is_fetched: return
        self.html_soup = BeautifulSoup(self.html_raw.text, 'lxml')
        selectors = []
        ret = []
        for i in range(amount):
            selectors.append(f'#pageContent > div.contestList > div.datatable > div:nth-child(6) > table > tr:nth-child({i + 2})');
        for selector in selectors:
            data = self.html_soup.select(selector)
            new_append = CFContest(
                name = str.strip(data[0].select('td:nth-child(1)')[0].text),
                start_time = str.strip(data[0].select('td:nth-child(3)')[0].text),
                length = str.strip(data[0].select('td:nth-child(4)')[0].text),
            )
            if new_append.countdown().days <= countdown_limit_hours // 24 and new_append.countdown().seconds // 3600 < countdown_limit_hours % 24:
                ret.append(new_append)
        return ret
