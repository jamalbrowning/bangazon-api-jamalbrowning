import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product
from reports.views import Connection


def completedorder_list(request):
    """Function to build an HTML report of products over $1000"""
    if request.method == 'GET':
        # connect to database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
              SELECT
                bangazonapi_order.id AS "order",
                auth_user.first_name || ' ' || auth_user.last_name as "full name",
                bangazonapi_payment.merchant_name as "payment type",
                SUM(price) as "total price"
              FROM 
                bangazonapi_order
              JOIN 
                bangazonapi_customer  ON bangazonapi_order.customer_id = bangazonapi_customer.id
              JOIN 
                auth_user  ON auth_user.id = bangazonapi_customer.user_id
              JOIN 
                bangazonapi_orderproduct ON bangazonapi_orderproduct.order_id = bangazonapi_order.id
              JOIN 
                bangazonapi_product  ON bangazonapi_product.id = bangazonapi_orderproduct.id
              JOIN 
                bangazonapi_payment  ON bangazonapi_payment.id = bangazonapi_order.payment_type_id
              WHERE 
                bangazonapi_order.payment_type_id IS NOT NULL
              GROUP BY 
                bangazonapi_order.id
        """)

        dataset = db_cursor.fetchall()

        completed_orders = []

        for row in dataset:
            order = {}
            order["order_id"] = row["order"]
            order['full_name'] = row['full name']
            order['payment_type'] = row['payment type']
            order['total_price'] = row['total price']

            completed_orders.append(order)

        template = 'orders/completed_orders.html'
        context = {
            'completed_orders': completed_orders
        }

        return render(request, template, context)
