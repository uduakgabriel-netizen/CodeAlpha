🍽️ RestoTrack — Restaurant Management & Tracking System

RestoTrack is a powerful and user-friendly restaurant management system built with Django REST Framework (DRF).
It allows restaurant administrators and staff to efficiently manage menu items, table reservations, inventory, and customer orders — all in one place.
Customers can place orders and book tables seamlessly, while the admin can monitor every activity via a powerful dashboard.

🚀 Features
👥 User Management

Secure user registration and login using JWT authentication.

Role-based access for admin, staff, and customers.

Staff and admin users can be created through the admin panel.

🧾 Menu Management

Staff/Admin can create, update, and delete menu items.

Customers can view available menu items in real time.

🪑 Table Management

Track restaurant tables and their statuses (free, reserved, etc.).

Staff/Admin can manage tables from the admin dashboard or API.

📦 Inventory Management

Manage stock levels of ingredients or supplies.

Only accessible to staff and admin users.

🧍‍♂️ Order Management

Customers can place orders from available menu items.

Staff/Admin can view, update order status (pending, preparing, served, etc.).

Automatic total calculation including subtotal, tax, and service charge.

📅 Reservation System

Customers can book tables only when they’re available.

Admin and staff can view and manage all reservations.

🔐 Authentication

JWT-based authentication for secure access.

Integrated with djangorestframework-simplejwt.

🛠️ Tech Stack
Component	Technology
Backend Framework	Django 5 + Django REST Framework
Authentication	JWT (via djangorestframework-simplejwt)
Database	SQLite (default, easily switchable to PostgreSQL/MySQL)
Language	Python 3
API Testing	Django REST Framework UI / Postman
Deployment Ready	Yes (supports environment variable configuration)
⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/<uduakgabriel-netizen>/RestoTrack.git
cd RestoTrack

2. Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On Mac/Linux

3. Install Dependencies
pip install -r requirements.txt

4. Apply Migrations
python manage.py makemigrations
python manage.py migrate

5. Create Superuser
python manage.py createsuperuser

6. Run Development Server
python manage.py runserver


Now visit http://127.0.0.1:8000/

The admin panel is available at: http://127.0.0.1:8000/admin/

🧭 API Endpoints Overview
Endpoint	Method	Description	Access
/api/auth/register/	POST	Register a new user	Public
/api/auth/login/	POST	Login and obtain JWT token	Public
/api/menu/	GET/POST/PUT/DELETE	Manage menu items	Staff/Admin
/api/tables/	GET/POST/PUT/DELETE	Manage tables	Staff/Admin
/api/inventory/	GET/POST/PUT/DELETE	Manage inventory	Staff/Admin
/api/orders/	GET/POST	Create and manage orders	Authenticated users
/api/orders/{id}/update_status/	POST	Update order status	Staff/Admin
/api/reservations/	GET/POST/PUT/DELETE	Manage reservations	Authenticated users
🧑‍💼 Admin Panel

RestoTrack includes a full-featured Django Admin Panel where staff and administrators can:

Manage users, menu items, tables, inventory, and orders.

Track reservations and monitor daily restaurant operations.

URL: http://127.0.0.1:8000/admin/

🧩 Project Structure
RestoTrack/
├── mealtracker/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   └── admin.py
├── RestoTrack/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt

🔮 Next Steps (In Progress)

Frontend integration is under development and will be built with:

React + TypeScript

Responsive design for desktop and mobile

Interactive dashboard for restaurant staff and customers

API consumption from the Django backend

📢 Contribution

Contributions are welcome!
If you’d like to improve RestoTrack or add new features:

Fork the repository.

Create a new branch (feature/your-feature).

Commit your changes.

Submit a pull request.

🧑‍💻 Developer

👨‍💻 Uduak Gabriel
Backend Developer | Django & REST Framework Enthusiast
🌐 GitHub
 • 💼 LinkedIn

📝 License
MIT License

Copyright (c) 2025 Uduak Gabriel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
