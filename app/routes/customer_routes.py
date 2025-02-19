from flask import Blueprint, request, jsonify
from app import db
from app.models.customer import Customer

bp = Blueprint('customer', __name__, url_prefix='/api/customers')

# ✅ Add this route to get all customers
@bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customer_list = [
        {'id': c.id, 'name': c.name, 'email': c.email, 'phone': c.phone}
        for c in customers
    ]
    return jsonify({'customers': customer_list})

@bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()

    if not all(k in data for k in ['name', 'email']):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone')
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({
            'message': 'Customer created successfully',
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone
    })


@bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    
    try:
        if 'name' in data:
            customer.name = data['name']
        if 'email' in data:
            customer.email = data['email']
        if 'phone' in data:
            customer.phone = data['phone']
        
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400