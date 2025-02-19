from flask import Blueprint, request, jsonify, make_response
from functools import wraps
from app import db
from app.models.product import Product

bp = Blueprint('product', __name__, url_prefix='/api/products')

def add_cors_headers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response
    return decorated_function

@bp.route('/', strict_slashes=False, methods=['OPTIONS'])
@add_cors_headers
def handle_options():
    """Handles CORS preflight request"""
    return make_response('', 204)


@bp.route('/', methods=['GET'])
@add_cors_headers
def list_products():
    products = Product.query.all()
    return jsonify({
        'products': [{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'stock': p.stock
        } for p in products]
    })

@bp.route('/', methods=['POST'])
@add_cors_headers
def create_product():
    data = request.get_json()
    
    if not all(k in data for k in ['name', 'price']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        product = Product(
            name=data['name'],
            price=data['price'],
            stock=data.get('stock', 0)
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({
            'message': 'Product created successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'stock': product.stock
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

