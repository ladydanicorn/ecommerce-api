# E-commerce API

A Flask-based REST API for e-commerce operations including customer management, product catalog, and order processing.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MySQL database:
- Create a database named 'ecommerce_db'
- Update database credentials in app/config.py if needed

5. Initialize the database:
```bash
python setup.py
```

6. Run the application:
```bash
python run.py
```

## API Endpoints

### Customer Management
- `POST /api/customers/` - Create customer
- `GET /api/customers/<id>` - Get customer details
- `PUT /api/customers/<id>` - Update customer
- `DELETE /api/customers/<id>` - Delete customer

### Product Management
- `POST /api/products/` - Create product
- `GET /api/products/` - List all products
- `GET /api/products/<id>` - Get product details
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Order Management
- `POST /api/orders/` - Create order
- `GET /api/orders/<id>` - Get order details

## Testing

Use Postman or similar tools to test the endpoints. Example request for creating a customer:

```json
POST /api/customers/
{
    "name": "Doctor Worm",
    "email": "drworm@example.com",
    "phone": "1234567890"
}
```