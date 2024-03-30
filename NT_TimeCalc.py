from decimal import Decimal
import datetime

#converts raw 18-digit timestamp into a datetime format
def ticks_to_DT(ticks):
    ticksPD = Decimal(864000000000)

    days = Decimal(ticks) / ticksPD

    remaining_ticks = Decimal(ticks) % ticksPD

    baseDate = datetime.datetime(1, 1, 1)
    delta = datetime.timedelta(days=int(days), microseconds=int(remaining_ticks) // 10)
    return baseDate + delta

#converts datetime into readable format
def fmtTime(timeInput):
    dtObj = ticks_to_DT(int(timeInput))
    frmDT = dtObj.strftime("%Y-%m-%d %H:%M:%S")
    return(frmDT)
