import os
import django
from django.db.models import Sum, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct


# Create and run queries
def add_records_to_database():
    # Categories
    food_category = Category.objects.create(name='Food')
    drinks_category = (Category.objects.create(name='Drinks'))

    # Food
    product1 = Product.objects.create(name='Pizza', description='Delicious pizza with toppings', price=10.99,
                                      category=food_category, is_available=False)
    product2 = Product.objects.create(name='Burger', description='Classic burger with cheese and fries', price=7.99,
                                      category=food_category, is_available=False)
    product3 = Product.objects.create(name='Apples', description='A bag of juicy red apples', price=3.99,
                                      category=food_category, is_available=True)
    product4 = Product.objects.create(name='Bread', description='A freshly baked loaf of bread', price=2.49,
                                      category=food_category, is_available=True)
    product5 = Product.objects.create(name='Pasta and Sauce Bundle',
                                      description='Package containing pasta and a jar of pasta sauce', price=6.99,
                                      category=food_category, is_available=False)
    product6 = Product.objects.create(name='Tomatoes', description='A bundle of ripe, red tomatoes', price=2.99,
                                      category=food_category, is_available=True)
    product7 = Product.objects.create(name='Carton of Eggs', description='A carton containing a dozen fresh eggs',
                                      price=3.49, category=food_category, is_available=True)
    product8 = Product.objects.create(name='Cheddar Cheese', description='A block of aged cheddar cheese', price=7.99,
                                      category=food_category, is_available=False)
    product9 = Product.objects.create(name='Milk', description='A gallon of fresh cow milk', price=3.49,
                                      category=food_category, is_available=True)

    # Drinks
    product10 = Product.objects.create(name='Coca Cola', description='Refreshing cola drink', price=1.99,
                                       category=drinks_category, is_available=True)
    product11 = Product.objects.create(name='Orange Juice', description='Freshly squeezed orange juice', price=2.49,
                                       category=drinks_category, is_available=False)
    product12 = Product.objects.create(name='Bottled Water', description='A 12-pack of purified bottled water',
                                       price=4.99, category=drinks_category, is_available=True)
    product13 = Product.objects.create(name='Orange Soda', description='A 6-pack of carbonated orange soda', price=5.49,
                                       category=drinks_category, is_available=True)
    product14 = Product.objects.create(name='Bottled Green Tea', description='A bottled green tea', price=3.99,
                                       category=drinks_category, is_available=False)
    product15 = Product.objects.create(name='Beer', description='A bottled craft beer', price=5.49,
                                       category=drinks_category, is_available=True)

    # Customers
    customer1 = Customer.objects.create(username='john_doe')
    customer2 = Customer.objects.create(username='alex_alex')
    customer3 = Customer.objects.create(username='peter132')
    customer4 = Customer.objects.create(username='k.k.')
    customer5 = Customer.objects.create(username='peter_smith')

    # Orders
    order1 = Order.objects.create(customer=customer1)
    order_product1 = OrderProduct.objects.create(order=order1, product=product3, quantity=2)
    order_product2 = OrderProduct.objects.create(order=order1, product=product6, quantity=1)
    order_product3 = OrderProduct.objects.create(order=order1, product=product7, quantity=5)
    order_product4 = OrderProduct.objects.create(order=order1, product=product13, quantity=1)

    order2 = Order.objects.create(customer=customer3)
    order_product5 = OrderProduct.objects.create(order=order2, product=product3, quantity=2)
    order_product6 = OrderProduct.objects.create(order=order2, product=product9, quantity=1)

    order3 = Order.objects.create(customer=customer1)
    order_product5 = OrderProduct.objects.create(order=order3, product=product12, quantity=4)
    order_product6 = OrderProduct.objects.create(order=order3, product=product7, quantity=3)
    return "All data entered!"


def product_quantity_ordered():
    result = []
    orders = Product.objects.annotate(
        total=Sum('orderproduct__quantity')
    ).values('name', 'total').order_by('-total')

    for order in orders:
        result.append(f"Quantity ordered of {order['name']}: {order['total']}")
    return '\n'.join(result)


def ordered_products_per_customer():
    orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')
    result = []

    # for order in orders:
    #     result.append(f'Order ID: {order.id}, Customer: {order.customer.username}')
    #     for ordered_product in order.orderproduct_set.all():
    #         result.append(f'- Product: {ordered_product.product.name}, Category: {ordered_product.category.name}')

    for order in orders:
        result.append(f'Order ID: {order.id}, Customer: {order.customer.username}')
        for ordered_product in order.orderproduct_set.all():
            product = ordered_product.product  # Get the related Product instance
            category = product.category  # Get the Category of the Product
            result.append(f'- Product: {product.name}, Category: {category.name}')

    return '\n'.join(result)


def filter_products():
    products = Product.objects.filter(
        Q(is_available=True) &
        Q(price__gt=3)
    ).order_by(
        '-price',
        'name'
    )
    result = []
    for p in products:
        result.append(f'{p.name}: {p.price}lv.')

    return '\n'.join(result)


def give_discount():
    query = Q(is_available=True) & Q(price__gt=3.00)
    product_to_be_discounted = Product.objects.filter(query).order_by('-price', 'name')
    product_to_be_discounted.update(price=F('price') * 0.7)
    available_products = Product.objects.filter(is_available=True).order_by('-price', 'name')
    return '\n'.join(f'{product.name}: {product.price}lv.' for product in available_products)


# Run and print your queries
# print(add_records_to_database())
# print(product_quantity_ordered())
# print(ordered_products_per_customer())
# print(filter_products())
# print(give_discount())