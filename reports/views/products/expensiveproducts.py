import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product
from reports.views import Connection


def expensiveproduct_list(request):
    """Function to build an HTML report of products over $1000"""
    if request.method == 'GET':
        # connect to database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

        # query all products over $1000
        db_cursor.execute("""
              SELECT 
                *
              FROM bangazonapi_product
              WHERE bangazonapi_product.price >= 1000 
              ORDER BY bangazonapi_product.price ASC
        """)

        dataset = db_cursor.fetchall()

        product_list = []

        for row in dataset:
            # create a product instance and set its properties
            product = Product()
            product.pk = row["id"]
            product.name = row["name"]
            product.price = row["price"]
            product.description = row["description"]
            product.quantity = row["quantity"]
            product.created_date = row["created_date"]
            product.location = row["location"]

            product_list.append(product)

    template = 'products/list_expensive_products.html'
    context = {
        'product_list': product_list
    }

    return render(request, template, context)
