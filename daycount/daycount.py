import calendar
import datetime
import pytz
import numpy as np
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, \
    USMartinLutherKingJr, USPresidentsDay, GoodFriday, USMemorialDay, \
    USLaborDay, USThanksgivingDay
import pandas as pd
from types import NoneType

''' ACTUAL METHODS'''
def actual360_T(start : datetime.datetime, 
                end : datetime.datetime, 
                secs : bool = True):
    '''
    
    Actual/360. Used in money markets for short-term lending of currencies, 
    ESCB monetary policy, and REPO agreemments.

    Resource: https://en.wikipedia.org/wiki/Day_count_convention

    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    `secs` : bool
        Whether to included seconds when calculating the contract's tenor.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''
    if secs:
        divisor = 360 * 24 * 60 * 60
        return (end - start).total_seconds() / divisor

    else:
        divisor = 360
        return (end - start).days / divisor

def actual364_T(start : datetime.datetime, 
                end : datetime.datetime, 
                secs : bool = True):
    '''
    
    Actual/364.
    
    Resource: https://en.wikipedia.org/wiki/Day_count_convention
    
    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    `secs` : bool
        Whether to included seconds when calculating the contract's tenor.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    if secs:
        divisor = 364 * 24 * 60 * 60
        return (end - start).total_seconds() / divisor

    else:
        divisor = 364
        return (end - start).days / divisor

def actual365_T(start : datetime.datetime, 
                end : datetime.datetime, 
                secs : bool = True):
    '''
    
    Actual/365 Fixed.

    Resource: https://en.wikipedia.org/wiki/Day_count_convention

    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    `secs` : bool
        Whether to included seconds when calculating the contract's tenor.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    if secs:
        divisor = 366 * 24 * 60 * 60
        return (end - start).total_seconds() / divisor

    else:
        divisor = 366
        return (end - start).days / divisor

def actual365L_T(start : datetime.datetime, 
                 end : datetime.datetime, 
                 couponFreq : int, 
                 secs : bool = True):
    '''

    Actual/365L.
    
    Resource: https://en.wikipedia.org/wiki/Day_count_convention

    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    `couponFreq` : int
        Number of payments per year.

    `secs` : bool
        Whether to included seconds when calculating the contract's tenor.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    divisor = 365

    if couponFreq != 1:
        if calendar.isleap(end.year):
            divisor = 366
    else:
        for year in range(start.year, end.year + 1):
            if ( start < (datetime.datetime(year, 3, 1) - datetime.timedelta(days=1)) ) and \
                ( (datetime.datetime(year, 3, 1) - datetime.timedelta(days=1)) <= end):
                
                try:
                    datetime.datetime(year, 2, 29)
                    divisor = 366
                    break

                except ValueError as e:
                    continue

    if secs:
        return (end - start).total_seconds() / (divisor * 24 * 60 * 60)
    
    else:
        return (end - start).days / divisor

def actualActualICMA_T(start : datetime.datetime, 
                       end : datetime.datetime, 
                       nextCoupon : datetime.datetime, 
                       couponFreq : int, 
                       secs : bool = True):
    '''
    
    Actual/Actual ICMA. Used for US T-bonds and Notes (among other securities).

    Resource: https://en.wikipedia.org/wiki/Day_count_convention

    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    `nextCoupon` : datetime.datetime
        The date/time of the next payment.
    
    `couponFreq` : int
        Number of payments per year.

    `secs` : bool
        Whether to included seconds when calculating the contract's tenor.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    if secs:
        numerator = (end - start).total_seconds()
        denominator = couponFreq * (nextCoupon - start).total_seconds()
    else:
        numerator = (end - start).days
        denominator = couponFreq * (nextCoupon - start).days

    return numerator / denominator

def actualActualISDA_T(start : datetime.datetime, 
                       end : datetime.datetime, 
                       secs : bool = True):
    '''
    
    Actual/Actual ISDA.

    Resource: https://en.wikipedia.org/wiki/Day_count_convention

    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    `secs` : bool
        Whether to included seconds when calculating the contract's tenor.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    total = 0
    currentDate = start
    
    for year in range(start.year, end.year + 1):
        
        DIY = 366 if calendar.isleap(year) else 365

        if secs:
            divisor = DIY * 24 * 60 * 60

            if year == end.year:
                total += (end - currentDate).total_seconds() / divisor

            else:
                newYear = datetime.datetime(year + 1, 1, 1, 0, 0, 0)
                total += (newYear - currentDate).total_seconds() / divisor
                currentDate = newYear
        else:
            divisor = DIY

            if year == end.year:
                total += (end - currentDate).days / divisor

            else:
                newYear = datetime.datetime(year + 1, 1, 1, 0, 0, 0)
                total += (newYear - currentDate).days / divisor
                currentDate = newYear

    return total

