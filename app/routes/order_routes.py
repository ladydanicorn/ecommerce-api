from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order, OrderItem
from app.models.product import Product

bp = Blueprint('order', __name__, url_prefix='/api/orders')

@bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    
    if not all(k in data for k in ['customer_id', 'items']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        order = Order(customer_id=data['customer_id'])
        db.session.add(order)
        
        for item_data in data['items']:
            product = Product.query.get_or_404(item_data['product_id'])
            if product.stock < item_data['quantity']:
                db.session.rollback()
                return jsonify({'error': f'Insufficient stock for product {product.name}'}), 400
            
            order_item = OrderItem(
                order=order,
                product_id=product.id,
                quantity=item_data['quantity'],
                price_at_time=product.price
            )
            db.session.add(order_item)
            
            product.stock -= item_data['quantity']
        
        db.session.commit()
        return jsonify({
            'message': 'Order created successfully',
            'order_id': order.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        'id': order.id,
        'customer_id': order.customer_id,
        'status': order.status,
        'order_date': order.order_date.isoformat(),
        'items': [{
            'product_id': item.product_id,
            'quantity': item.quantity,
            'price': item.price_at_time
        } for item in order.items],
        'total': order.calculate_total()
    })