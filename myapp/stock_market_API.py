from vnstock import *
import pytz

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
        yesterday = current_datetime - timedelta(days=1)
        today_date = yesterday.strftime("%Y-%m-%d")
    else:
        # If it's Saturday or Sunday, return the date of the last Friday
        last_friday = current_datetime - timedelta(days=current_datetime.weekday() + 2)
        today_date = last_friday.strftime("%Y-%m-%d")

    print(today_date)
    return today_date

def get_date_x_days_before(input_date_str, x):
    try:
        # Define the Vietnam timezone
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

        # Parse the input date string into a datetime object in the Vietnam timezone
        input_datetime = vietnam_tz.localize(datetime.strptime(input_date_str, "%Y-%m-%d"))

        # Check if the input date is a Monday
        if input_datetime.weekday() == 0:  # Monday is represented by 0
            # Adjust the result to be the Friday of the previous week
            result_datetime = input_datetime - timedelta(days=(x + 2 + 7) % 7)
        else:
            # Calculate the date x days before the input date
            result_datetime = input_datetime - timedelta(days=x)

        # Convert the result back to the "YYYY-MM-DD" format and return it in Vietnam timezone
        result_date = result_datetime.strftime("%Y-%m-%d")

        return result_date
    except ValueError:
        return "Invalid date format. Please use 'YYYY-MM-DD'."

def get_index_data (name, type):
    today_date_in_vietnam = get_today_date_in_vietnam()
    the_day_before = get_date_x_days_before(today_date_in_vietnam, 1)
    
    if type == 'index':
        df1 = stock_ohlc(name, today_date_in_vietnam, today_date_in_vietnam, '3', 'index')
        df2 = stock_ohlc(name, the_day_before, the_day_before, '1D', 'index')

        json_data1 = df1.to_json(orient='records') 
        json_data2 = df2.to_json(orient='records')

        # Parse the JSON string to a JSON object
        parsed_json_data1 = json.loads(json_data1)
        parsed_json_data2 = json.loads(json_data2)

        parsed_json_data = parsed_json_data2 + parsed_json_data1

    elif type == 'stock':
        df = stock_ohlc(name, today_date_in_vietnam, today_date_in_vietnam, '1D', 'stock')

        json_data = df.to_json(orient='records')

        # Parse the JSON string to a JSON object
        parsed_json_data = json.loads(json_data)

    return parsed_json_data

# def get_stock_data (name):
#     print(name)
#     today_date_in_vietnam = get_today_date_in_vietnam()
    
#     df = stock_ohlc(name, today_date_in_vietnam, today_date_in_vietnam, '1D', 'stock')

#     json_data = df.to_json(orient='records')

#     # Parse the JSON string to a JSON object
#     parsed_json_data = json.loads(json_data)

#     print('data from vnstock: ', parsed_json_data)

#     return parsed_json_data