''' 30/360 METHODS '''
def bbThirty360_T(start : datetime.datetime, 
                  end : datetime.datetime, 
                  secs : bool = True):
    '''

    30/360 Bond Basis.
    
    Resource: https://en.wikipedia.org/wiki/Day_count_convention

    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    `secs` : bool
        Whether to included seconds when calculating the contract's tenor.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    startDay = min(start.day, 30)
    
    if startDay > 29:
        endDay = min(end.day, 30)
    else:
        endDay = end.day

    if (end.day == 31) and ((start.day) == 30 or (start.day == 31)):
        endDay = 30
    if start.day == 31:
        startDay = 30

    if secs:
        divisor = 360 * 24 * 60 * 60

        years = (end.year - start.year) * 360 * 24 * 60 * 60
        months = (end.month - start.month) * 30 * 24 * 60 * 60
        days = (endDay - startDay) * 24 * 60 * 60
        hours = (end.hour - start.hour) * 60 * 60
        minutes = (end.minute - start.minute) * 60
        seconds = (end.second - start.second)

        return (years + months + days + hours + minutes + seconds) / divisor
    
    else:
        divisor = 360

        years = (end.year - start.year) * 360
        months = (end.month - start.month) * 30
        days = (endDay - startDay)
        
        return (years + months + days) / divisor

def _lastFebDay(dateTime : datetime.datetime):
    if dateTime.month == 2:
        _, last_of_month = calendar.monthrange(dateTime.year, dateTime.month)
        if dateTime.day == last_of_month:
            return True
    return False

def usThirty360_T(start : datetime.datetime, 
                  end : datetime.datetime, 
                  eomPayments : bool, 
                  secs : bool = True):
    '''

    30/360 US. Used for US Corporate bond and many US agency issues.
    
    Resource: https://en.wikipedia.org/wiki/Day_count_convention

    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    `eomPayments` : bool
        Whether payments are received at the every end of the month.

    `secs` : bool
        Whether to included seconds when calculating the contract's tenor.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    startDay = start.day
    endDay = end.day
    
    if eomPayments:
        if _lastFebDay(start) and _lastFebDay(end):
            endDay = 30
        if _lastFebDay(start):
            startDay = 30

    if (endDay == 31) and ((startDay) == 30 or (startDay == 31)):
        endDay = 30
    if startDay == 31:
        startDay = 30

    if secs:
        divisor = 360 * 24 * 60 * 60

        years = (end.year - start.year) * 360 * 24 * 60 * 60
        months = (end.month - start.month) * 30 * 24 * 60 * 60
        days = (endDay - startDay) * 24 * 60 * 60
        hours = (end.hour - start.hour) * 60 * 60
        minutes = (end.minute - start.minute) * 60
        seconds = (end.second - start.second)

        return (years + months + days + hours + minutes + seconds) / divisor

    else:
        divisor = 360

        years = (end.year - start.year) * 360
        months = (end.month - start.month) * 30
        days = (endDay - startDay)

        return (years + months + days) / divisor

