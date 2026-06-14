# Library Management System

A Python-based command-line Library Management System that helps manage books, borrowers, returns, fines, and transaction history using CSV file storage.

## Features

- Admin login
- Add new books
- Update existing book details
- Delete books
- Display all books
- Search books by title, author, keyword, category, or book ID
- Filter books by availability, borrowed status, overdue status, or unavailable status
- Borrow books
- Return books
- Fine calculation for overdue books
- Fine payment tracking
- View borrowed books by user
- Display borrower records
- View issue and return history
- Dashboard with total books, copies, borrowed books, overdue books, and pending fines
- CSV-based data storage

## Technologies Used

- Python
- CSV file handling
- Command-line interface

## Files Used

The project uses the following CSV files to store data:

- `books.csv` - stores book details
- `borrowers.csv` - stores currently borrowed book records
- `history.csv` - stores issue and return history
- `admin.csv` - stores admin login details

If these files are not present, the program can create the required admin file automatically.

## Default Admin Login

```text
Username: admin
Password: admin123
```

Note: The admin password is stored in plain text because this is a beginner-level learning project. In real-world applications, secure password hashing should be used.

## How to Run

1. Make sure Python is installed on your system.

2. Clone the repository:

```bash
git clone https://github.com/sruthika-19/library-management-system-python
```

3. Open the project folder:

```bash
cd library-management-system
```

4. Run the program:

```bash
python main.py
```

## User Roles

### Admin

The admin can:

- Add books
- Update book details
- Delete books
- View all books
- Search and filter books
- View borrower records
- View issue/return history
- Check overdue reports
- View dashboard summary

### User

The user can:

- Search books
- Filter books
- View all books
- Borrow books
- Return books
- Pay overdue fines
- View their borrowed books

## Borrowing Rules

- A user can borrow a maximum of 3 books.
- A user cannot borrow the same book twice at the same time.
- The default borrowing period is 14 days.
- Fine is calculated for overdue books.
- Fine rate is 3 units per day.

## Project Purpose

This project was created as a beginner-friendly Python project to practice:

- Functions
- Classes and objects
- File handling
- CSV data storage
- Input validation
- Conditional statements
- Loops
- Basic CRUD operations
- Real-world problem solving

## Future Improvements

- Use password hashing for admin login
- Add a graphical user interface
- Use a database like SQLite or MySQL
- Add student/member IDs
- Add book reservation feature
- Add automated testing
- Export reports
