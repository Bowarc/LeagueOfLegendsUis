from datetime import datetime


def getDate(Separator="/"):
    date = str(datetime.now())[:10].replace("-", Separator)
    return date


def getDateYear():
    year = getDate()[:4]
    return year


def getDateMonth():
    month = getDate()[5:7]
    return month


def getDateDay():
    day = getDate()[8:]
    return day


def getHour():
    hour = str(datetime.now())[11:13]
    return hour


def getMinutes():
    minutes = str(datetime.now())[14:16]
    return minutes


def getSecconds():
    secconds = str(datetime.now())[17:19]
    return secconds


if __name__ == "__main__":

    print(f"Hours: {getHour()}\nMinutes: {getMinutes()}\nSecconds: {getSecconds()}\nYear is: {getDateYear()}\nMonth is: {getDateMonth()}\nDay is: {getDateDay()}")
