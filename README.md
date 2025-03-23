# Expense Tracker API

A simple expense tracker API built with Django and FastAPI.

## Features
- User authentication (To be added)
- Expense tracking
- Category management
- Reports & summaries (To be added)

## Prerequisites
Make sure you have the following installed:
- Python (latest available version)
- SQLite (default database, can be changed later)

## Setup Instructions

1. **Clone the Repository**
```sh
git clone https://github.com/shetty456/expense-tracker-api.git
cd expense-tracker-api
```

2. **Create a Virtual Environment**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install Dependencies**
```sh
pip install -r requirements.txt
```

4. **Run Database Migrations**
```sh
python manage.py migrate
```

5. **Start the Development Server**
```sh
python manage.py runserver
```

6. **API Endpoints** (To be added)
   - `/api/expenses/` - List all expenses
   - `/api/expenses/{id}/` - Get details of a specific expense
   - `/api/categories/` - List all categories
   - More endpoints will be documented soon.

## Running with Makefile
Instead of manually running commands, you can use:
```sh
make run
```

## Future Enhancements
- Add Docker support
- Implement authentication
- Write unit tests
- Improve documentation

## Contributions
Contributions are welcome! Feel free to fork and submit PRs.

## License
MIT License