def euroThirty360_T(start : datetime.datetime, 
                    end : datetime.datetime, 
                    secs : bool = True):
    '''

    30E/360.
    
    Resource: https://en.wikipedia.org/wiki/Day_count_convention

    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    `secs` : bool
        Whether to included seconds when calculating the contract's tenor.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    endDay = end.day
    startDay = start.day

    if end.day == 31:
        endDay = 30

    if start.day == 31:
        startDay = 30

    if secs:
        divisor = 360 * 24 * 60 * 60

        years = (end.year - start.year) * 360 * 24 * 60 * 60
        months = (end.month - start.month) * 30 * 24 * 60 * 60
        days = (endDay - startDay) * 24 * 60 * 60
        hours = (end.hour - start.hour) * 60 * 60
        minutes = (end.minute - start.minute) * 60
        seconds = (end.second - start.second)

        return (years + months + days + hours + minutes + seconds) / divisor
    
    else:
        divisor = 360

        years = (end.year - start.year) * 360
        months = (end.month - start.month) * 30
        days = (endDay - startDay)

        return (years + months + days) / divisor

def euroISDAThirty360_T(start : datetime.datetime, 
                        end : datetime.datetime, 
                        endIsMaturity : bool, 
                        secs : bool = True):
    '''

    30E/360 ISDA.
    
    Resource: https://en.wikipedia.org/wiki/Day_count_convention

    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    `endIsMaturity` : bool
        Whether the expiration of the contract is considered the maturity of 
        the contract.

    `secs` : bool
        Whether to included seconds when calculating the contract's tenor.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    startDay = start.day
    endDay = end.day

    _, lastOfMonth = calendar.monthrange(start.year, start.month)
    if start.day == lastOfMonth:
        startDay = 30

    _, lastOfMonth = calendar.monthrange(end.year, end.month)
    if (end.day == lastOfMonth) and not (endIsMaturity and (end.month == 2)):
        endDay = 30


    if secs:
        divisor = 360 * 24 * 60 * 60

        years = (end.year - start.year) * 360 * 24 * 60 * 60
        months = (end.month - start.month) * 30 * 24 * 60 * 60
        days = (endDay - startDay) * 24 * 60 * 60
        hours = (end.hour - start.hour) * 60 * 60
        minutes = (end.minute - start.minute) * 60
        seconds = (end.second - start.second)

        return (years + months + days + hours + minutes + seconds) / divisor

    else:
        divisor = 360

        years = (end.year - start.year) * 360
        months = (end.month - start.month) * 30
        days = (endDay - startDay)

        return (years + months + days) / divisor

''' CUSTOM METHODS '''
class USTradingCalendar(AbstractHolidayCalendar):
    rules = [USMartinLutherKingJr,
             USPresidentsDay,
             GoodFriday,
             USMemorialDay,
             Holiday("Juneteenth", month=6, day=19),
             Holiday('IndependenceDay', month=7, day=4, observance=nearest_workday),
             #USLaborDay,
             USThanksgivingDay,
             Holiday('Christmas', month=12, day=25, observance=nearest_workday),
             Holiday('NewYearsEve', month=1, day=1, observance=nearest_workday)]

CAL = USTradingCalendar()
CST = pytz.timezone("CST6CDT")

