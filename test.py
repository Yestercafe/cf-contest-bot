from cf import CFContest, CFSpider

cfs = CFSpider()
HOURS = 200
contest_list = cfs.get_recent_contest(5, countdown_limit_hours=HOURS)
print(contest_list)
print(contest_list[0].countdown_as_str())
