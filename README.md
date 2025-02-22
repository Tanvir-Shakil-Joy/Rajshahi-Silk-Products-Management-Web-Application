# Rajshahi Silk Products Management Web Application

A Django-based web application designed to manage the silk products catalog for the Rajshahi Silk Industry. This application provides a comprehensive solution for managing silk product inventory, including product listing, searching, and CRUD operations.

## Features

- Product Management (CRUD Operations)
- Search functionality for products
- Responsive and modern user interface
- Form validation and error handling
- Admin interface for product management

## Technologies Used

- Python 3.13
- Django 5.1.5
- SQLite3
- HTML5
- CSS3

## Installation

Follow these steps to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/Tanvir-Shakil-Joy/Rajshahi-Silk-Products-Management-Web-Application.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Rajshahi-Silk-Products-Management-Web-Application
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Unix/macOS
   ```

4. Install dependencies:
   ```bash
   pip install django
   ```

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the application: [http://localhost:8000](http://localhost:8000)
- Admin interface: [http://localhost:8000/admin](http://localhost:8000/admin)
- Manage products:
  - Add new products using the "Add New Product" button.
  - Search for products using the search bar.
  - Edit or delete products using the action buttons.

## Project Structure

```
silk_catalog/
├── manage.py
├── silk_catalog/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── silk_products/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/
│   ├── base.html
│   └── silk_products/
│       ├── product_list.html
│       ├── product_form.html
│       └── product_confirm_delete.html
└── static/
    └── css/
        └── style.css
```

## Contributing

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/new-feature
   ```
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Author

**Tanvir Shakil Joy**

## Acknowledgments

- Django Documentation
- Bootstrap for design inspiration
