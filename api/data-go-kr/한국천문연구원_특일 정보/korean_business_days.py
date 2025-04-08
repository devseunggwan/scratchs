import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import requests
from dotenv import load_dotenv
load_dotenv(override=True)


def get_holidays_in_month(month_range: int = 6) -> list[str]:
    """한국천문연구원 특일 정보 API를 사용하여 공휴일을 가져옵니다.
    
    Args:
        month_range (int): 찾으려는 개월 범위. Defaults to 6.

    Returns:
        list[str]: 공휴일 리스트 ["YYYYMMDD"]
    """
    
    
    result = []
    
    __now = datetime.now()
    __url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
    __params = {
        "_type": "json",
        'serviceKey' : os.getenv("DATA_API_KEY"), 
        'pageNo' : '1', 
        'numOfRows' : '20', 
        'solYear' : __now.year, 
        'solMonth' : f"{__now.month}".rjust(2, "0") 
    }
    
    for month in range(month_range + 1):
        __target_datetime = __now + relativedelta(months=month)
        __params["solYear"] = __target_datetime.year
        __params["solMonth"] = f"{__target_datetime.month}".rjust(2, "0")
        
        __resp = requests.get(__url, params=__params)
        
        if __resp.status_code == 200:
            # 결과가 없는 경우 str
            items: dict | str = __resp.json()["response"]["body"]["items"]
            
            if type(items) == dict:
                # 1개만 나오면 딕셔너리 아이템 하나만 있다.
                # list[dict]는 1개 이상일 떄 반환
                items: dict | list = items["item"]
                
                if type(items) == dict:
                    result.append(items)
                else:
                    result.extend(items)
    
    result = sorted(set([str(item["locdate"]) for item in result]))
    
    return result


def get_weekdays_in_month(month_range: int = 6, date_format: str = "%Y%m%d") -> list[str]:
    """지정한 달 내에 있는 주말(토, 일)에 대한 리스트를 제공합니다.

    Args:
        month_range (int): 찾으려는 개월 범위. Defaults to 6.
        date_format (str): 반환활 날짜 문자열 포맷. Defaults to "%Y%m%d" (YYYYMMDD).

    Returns:
        list[str]: 주말 리스트 [{date_format}]
    """
    result = []
    
    __now = datetime.now()
    __saterday = __now + timedelta(days=5-__now.weekday())
    __sunday = __now + timedelta(days=6-__now.weekday())   
    
    __last_month_day = (__now + relativedelta(months=month_range+1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    while __saterday < __last_month_day and __sunday < __last_month_day:
        if __saterday < __last_month_day:
            result.append(__saterday.strftime(date_format))
        if __sunday < __last_month_day:
            result.append(__sunday.strftime(date_format))
            
        __saterday += timedelta(days=7)
        __sunday += timedelta(days=7)
        
    return result


def get_business_days_in_holidays(holidays: list[str] = [], month_range: int = 6, date_format: str = "%Y%m%d") -> dict[str, bool]:
    """공휴일 리스트를 받아서 실행일부터 지정 기간 이내까지 영업일인지 확인할 수 있는 딕셔너리를 반환합니다.

    Args:
        holidays (list[str]): 공휴일(주말, 임시공휴일 등)이 표기된 리스트. Defaults to [].
        month_range (int, optional): 찾으려는 개월 범위. Defaults to 6.
        date_format (str, optional): 공휴일 리스트의 날짜 포맷. Defaults to "%Y%m%d" (YYYYMMDD).

    Returns:
        dict[str, bool]: 영업일(True), 공휴일(True)
    """
    
    
    result = {}
        
    __now = datetime.now()
    __last_month_day = (__now + relativedelta(months=month_range+1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    for __day in range((__last_month_day - __now).days + 1):
        __date = (__now + timedelta(days=__day)).strftime(date_format)
        result[__date] = __date not in holidays
        
        
    return result


def korean_business_days(month_range: int = 6, date_format: str = "%Y%m%d") -> dict[str, bool]:
    """지정한 달 내에 있는 영업일, 공휴일 정보를 가져옵니다.

    Args:
        month_range (int): 찾으려는 개월 범위. Defaults to 6.
        date_format (str): 반환활 날짜 문자열 포맷. Defaults to "%Y%m%d" (YYYYMMDD).

    Returns:
        dict[str, bool]: 영업일(True), 공휴일(True)
    """
    
    holidays = get_holidays_in_month(month_range=month_range)
    weekdays = get_weekdays_in_month(month_range=month_range, date_format=date_format)
    
    return get_business_days_in_holidays(holidays=holidays+weekdays, month_range=month_range, date_format=date_format)


if __name__ == "__main__":
    from pprint import pprint
    
    pprint(korean_business_days())