def trading_TS(start : datetime.datetime, end : datetime.datetime):
    '''

    "TS" = "Tenor Simple": Counts the number of business days until a 
    contract's expiration (adjusted for holidays).

    *note* Converts datetimes provided to CST for US holiday filtering. Ignores
    initial start day if timestamped past 1600 CST and ignores final day if
    timestamped before 0930 CST.
    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    # adjusted timezone for calendar filters
    newStart = start.astimezone(CST)
    newEnd = end.astimezone(CST)

    # adjust dates
    if newStart.hour >= 16:
        newStart += datetime.timedelta(days=1)
    
    if (newEnd <= newEnd.replace(hour=9, minute=30, second=0, microsecond=0)):
        newEnd -= datetime.timedelta(days=1)

    # business day count is start inclusive and end exclusive (adding 1).
    tradingDays = np.busday_count(newStart.date(), 
                                  newEnd.date() + datetime.timedelta(days=1), 
                                  holidays=np.array(CAL.holidays(newStart.replace(hour=0, minute=0, second=0, microsecond=0), 
                                                                 newEnd), 
                                                                 dtype="datetime64[D]"))

    # get count for next year of trading days
    DIY = 366 if calendar.isleap(newStart.year) else 365
    oneYearAhead = newStart + datetime.timedelta(days=DIY)
    yearlyTradingDays = np.busday_count(newStart.date(), 
                                        oneYearAhead.date(), 
                                        holidays=np.array(CAL.holidays(newStart.replace(hour=0, minute=0, second=0, microsecond=0), 
                                                                       oneYearAhead), dtype="datetime64[D]"))

    return tradingDays / yearlyTradingDays

def trading_seconds(start : datetime.datetime | None = None, end : datetime.datetime | None = None) -> float:
    '''
    
    Returns the number of trading seconds between two dates.
    
    *note* Converts datetimes provided to CST for US holiday filtering, removing
    1 hour from every 24h trading day for market close between 1600-1700 CST.
    
    Parameters
    ----------
    `start` : datetime.datetime
        The date to begin counting from (inclusive). If None (default), uses 
        current date/time.

    `end` : datetime.datetime | None = None
        The date to count up to (inclusive). If None (default), will use 1
        year ahead of the start date - ie. defaults to trading days in a year.
    
    Returns
    -------
    `float`
        The number of seconds in the upcoming trading period specified.

    '''

    # default start
    if isinstance(start, NoneType):
        start = datetime.datetime.now(tz=datetime.UTC)

    # default end (one year from start)
    if isinstance(end, NoneType):
        DIY = 366 if calendar.isleap(start.year) else 365
        end = start + datetime.timedelta(DIY)

    # adjusted timezone for calendar filters
    newStart = start.astimezone(CST)
    newEnd = end.astimezone(CST)
    holidays = CAL.holidays(newStart.replace(hour=0, minute=0, second=0, microsecond=0), newEnd).to_numpy(dtype="datetime64[D]")

    # catch same day start / end
    if newStart.date() == newEnd.date():

        # Sundays, limit market to open
        if newStart.weekday() == 6:
            if newEnd.hour >= 17:
                totalSeconds = (newEnd - max(newStart, newStart.replace(hour=17, minute=0, second=0, microsecond=0))).total_seconds()
            else:
                totalSeconds = 0
        
        # Weekdays, handle as usual and subtract closed hours
        elif newStart.weekday() in [0, 1, 2, 3]:
            
            # either ends before 1600 or starts after 1700
            if (newEnd.hour < 16) or (newStart.hour >= 17):
                totalSeconds = (newEnd - newStart).total_seconds()
            
            # starts and ends during close
            elif (newStart.hour == 16) and (newEnd.hour == 16):
                totalSeconds = 0

            # starts during close, shift to open
            elif newStart.hour == 16:
                totalSeconds = (newEnd - newStart.replace(hour=17, minute=0, second=0, microsecond=0)).total_seconds()
            
            # ends during close, shift to close
            elif newEnd.hour == 16:
                totalSeconds = (newEnd.replace(hour=16, minute=0, second=0, microsecond=0) - newStart).total_seconds()

            elif (newStart.hour < 16) and (newEnd.hour >= 17):
                totalSeconds = ( newEnd - newStart - datetime.timedelta(hours=1) ).total_seconds()

        # Fridays, limit market to close
        elif newStart.weekday() == 4:
            if newStart.hour < 16:
                totalSeconds = (min(newEnd.replace(hour=16, minute=0, second=0, microsecond=0), newEnd) - newStart).total_seconds()
            else:
                totalSeconds = 0
    
    # otherwise, multi-day period
    else:
        # np.busday_count() formatting:
        startDate = newStart.date()
        endDate = (newEnd + datetime.timedelta(days=1)).date() # np.busday_count() is exclusive of end date

        weekdays = np.busday_count(startDate, endDate, weekmask="1111000", holidays=holidays)
        fridays = np.busday_count(startDate, endDate, weekmask="0000100", holidays=holidays)
        sundays = np.busday_count(startDate, endDate, weekmask="0000001", holidays=holidays)

        # count seconds
        totalSeconds = weekdays * 82800 # 0000 - 1600, 1700 - 2359
        totalSeconds += fridays * 57600 # 0000 - 1600
        totalSeconds += sundays * 25200 # 1700 - 2359

        # adjust back for start time
        if newStart.replace(hour=0, minute=0, second=0, microsecond=0) not in holidays:
            if newStart.weekday() == 6:
                if newStart.hour >= 17:
                    nextDay = (newStart + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                    totalSeconds -= (25200 - (nextDay - newStart).total_seconds())

            elif newStart.weekday() in [0, 1, 2, 3]:
                if newStart.hour >= 17:
                    nextDay = (newStart + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                    totalSeconds -= (82800 - (nextDay - newStart).total_seconds())

                elif newStart.hour == 16:
                    totalSeconds -= 57600

                elif newStart.hour < 16:
                    nextDay = (newStart + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                    totalSeconds -= (86400 - (nextDay - newStart).total_seconds()) # added 1h back: 82800 -> 86400
            
            elif newStart.weekday() == 4:
                if newStart.hour < 16:
                    totalSeconds -= (57600 - (newStart.replace(hour=16, minute=0, second=0, microsecond=0) - newStart).total_seconds())
                else:
                    totalSeconds -= 57600
        
        # adjust back for end time
        if newEnd.replace(hour=0, minute=0, second=0, microsecond=0) not in holidays:
            if newEnd.weekday() == 6:
                if newEnd.hour >= 17:
                    totalSeconds -= (25200 - (newEnd - newEnd.replace(hour=17, minute=0, second=0, microsecond=0)).total_seconds())
                else:
                    totalSeconds -= 25200
                
            elif newEnd.weekday() in [0, 1, 2, 3]:
                if newEnd.hour >= 17:
                    totalSeconds -= (86400 - (newEnd - newEnd.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()) # added 1h back: 82800 -> 86400

                elif newEnd.hour == 16:
                    totalSeconds -= 25200
                
                elif newEnd.hour < 16:
                    totalSeconds -= (82800 - (newEnd - newEnd.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
            
            else:
                if newEnd.hour < 16:
                    totalSeconds -= (57600 - (newEnd - newEnd.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())

    return totalSeconds

def trading_days(start : datetime.datetime | None = None, end : datetime.datetime | None = None) -> float:
    '''
    
    Returns the number of trading days between two dates (partials included).
    If all arguments are "None", returns trading days in the upcoming year.
    
    *note* Converts datetimes provided to CST for US holiday filtering, removing
    1 hour from every 24h trading day for market close between 1600-1700 CST.
    
    Parameters
    ----------
    `start` : datetime.datetime
        The date to begin counting from (inclusive). If None (default), uses 
        current date/time.

    `end` : datetime.datetime | None = None
        The date to count up to (inclusive). If None (default), will use 1
        year ahead of the start date - ie. defaults to trading days in a year.
    
    Returns
    -------
    `float`
        The number of days in the upcoming trading period specified.

    '''

    # divide by 23 hours in day vs 24 to adjust for 1h close
    return trading_seconds(start, end) / (23 * 60 * 60)

def trading_T(start : datetime.datetime, end : datetime.datetime):
    '''

    Calculates tenor of currency futures (or options) contracts, accounting
    for seconds.

    *note* Converts datetimes provided to CST for US holiday filtering, removes
    1 hour from every full tradingday for market close between 1600-1700 CST.
    
    
    Parameters
    ----------
    `start` : datetime.datetime
        The "current" date/time from the contract's point of view.

    `end` : datetime.datetime
        The expiration / settlement / maturity of the contract.

    Returns
    -------
    `float`
        The length of time until the contract's expiration, expressed as a 
        fraction of a year.

    '''

    # trading seconds in period / trading seconds in upcoming year
    return trading_seconds(start, end) / trading_seconds(start)