def get_stock_data(stock):
    print('start fetching ', stock)
    url = "https://finance.vietstock.vn/data/GetStockBySector_V3"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie":
        "language=vi-VN; Theme=Light; dable_uid=undefined; isShowLogin=true; AnonymousNotification=; _gid=GA1.2.1147915689.1688370205; ASP.NET_SessionId=t40pxcvenvdzz0fkx5r32yzh; __RequestVerificationToken=BNhp45MadU2bWY6gT1j0R_ezgd5vGZkEGSox4RYrGBBPg0CQVWYqFEIXfHSequEgtTLUlj14TK9SC-KxI8Sm-go7EG6nvWsZL9nd68Ak_Ro1; cto_bundle=gIziwl9MMWJrQnNBOFJPbVVkcmw3bnB2JTJCc1FHT05KNlFnZE0lMkZQMnZHc284U0NSQ3dxUDlrekFUcGI2JTJGYyUyRkF3cWpqQzVkZHR3JTJGQW9TcnNRdjVFJTJGRDZtME4yM3pFNnNKaGhFUjRBWGolMkZ5ZnlURzIlMkZGU09MRG1BSmVmUHJzV3NwT2hDblJyejFTRUVHanNNSU80b2IlMkZxM0VMaHclM0QlM0Q; finance_viewedstock=AAA,; _ga_EXMM0DKVEX=GS1.1.1688417776.26.1.1688418275.59.0.0; _ga=GA1.2.835457032.1688366445; _gat_UA-1460625-2=1; __gads=ID=702ba60129a42c1f-22affee385e200c9:T=1688366444:RT=1688418277:S=ALNI_MYQYL8IfxHvxAebvR3JM5N4PBOQ7Q; __gpi=UID=00000c1d5e40c01b:T=1688366444:RT=1688418277:S=ALNI_MZN7ndpv0gCJxbWsVs_h4VpxFV8bQ",
        "Origin": "https://finance.vietstock.vn",
        "Referer": "https://finance.vietstock.vn/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua":
        '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    data = {
        'filter[exchangeId]':
        '0',
        'filter[exchange][id]':
        '0',
        'filter[exchange][text]':
        'Tất cả',
        'filter[sectorId]':
        '0',
        'filter[sector][id]':
        '0',
        'filter[sector][text]':
        'Tất cả',
        'filter[capitalId]':
        '0',
        'filter[capital][id]':
        '0',
        'filter[capital][text]':
        'Tất cả',
        'filter[totalVal][]': ['0', '3000'],
        'filter[totalVol][]': ['0', '500'],
        'filter[totalValMatching][]': ['0', '3000'],
        'filter[totalVolMatching][]': ['0', '500'],
        'filter[totalValPut][]': ['0', '3000'],
        'filter[totalVolPut][]': ['0', '500'],
        'filter[foreignBuyVal][]': ['0', '3000'],
        'filter[foreignBuyVol][]': ['0', '500'],
        'filter[foreignSellVal][]': ['0', '3000'],
        'filter[foreignSellVol][]': ['0', '500'],
        'filter[perChange][]': ['-15.00', '15.00'],
        'filter[closePrice][]': ['0', '2000000'],
        'filter[basicPrice][]': ['0', '2000000'],
        'filter[floorPrice][]': ['0', '2000000'],
        'filter[ceilingPrice][]': ['0', '2000000'],
        'sectorID':
        '0',
        'catID':
        '0',
        'capitalID':
        '0',
        'languageID':
        '1',
        '__RequestVerificationToken':
        'YdIdxdDgYbjEPyW8nB2mfpEZHa6URsNDjHgpCxMvNSsTsnuOjgLJIjtC67ZTeaD-iLFutDNfGpJrFLGs8DYsGAHMho6gAJzRqVUDzuRT9ig1'
    }

    response = requests.post(url, headers=headers, data=data)
    json_data = response.json()
    items = json_data['data']

    # Value to search for
    target_value = stock

    # Initialize an empty list to store matching documents
    matching_documents = []

    # Iterate through the array and check for the desired key-value pair
    for document in items:
        if document.get('_sc_') == target_value:
            matching_documents.append(document)


    for data in matching_documents:
        # Extract the data from each item
        # machungkhoan = data['_sc_']
        # von_hoa = data['_vhtt_'] * 1000000000
        # gia_tran = data['_bp_']
        # gia_san = data['_fp_']
        # gia_mo_cua = data['_op_']
        gia_dong_cua = data['_cp_']
        thay_doi = data['change']
        # thay_doi_pt = data['_pc_']
        # klgd = data['_tvolmatching_']
        # gtgd = data['_tvalmatching_']
        # nn_buy_vol = data['_foreignbuyvol_']
        # nn_buy = data['_foreignbuyval_']
        # nn_sell_vol = data['_foreignsellvol_']
        # nn_sell = data['_foreignsellval_']
        # Create the filter/query for the item


        trading_data = {
            'market_price': gia_dong_cua,
            'change': thay_doi
        }
    
    print(trading_data)

    return trading_data

