import pytz
from datetime import datetime, timedelta

def get_today_date_in_vietnam():
    # Define the Vietnam timezone
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

    # Get the current date and time in Vietnam timezone
    current_datetime = datetime.now(vietnam_tz)

    if current_datetime.weekday() < 5 and current_datetime.hour >= 9 and current_datetime.minute >= 15:
        # If it's a weekday and the time is greater than or equal to 9:15 AM, return today's date
        today_date = current_datetime.strftime("%Y-%m-%d")
    elif current_datetime.weekday() == 0:
        # If it's Monday and before 9:15 AM, return the date of the last Friday
        last_friday = current_datetime - timedelta(days=current_datetime.weekday() + 3)
        today_date = last_friday.strftime("%Y-%m-%d")
    elif 5 > current_datetime.weekday() > 0:
        # If it's Tuesday to Friday, return yesterday's date
        yesterday = current_datetime
        today_date = yesterday.strftime("%Y-%m-%d")
    elif current_datetime.weekday() == 5:
        # If it's Saturday, return the date of the last Friday
        last_friday = current_datetime - timedelta(days=current_datetime.weekday() + 1)
        today_date = last_friday.strftime("%Y-%m-%d")
    else:
        # If it's Sunday, return the date of the last Friday
        last_friday = current_datetime - timedelta(days=current_datetime.weekday() + 2)
        today_date = last_friday.strftime("%Y-%m-%d")

    return today_date

print(get_today_date_in_vietnam())
