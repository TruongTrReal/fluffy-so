# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from .stock_market_API import get_index_data, get_stock_data
from .mysql_query import connect_sql, account_exists, add_or_modify_a_stock, get_account_summary, add_or_modify_summary, create_or_get_account, delete_a_stock, delete_all_stocks_for_account, get_all_stocks_for_account

class StockAPI(APIView):
    def get(self, request):
        data_type = request.GET.get('data_type') 
        stock_name = request.GET.get('stock_name')  

        if data_type == 'index':
            return Response(get_index_data(stock_name, data_type))
        elif data_type == 'stock':
            return Response(get_index_data(stock_name, data_type))
        else:
            return Response({"error": "Invalid stock name"})
        

@api_view(['POST'])
def add_or_modify_stock(request):
    """
    Endpoint to add or modify a stock for an account.
    """
    try:
        conn = connect_sql()

        account_type = request.data.get('account_type')
        account_number = request.data.get('account_number')
        stock_data = request.data.get('stock_data')

        print(account_type, account_number, stock_data)

        account_id = create_or_get_account(conn, account_type, account_number)

        if not account_exists(conn, account_type, account_number):
            return JsonResponse({"error": f"Account with account_id {account_id} does not exist and fail to create."}, status=status.HTTP_404_NOT_FOUND)

        success = add_or_modify_a_stock(conn, account_id, stock_data)

        if success:
            return Response({"success": True})
        else:
            return JsonResponse({"error": "Failed to add or modify the stock."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
def delete_stock(request, account_number, account_type, symbol):
    """
    Endpoint to delete a stock for an account.
    """
    try:
        conn = connect_sql()
        account_id = create_or_get_account(conn, account_type, account_number)
        
        if not account_exists(conn, account_type, account_number):
            return JsonResponse({"error": f"Account with account_id {account_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        success = delete_a_stock(conn, account_id, symbol)

        if success:
            return Response({"success": True})
        else:
            return JsonResponse({"error": f"Failed to delete the stock with symbol {symbol}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_stocks(request, account_number, account_type):
    """
    Endpoint to get all stocks for an account.
    """
    try:
        conn = connect_sql()

        account_id = create_or_get_account(conn, account_type, account_number)

        if not account_exists(conn, account_type, account_number):
            return JsonResponse({"error": f"Account with account_id {account_id} does not exist and fail to create."}, status=status.HTTP_404_NOT_FOUND)

        stocks = get_all_stocks_for_account(conn, account_id)

        # Call the function get_stock_data(name of stock) for each stock
        enhanced_stocks = []
        for stock in stocks:
            stock_data = get_stock_data(stock['stock_symbol'])
            enhanced_stock = {
                **stock, 
                'market_price': stock_data['market_price'], 
                'change':  stock_data['change']
            }
            enhanced_stocks.append(enhanced_stock)

        return Response({"stocks": enhanced_stocks})

    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_account_summary_api(request, account_number, account_type):
    try:
        conn = connect_sql()

        account_id = create_or_get_account(conn, account_type, account_number)

        if not account_exists(conn, account_type, account_number):
            return JsonResponse({"error": f"Account with account_id {account_id} does not exist and fail to create."}, status=status.HTTP_404_NOT_FOUND)

        summary = get_account_summary(conn, account_id)

        return Response({"summary": summary})

    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_or_modify_summary_api(request):
    try:
        conn = connect_sql()

        print(request.data)

        account_type = request.data.get('account_type')
        account_number = request.data.get('account_number')
        total_asset = request.data.get('total_asset')
        total_cash = request.data.get('total_cash')
        margin_ratio = request.data.get('margin_ratio')


        account_id = create_or_get_account(conn, account_type, account_number)

        if not account_exists(conn, account_type, account_number):
            return JsonResponse({"error": f"Account with account_id {account_id} does not exist and fail to create."}, status=status.HTTP_404_NOT_FOUND)

        success = add_or_modify_summary(conn, account_id, total_asset, total_cash, margin_ratio)

        if success:
            return Response({"success": True})
        else:
            return JsonResponse({"error": "Failed to add or modify the summary."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)