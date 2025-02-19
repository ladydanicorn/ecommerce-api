from flask import Blueprint, request, jsonify, make_response
from functools import wraps
from app import db
from app.models.order import Order, OrderItem
from app.models.product import Product

bp = Blueprint('order', __name__, url_prefix='/api/orders')

def add_cors_headers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response
    return decorated_function

@bp.route('', methods=['OPTIONS'])
@bp.route('/', methods=['OPTIONS'])
@add_cors_headers
def handle_options():
    """Handles CORS preflight request"""
    return make_response('', 204)

@bp.route('', methods=['GET'])
@bp.route('/', methods=['GET'])
@add_cors_headers
def get_orders():
    orders = Order.query.all()
    return jsonify({
        'orders': [{
            'id': order.id,
            'customer_id': order.customer_id,
            'customer_name': order.customer.name,
            'order_date': order.order_date.isoformat(),
            'total_price': order.calculate_total()
        } for order in orders]
    })

@bp.route('', methods=['POST'])
@bp.route('/', methods=['POST'])
@add_cors_headers
def create_order():
    data = request.get_json()
    print("Received order data:", data)  # Debug print
    
    if not all(k in data for k in ['customer_id', 'items']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Convert customer_id to integer if it's a string
        customer_id = int(data['customer_id'])
        order = Order(customer_id=customer_id)
        db.session.add(order)
        
        # Filter out items with zero quantity
        valid_items = [item for item in data['items'] if item.get('quantity', 0) > 0]
        
        if not valid_items:
            return jsonify({'error': 'No valid items in order'}), 400
        
        for item_data in valid_items:
            product = Product.query.get_or_404(item_data['product_id'])
            quantity = int(item_data['quantity'])
            
            if product.stock < quantity:
                db.session.rollback()
                return jsonify({'error': f'Insufficient stock for product {product.name}'}), 400
            
            order_item = OrderItem(
                order=order,
                product_id=product.id,
                quantity=quantity,
                price_at_time=product.price
            )
            db.session.add(order_item)
            
            # Update product stock
            product.stock -= quantity
        
        db.session.commit()
        return jsonify({
            'message': 'Order created successfully',
            'order_id': order.id
        }), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': 'Invalid numeric value provided'}), 400
    except Exception as e:
        db.session.rollback()
        print("Error creating order:", str(e))  # Debug print
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['GET'])
@bp.route('/<int:id>/', methods=['GET'])
@add_cors_headers
def get_order(id):
    try:
        order = Order.query.get_or_404(id)
        return jsonify({
            'id': order.id,
            'customer_id': order.customer_id,
            'customer_name': order.customer.name,
            'status': order.status,
            'order_date': order.order_date.isoformat(),
            'items': [{
                'product_id': item.product_id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.price_at_time)
            } for item in order.items],
            'total_price': sum(item.quantity * item.price_at_time for item in order.items)
        })
    except Exception as e:
        print(f"Error getting order {id}:", str(e))  # Debug print
        return jsonify({'error': f'Failed to load order: {str(e)}'}), 500