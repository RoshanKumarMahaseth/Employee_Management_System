# 👨‍💼 Employee Management System

A modern Employee Management System built with **Flask** that allows administrators to efficiently manage employee records. The application provides secure authentication and an intuitive interface for adding, updating, viewing, and deleting employee information.

---

## 🚀 Features

- 🔐 User Authentication (Register & Login)
- 👤 Employee Dashboard
- ➕ Add New Employee
- ✏️ Update Employee Details
- 🗑️ Delete Employee Records
- 📋 View All Employees
- 🔍 Search Employees
- ✅ Form Validation
- 📱 Responsive User Interface

---

## 🛠️ Tech Stack

- **Backend:** Flask
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF
- **Frontend:** HTML5, CSS3, Bootstrap
- **Templating:** Jinja2

---

## 📂 Project Structure

```
Employee-Management-System/
│
├── apps/
│   │
│   ├── __init__.py
│   ├── models.py
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   │
│   ├── employees/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   │
│   ├── admin/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── login.html
│   ├── register.html
│   ├── reset_request.html
│   ├── reset_token.html
│   ├── dashboard.html
│   ├── add_employee.html
│   ├── edit_employee.html
│   ├── employees.html
│   ├── employee_details.html
│   └── users.html
│
├── static/
│   └── ...
│
├── instance/
│   └── site.db              # DON'T upload to GitHub
│
├── .env                    # DON'T upload
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/Employee_Management_System.git
```

### Navigate to the project

```bash
cd Employee_Management_System
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python run.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```


## 🎯 Future Improvements

- Profile Picture Upload
- Attendance Tracking
- Email Notifications
- REST API Support

---

## 👨‍💻 Author

**Roshan Kumar Mahaseth**

GitHub: https://github.com/RoshanKumarMahaseth

---

## 📄 License

This project is developed for learning purposes and is open for educational use.