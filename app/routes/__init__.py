from .customer_routes import bp as customer_bp
from .product_routes import bp as product_bp
from .order_routes import bp as order_bp

__all__ = ['customer_bp', 'product_bp', 'order_bp']