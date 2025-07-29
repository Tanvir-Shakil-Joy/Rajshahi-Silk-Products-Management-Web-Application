# Rajshahi Silk Products Management Web Application

A comprehensive Django-based web application designed to manage the silk products catalog for the Rajshahi Silk Industry. This application provides a complete solution for managing silk product inventory with both web interface and REST API functionality, user authentication, role-based permissions, and email notifications.

## Features

### Core Features
- **Product Management (CRUD Operations)** - Create, read, update, and delete silk products
- **User Authentication & Authorization** - Registration, login, logout with role-based access
- **User Roles** - Seller and Buyer roles with different permissions
- **Search Functionality** - Advanced search for products by name, type, and description
- **Email Notifications** - Contact seller functionality with email integration
- **Responsive UI** - Modern and mobile-friendly user interface
- **Form Validation** - Comprehensive client and server-side validation
- **Admin Interface** - Django admin for product and user management

### API Features
- **REST API** - Complete RESTful API for all operations
- **JWT Authentication** - Token-based authentication for API access
- **API Documentation** - Well-structured API endpoints
- **Product Statistics** - API endpoint for product analytics
- **User Profile Management** - API for user profile operations

### Product Features
- **Product Types** - Support for Saree, Fabric, Scarf, and Shawl
- **Product Details** - Name, type, price, availability, description, owner
- **Ownership Management** - Products linked to specific sellers
- **Availability Tracking** - Track product availability status
- **Timestamps** - Created and updated timestamps for all products

### Security Features
- **Permission-based Access** - Role-based permissions for different operations
- **Owner-only Editing** - Only product owners can edit/delete their products
- **Form Validation** - Prevent negative prices and invalid data
- **CSRF Protection** - Built-in Django CSRF protection

## Technologies Used

- **Backend**: Python 3.13, Django 5.2.4
- **Database**: SQLite3
- **API**: Django REST Framework
- **Authentication**: Django Auth + JWT (Simple JWT)
- **Frontend**: HTML5, CSS3, Bootstrap-inspired design
- **Email**: Django Email Backend
- **Testing**: Django TestCase, REST Framework APITestCase

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Tanvir-Shakil-Joy/Rajshahi-Silk-Products-Management-Web-Application.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd Rajshahi-Silk-Products-Management-Web-Application
   ```

3. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Unix/macOS
   # or
   venv\Scripts\activate  # For Windows
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser for admin access:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Usage

### Web Interface
- **Main Application**: [http://localhost:8000](http://localhost:8000)
- **Admin Interface**: [http://localhost:8000/admin](http://localhost:8000/admin)
- **User Registration**: [http://localhost:8000/register](http://localhost:8000/register)
- **Login**: [http://localhost:8000/login](http://localhost:8000/login)

### Web Features
- **Product Management**: Add, edit, delete products (sellers only)
- **Product Search**: Search products by name, type, or description
- **Contact Sellers**: Send emails to product owners
- **User Profiles**: Manage user information and roles

### API Endpoints

#### Authentication
- `POST /api/token/` - Obtain JWT token pair
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/register/` - User registration
- `GET /api/profile/` - Get user profile
- `POST /api/logout/` - Logout user (blacklist token)

#### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product (authenticated sellers only)
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product (owner only)
- `DELETE /api/products/{id}/` - Delete product (owner only)
- `GET /api/products/stats/` - Get product statistics

### API Usage Examples

#### Register a new user:
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword",
    "password_confirm": "securepassword",
    "first_name": "John",
    "last_name": "Doe",
    "role": "seller",
    "phone": "01234567890"
  }'
```

#### Get JWT token:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepassword"
  }'
```

#### Create a product:
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Beautiful Silk Saree",
    "type": "saree",
    "price": "2500.00",
    "availability": true,
    "description": "Handwoven silk saree from Rajshahi"
  }'
```

## Project Structure

```
Rajshahi-Silk-Products-Management-Web-Application/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── db.sqlite3
├── silk_catalog/                 # Main project directory
│   ├── init .py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
├── silk_products/               # Main application
│   ├── init .py
│   ├── admin.py                 # Admin interface configuration
│   ├── api_urls.py              # API URL patterns
│   ├── api_views.py             # REST API views
│   ├── apps.py                  # App configuration
│   ├── forms.py                 # Django forms
│   ├── models.py                # Database models
│   ├── serializers.py           # DRF serializers
│   ├── tests.py                 # Test cases
│   ├── urls.py                  # Web URL patterns
│   ├── views.py                 # Web views
│   ├── migrations/              # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_silkproduct_name_alter_silkproduct_type.py
│   │   ├── 0003_silkproduct_description_silkproduct_owner_and_more.py
│   │   └── init .py
│   └── management/              # Custom management commands
│       └── commands/
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   ├── registration/           # Authentication templates
│   │   ├── login.html
│   │   └── register.html
│   └── silk_products/          # Product templates
│       ├── product_list.html
│       ├── product_detail.html
│       ├── product_form.html
│       └── product_confirm_delete.html
└── static/                     # Static files
└── css/
└── style.css           # Custom styles
```

## Models

### UserProfile
- Extends Django User model
- Fields: role (seller/buyer), phone
- One-to-one relationship with User

### SilkProduct
- Fields: name, type, price, availability, owner, description
- Timestamps: created_at, updated_at
- Foreign key relationship with User (owner)

## Testing

The application includes comprehensive test coverage:

```bash
# Run all tests
python manage.py test

# Run specific test classes
python manage.py test silk_products.tests.SilkProductModelTest
python manage.py test silk_products.tests.SilkProductAPITest
python manage.py test silk_products.tests.EmailFunctionalityTest
```

### Test Coverage
- Model tests
- Form validation tests
- View tests (web interface)
- API tests (REST endpoints)
- Authentication tests
- Permission tests
- Email functionality tests
- Integration tests

## Contributing

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/new-feature
   ```
3. **Make your changes and add tests**
4. **Run tests to ensure everything works:**
   ```bash
   python manage.py test
   ```
5. **Commit your changes:**
   ```bash
   git commit -m "Add new feature: description"
   ```
6. **Push to the branch:**
   ```bash
   git push origin feature/new-feature
   ```
7. **Open a Pull Request**

## Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation for API changes
- Use meaningful commit messages
- Ensure all tests pass before submitting PR

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Author

**Tanvir Shakil Joy**
- GitHub: [@Tanvir-Shakil-Joy](https://github.com/Tanvir-Shakil-Joy)

## Acknowledgments

- Django Documentation
- Django REST Framework Documentation
- Bootstrap for design inspiration
- Simple JWT for authentication
- SQLite for database management

## Changelog

### Latest Updates
- Added comprehensive REST API with JWT authentication
- Implemented user roles (seller/buyer) with permissions
- Added email notification system for seller contact
- Enhanced product management with ownership controls
- Improved form validation and error handling
- Added comprehensive test suite
- Updated project structure and documentation
