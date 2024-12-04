from functools import wraps
from flask import jsonify, request
from datetime import datetime

def validate_json(*required_fields):
    """
    Decorator to validate JSON request data
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Missing JSON in request'}), 400
            
            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return jsonify({
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                }), 400
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def format_datetime(dt):
    """
    Format datetime object to string
    """
    return dt.isoformat() if dt else None

def handle_error(e):
    """
    Generic error handler
    """
    return jsonify({
        'error': str(e),
        'timestamp': datetime.utcnow().isoformat(),
        'type': e.__class__.__name__
    }), 500

def validate_email(email):
    """
    Basic email validation
    """
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """
    Basic phone number validation
    """
    import re
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone))

def paginate_results(query, page=1, per_page=10):
    """
    Helper function to paginate query results
    """
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        'items': pagination.items,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }

def generate_order_number():
    """
    Generate a unique order number
    Format: ORD-YYYYMMDD-XXXXX (where X is a random number)
    """
    import random
    date_str = datetime.utcnow().strftime('%Y%m%d')
    random_str = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    return f'ORD-{date_str}-{random_str}'

def calculate_order_total(items):
    """
    Calculate total price for a list of order items
    """
    return sum(item.quantity * item.price_at_time for item in items)

def check_stock_levels(products):
    """
    Check if products need restocking
    Returns list of products that need restocking (stock <= restock_threshold)
    """
    restock_threshold = 10
    return [
        product for product in products 
        if product.stock <= restock_threshold
    ]

def format_currency(amount):
    """
    Format currency amount
    """
    return f"${amount:.2f}"

def sanitize_input(text):
    """
    Basic input sanitization
    """
    import html
    if isinstance(text, str):
        return html.escape(text.strip())
    return text