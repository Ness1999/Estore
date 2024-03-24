from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime 
from .models import * 
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed





def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store.html', context)

def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		print('CART:', cart)

		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

		for i in cart:
			try:
				cartItems+=cart[i]['quantity']

				product=Product.objects.get(id=i)
				total=(product.price*cart[i]['quantity'])

				order['get_cart_total']+=total
				order['get_cart_items']+=cart[i]['quantity']

				item={
					'product':{
						'id':product.id,
						'name':product.name,
						'price': product.price,
						'imageURL':product.imageURL,
					},
					'quantity':cart[i]['quantity'],
					'get_total':total
				}
				items.append(item)

				if product.digital==False:
					order['shipping']=True

			except:
				pass

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)

@csrf_exempt

def checkout(request):
    if isinstance(request.user, AnonymousUser):
        # If the user is not authenticated, redirect them to the login page
        return redirect('login')

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)

from django.http import JsonResponse

@csrf_exempt
def updateItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productId = data.get('productId')  # Use get method to avoid KeyError if productId is None
        action = data['action']
        print('Received productId:', productId)
        print('Action:', action)

        if productId is None:
            # Handle the case where productId is None (e.g., clear action)
            # Clear the cart and return JsonResponse indicating success
            Order.objects.filter(customer=request.user.customer, complete=False).delete()
            return JsonResponse({'message': 'Cart cleared'}, status=200)

        # Proceed with normal processing for other actions (add, remove)
        customer = request.user.customer
        try:
            product = Product.objects.get(id=productId)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse({'message': 'Item updated'}, status=200)

    else:
        return HttpResponseNotAllowed(['POST'])





@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
            order.save()

            # Clear the cart after the order is completed
            order.orderitem_set.all().delete()
            # Alternatively, you can use the clear method if you have a ManyToManyField
            # order.products.clear()

            if order.shipping:
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                )

            return JsonResponse('Payment complete', safe=False)
        else:
            return JsonResponse('Payment failed', safe=False)
    else:
        return JsonResponse('User is not logged in', safe=False)
