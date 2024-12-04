from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product

bp = Blueprint('product', __name__, url_prefix='/api/products')

@bp.route('/', methods=['POST'])
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
                'price': product.price
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/', methods=['GET'])
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

@bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'stock': product.stock
    })
