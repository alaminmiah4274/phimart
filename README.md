# PhiMart - E-commerce API with Django REST Framework

![Django REST Framework](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT Authentication](https://img.shields.io/badge/JWT-Authentication-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Swagger Documentation](https://img.shields.io/badge/Swagger-Documentation-%2385EA2D?style=for-the-badge&logo=swagger&logoColor=black)

PhiMart is a robust e-commerce API built with Django REST Framework that provides endpoints for product management, order processing, shopping cart functionality, and user authentication.

## Features

- **JWT Authentication** using Djoser
- **Product Management** with categories
- **Shopping Cart** functionality
- **Order Processing** system
- **Swagger Documentation** with drf_yasg
- **RESTful** API design

## API Documentation

Swagger documentation is available at:

```
https://127.0.0.1:8000/swagger/
```

Redoc documentation is available at:

```
https://127.0.0.1:8000/swagger/
```

## Environment Variables

Create a `.env` file in the root directory and add the following:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
ALLOWED_HOST=*
EMAIL_HOST=your_email
```

## Technologies Used

- **Django** - Backend Framework
- **Django REST Framework (DRF)** - API Development
- **Simple JWT** - JWT Authentication
- **drf-yasg** - API Documentation
- **SQLite** - Database

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/phimart.git
   cd phimart
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   Create a `.env` file in the project root and add your configuration:
   ```bash
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```
5. Run migrations:
   ```bash
   python3 manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python3 manage.py runserver
   ```

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the project
2.  Create your feature branch (git checkout -b feature/AmazingFeature)
3.  Commit your changes (git commit -m 'Add some AmazingFeature')
4.  Push to the branch (git push origin feature/AmazingFeature)
5.  Open a Pull Request

## License

    Distributed under the MIT License. See LICENSE for more information.

## Contact

Al Amin Miah - alaminmiah4274@gmail.com
