# TECHYASTUTE EXPENSE TRACKER

A full-stack, server-rendered web application built with Python and [Flask](https://github.com) for managing personal expenses, tracking budgets, and viewing financial breakdowns.

---

## Features

- **Server-Side Rendering**: Built with Jinja2 templates and styled with CSS/Bootstrap.
- **User Authentication**: Secure registration, login, and logout tracking using `Flask-Login`.
- **Expense Management**: Full CRUD capabilities to add, view, update, and delete expenses.
- **Dynamic Dashboards**: Summary spending by category breakdowns.
- **Database Persistence**: SQLite database managed via SQLAlchemy ORM.

---

## tech Stack

- **Backend / Routing**: Python 3.10+, Flask
- **Frontend**: Jinja2 Templates, HTML5, CSS3 (Bootstrap)
- **Database**: SQLite (SQLAlchemy ORM)
- **Forms & Validation**: Flask-WTF

---

## 📁 Project Structure

```text
expense-tracker/
├── src/
│   ├── __init__.py
│   ├── models.py         # SQLAlchemy database models
│   ├── forms.py          # Flask-WTF form classes
│   ├── routes.py         # App view routing and logic
│   ├── templates/        # Jinja2 HTML views
│   │   ├── base.html     # Shared layout (navbar, footer)
│   │   ├── home.html     # Dashboard / Expense list / Summary list
│   │   ├── create_expense.html     # Create a new expense
│   │   ├── update_expense.html     # Update expense details
│   │   ├── delete_expense.html     # Delete expense 
│   │   ├── login.html    # Authentication views
│   │   ├── signup.html    # Register new user views
├── instance/             # Local SQLite database files
├── requirements.txt      # Python dependencies
├── app.py                # Application entry point
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Samuwar
cd /SkillsForge-ExpenseTracker
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Variables
Create a `.env` file in the root directory:
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-form-key-here
SQLALCHEMY_DATABASE_URI=sqlite:///expenses.db
```

### 5. Run the Application
```bash
flask run
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Key Application Routes

| Route | HTTP Method | View Template | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | `index.html` | User dashboard displaying recent expenses and totals. |
| `/login` | `GET`, `POST` | `login.html` | Handles user authentication and session management. |
| `/signup` | `GET`, `POST` | `signup.html`| Account creation page. |
| `/create_expense` | `GET`, `POST` | `create_expense.html` | Form to create a new expense item. |
| `/update_expense/<id>`| `GET`, `POST` | `update_expense.html` | Prefilled form to modify an existing item. |
| `/delete_expense/delete/<id>`| `POST` | `delete_expense.html` | Form target to securely delete an entry. |

---

