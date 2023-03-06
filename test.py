from cf import CFContest, CFSpider

cfs = CFSpider()
HOURS = 100
contest_list = cfs.get_recent_contest(countdown_limit_hours=HOURS)
print(contest_list)
