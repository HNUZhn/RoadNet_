import time
import pandas as pd
def gpsTimeDivide(filename):
    iURL = filename
    csvdata = pd.read_csv(iURL)
    Year = []
    Mon = []
    Day = []
    Hour = []
    Min = []
    Sec = []
    Wday = []
    Yday = []
    for temp in csvdata["GPSTime"]:
        year = time.strptime(temp, '%Y-%m-%d %H:%M:%S').tm_year	#年份，如 2017
        Year.append(year)
        mon = time.strptime(temp, '%Y-%m-%d %H:%M:%S').tm_mon	#月份，取值范围为[1, 12]
        Mon.append(mon)
        day = time.strptime(temp, '%Y-%m-%d %H:%M:%S').tm_mday	#一个月中的第几天，取值范围为[1-31]
        Day.append(day)
        hour = time.strptime(temp, '%Y-%m-%d %H:%M:%S').tm_hour	#小时， 取值范围为[0-23]
        Hour.append(hour)
        min_ = time.strptime(temp, '%Y-%m-%d %H:%M:%S').tm_min	#分钟，取值范围为[0, 59]
        Min.append(min_)
        sec = time.strptime(temp, '%Y-%m-%d %H:%M:%S').tm_sec	#秒，取值范围为[0, 61]
        Sec.append(sec)
        wday = time.strptime(temp, '%Y-%m-%d %H:%M:%S').tm_wday	#一个星期中的第几天，取值范围为[0-6]，0表示星期一
        Wday.append(wday)
        yday = time.strptime(temp, '%Y-%m-%d %H:%M:%S').tm_yday	#一年中的第几天，取值范围为[1, 366]
        Yday.append(yday)

    csvdata['Year'] = Year
    csvdata['Mon'] = Mon
    csvdata['Day'] = Day
    csvdata['Hour'] = Hour
    csvdata['Min'] = Min
    csvdata['Sec'] = Sec
    csvdata['Wday'] = Wday
    csvdata['Yday'] = Yday

    csvdata.to_csv('street_SZ.csv')
    return 0
gpsTimeDivide('street2.csv')