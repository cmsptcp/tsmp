from datetime import datetime, timedelta
import pytz
import app_config as cfg


# format: YYYY-MM-DDTHH:mm:ssZ (ISO 8601 / RFC 3339)
def play(time):
    try:
        function_with_exception429()
    except Exception as error:
        for i in range(0, len(error.args)):
            print(f'args[{i}]: {error.args[i]}, type: {type(error.args[i])}')
        if error.args[0] == 429:
            print("było 429")
        else:
            print("nie było 429")


def function_with_exception400():
    pass
    raise Exception(400, "błąd aaa")


def function_with_exception429():
    pass
    raise Exception(429, "błąd aaa")


def is_stock_market_open(time_to_be_checked):
    if type(time_to_be_checked) == str:
        tmp_time = datetime.strptime(time_to_be_checked, cfg.DATE_TIME_STRING_FORMAT)
        utc_time = pytz.utc.localize(tmp_time)
    else:
        utc_time = time_to_be_checked

    est_time = utc_time.astimezone(pytz.timezone("America/New_York"))
    weekday = est_time.weekday()
    if (9 <= est_time.hour <= 16) and weekday < 5:
        print(f'Day: {weekday}, Time: {time_to_be_checked} == {est_time} EST is inside or near stock market '
              f'opening hours')
        return True
    print(f'Day: {weekday}, Time: {time_to_be_checked} == {est_time} EST is outside stock market opening hours')
    return False


if __name__ == '__main__':
    utc_now = pytz.utc.localize(datetime.utcnow())
    est_now = utc_now.astimezone(pytz.timezone("America/New_York"))
    week_ago = (utc_now - timedelta(days=7))

    play(week_ago)

    print(utc_now.strftime(cfg.DATE_TIME_STRING_FORMAT))
    is_stock_market_open(utc_now.strftime(cfg.DATE_TIME_STRING_FORMAT))
    is_stock_market_open(utc_now)
