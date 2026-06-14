import csv
import getpass
from datetime import datetime, timedelta

BOOKS_FILE = "books.csv"
BORROWERS_FILE = "borrowers.csv"
HISTORY_FILE = "history.csv"
ADMIN_FILE = "admin.csv"

DATE_FORMAT = "%Y-%m-%d"


class Library:
    fine_per_day = 3
    borrow_days = 14

    book_fields = [
        "Book ID", "Title", "Author", "Category",
        "Total Copies", "Available Copies", "Status"
    ]

    borrower_fields = [
        "Borrower", "Book ID", "Title", "Author",
        "Borrow Date", "Due Date", "Fine Paid", "Fine Amount"
    ]

    history_fields = [
        "Transaction ID", "Borrower", "Book ID", "Title", "Author",
        "Action", "Borrow Date", "Due Date", "Return Date", "Fine"
    ]

    admin_fields = ["Username", "Password"]

    def __init__(self):
        self.books = []
        self.borrowers = []
        self.history = []

        self.ensure_admin_file()
        self.load_books()
        self.load_borrowers()
        self.load_history()

    # ---------------- FILE HANDLING ----------------

    def ensure_admin_file(self):
        try:
            with open(ADMIN_FILE, "r", newline="") as file:
                reader = list(csv.DictReader(file))
                if reader:
                    return
        except FileNotFoundError:
            pass

        with open(ADMIN_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.admin_fields)
            writer.writeheader()
            writer.writerow({"Username": "admin", "Password": "admin123"})

        print("Default admin account created.")
        print("Username: admin")
        print("Password: admin123")
        print("Note: Password is stored in plain text for learning/demo purpose.")

    def load_books(self):
        self.books.clear()

        try:
            with open(BOOKS_FILE, "r", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    total = int(row.get("Total Copies") or row.get("Copies") or 0)
                    available = int(row.get("Available Copies") or row.get("Copies") or 0)

                    self.books.append({
                        "Book ID": row.get("Book ID", "").strip(),
                        "Title": self.format_string(row.get("Title", "")),
                        "Author": self.format_string(row.get("Author", "")),
                        "Category": self.format_string(row.get("Category", "General")),
                        "Total Copies": total,
                        "Available Copies": available,
                        "Status": self.format_string(row.get("Status", "Available"))
                    })

        except FileNotFoundError:
            pass
        except ValueError:
            print("books.csv contains invalid copy values.")

    def save_books(self):
        with open(BOOKS_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.book_fields)
            writer.writeheader()
            writer.writerows(self.books)

    def load_borrowers(self):
        self.borrowers.clear()

        try:
            with open(BORROWERS_FILE, "r", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    self.borrowers.append({
                        "Borrower": self.format_string(row.get("Borrower", "")),
                        "Book ID": row.get("Book ID", "").strip(),
                        "Title": self.format_string(row.get("Title", "")),
                        "Author": self.format_string(row.get("Author", "")),
                        "Borrow Date": row.get("Borrow Date", "").strip(),
                        "Due Date": row.get("Due Date", "").strip(),
                        "Fine Paid": row.get("Fine Paid", "False").strip(),
                        "Fine Amount": row.get("Fine Amount", "0").strip()
                    })

        except FileNotFoundError:
            pass

    def save_borrowers(self):
        with open(BORROWERS_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.borrower_fields)
            writer.writeheader()
            writer.writerows(self.borrowers)

    def load_history(self):
        self.history.clear()

        try:
            with open(HISTORY_FILE, "r", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    self.history.append(row)

        except FileNotFoundError:
            pass

    def save_history(self):
        with open(HISTORY_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.history_fields)
            writer.writeheader()
            writer.writerows(self.history)

    

    # ---------------- VALIDATION AND FORMATTING ----------------

    def format_string(self, value):
        return " ".join(word.capitalize() for word in value.strip().split())

    def input_non_empty(self, message):
        while True:
            value = input(message).strip()

            if value:
                return self.format_string(value)

            print("Input cannot be empty.")

    def input_positive_int(self, message):
        while True:
            try:
                value = int(input(message).strip())

                if value > 0:
                    return value

                print("Enter a positive number.")

            except ValueError:
                print("Enter a valid number.")

    # ---------------- TABLE DISPLAY ----------------

    def print_table(self, headers, rows):
        if not rows:
            print("No records found.")
            return

        column_widths = []

        for index, header in enumerate(headers):
            max_width = len(str(header))

            for row in rows:
                max_width = max(max_width, len(str(row[index])))

            column_widths.append(max_width)

        separator = "+"

        for width in column_widths:
            separator += "-" * (width + 2) + "+"

        print("\n" + separator)

        header_row = "|"
        for index, header in enumerate(headers):
            header_row += " " + str(header).ljust(column_widths[index]) + " |"

        print(header_row)
        print(separator)

        for row in rows:
            table_row = "|"

            for index, value in enumerate(row):
                table_row += " " + str(value).ljust(column_widths[index]) + " |"

            print(table_row)

        print(separator)

    # ---------------- ID GENERATION ----------------

    def generate_book_id(self):
        if not self.books:
            return "B001"

        max_number = 0

        for book in self.books:
            book_id = book["Book ID"]

            if book_id.startswith("B") and book_id[1:].isdigit():
                max_number = max(max_number, int(book_id[1:]))

        return f"B{max_number + 1:03d}"

    def generate_transaction_id(self):
        if not self.history:
            return "T001"

        max_number = 0

        for record in self.history:
            transaction_id = record["Transaction ID"]

            if transaction_id.startswith("T") and transaction_id[1:].isdigit():
                max_number = max(max_number, int(transaction_id[1:]))

        return f"T{max_number + 1:03d}"

    # ---------------- BOOK HELPERS ----------------

    def update_book_status(self, book):
        if book["Status"] == "Unavailable":
            return

        if book["Available Copies"] > 0:
            book["Status"] = "Available"
        else:
            book["Status"] = "Borrowed"

    def find_book_by_id(self, book_id):
        for book in self.books:
            if book["Book ID"].lower() == book_id.lower().strip():
                return book

        return None

    def is_duplicate_book(self, title, author, category, ignore_book_id=None):
        for book in self.books:
            if ignore_book_id and book["Book ID"] == ignore_book_id:
                continue

            if (
                book["Title"].lower() == title.lower()
                and book["Author"].lower() == author.lower()
                and book["Category"].lower() == category.lower()
            ):
                return book

        return None

    def calculate_fine(self, due_date_text, fine_paid):
        try:
            due_date = datetime.strptime(due_date_text, DATE_FORMAT)
        except ValueError:
            return 0, 0

        today = datetime.now()

        if today <= due_date:
            return 0, 0

        days_late = (today - due_date).days
        fine = days_late * self.fine_per_day

        if fine_paid == "True":
            return days_late, 0

        return days_late, fine

    def add_history(self, borrower, action, return_date="", fine=0):
        self.history.append({
            "Transaction ID": self.generate_transaction_id(),
            "Borrower": borrower["Borrower"],
            "Book ID": borrower["Book ID"],
            "Title": borrower["Title"],
            "Author": borrower["Author"],
            "Action": action,
            "Borrow Date": borrower["Borrow Date"],
            "Due Date": borrower["Due Date"],
            "Return Date": return_date,
            "Fine": fine
        })

        self.save_history()

    # ---------------- ADMIN BOOK FEATURES ----------------

    def add_book(self):
        title = self.input_non_empty("Book Title: ")
        author = self.input_non_empty("Author: ")
        category = self.input_non_empty("Category: ")
        copies = self.input_positive_int("Total Copies: ")

        duplicate = self.is_duplicate_book(title, author, category)

        if duplicate:
            duplicate["Total Copies"] += copies
            duplicate["Available Copies"] += copies
            self.update_book_status(duplicate)
            self.save_books()
            print("Book already exists. Copies updated.")
            return

        book = {
            "Book ID": self.generate_book_id(),
            "Title": title,
            "Author": author,
            "Category": category,
            "Total Copies": copies,
            "Available Copies": copies,
            "Status": "Available"
        }

        self.books.append(book)
        self.save_books()

        print(f"Book added successfully. Book ID: {book['Book ID']}")

    def update_book(self):
        book_id = input("Enter Book ID to update: ").strip()
        book = self.find_book_by_id(book_id)

        if not book:
            print("Book not found.")
            return

        print("\nLeave input empty to keep old value.")

        new_title = input(f"New Title ({book['Title']}): ").strip()
        new_author = input(f"New Author ({book['Author']}): ").strip()
        new_category = input(f"New Category ({book['Category']}): ").strip()

        title = self.format_string(new_title) if new_title else book["Title"]
        author = self.format_string(new_author) if new_author else book["Author"]
        category = self.format_string(new_category) if new_category else book["Category"]

        duplicate = self.is_duplicate_book(
            title, author, category, ignore_book_id=book["Book ID"]
        )

        if duplicate:
            print("Another book with the same title, author, and category already exists.")
            return

        while True:
            total_input = input(f"New Total Copies ({book['Total Copies']}): ").strip()

            if not total_input:
                total_copies = book["Total Copies"]
                break

            try:
                total_copies = int(total_input)

                if total_copies >= 0:
                    break

                print("Copies cannot be negative.")

            except ValueError:
                print("Enter a valid number.")

        borrowed_count = book["Total Copies"] - book["Available Copies"]

        if total_copies < borrowed_count:
            print(f"Cannot set total copies below currently borrowed copies ({borrowed_count}).")
            return

        print("Status options: Available, Unavailable")
        status_input = input(f"New Status ({book['Status']}): ").strip()

        if status_input:
            status_input = self.format_string(status_input)

            if status_input not in ["Available", "Unavailable"]:
                print("Invalid status.")
                return

        book["Title"] = title
        book["Author"] = author
        book["Category"] = category

        for borrower in self.borrowers:
            if borrower["Book ID"].lower() == book["Book ID"].lower():
                borrower["Title"] = title
                borrower["Author"] = author

        self.save_borrowers()
        book["Available Copies"] = total_copies - borrowed_count
        book["Total Copies"] = total_copies

        if status_input:
            book["Status"] = status_input
        else:
            self.update_book_status(book)

        self.save_books()
        print("Book updated successfully.")

    def delete_book(self):
        book_id = input("Enter Book ID to delete: ").strip()
        book = self.find_book_by_id(book_id)

        if not book:
            print("Book not found.")
            return

        for borrower in self.borrowers:
            if borrower["Book ID"].lower() == book_id.lower():
                print("Cannot delete this book because it is currently borrowed.")
                return

        confirm = input(f"Delete '{book['Title']}'? (yes/no): ").strip().lower()

        if confirm in ["yes", "y"]:
            self.books.remove(book)
            self.save_books()
            print("Book deleted successfully.")
        else:
            print("Deletion cancelled.")

    # ---------------- DISPLAY, SEARCH, FILTER ----------------

    def display_books(self):
        if not self.books:
            print("No books available.")
            return

        headers = [
            "Book ID", "Title", "Author", "Category",
            "Total Copies", "Available Copies", "Status"
        ]

        rows = []

        for book in sorted(self.books, key=lambda b: b["Title"].lower()):
            self.update_book_status(book)

            rows.append([
                book["Book ID"],
                book["Title"],
                book["Author"],
                book["Category"],
                book["Total Copies"],
                book["Available Copies"],
                book["Status"]
            ])

        self.print_table(headers, rows)
        self.save_books()

    def search_books(self):
        print("\nSearch by:")
        print("1. Title")
        print("2. Author")
        print("3. Keyword")
        print("4. Category")
        print("5. Book ID")

        choice = input("Enter choice: ").strip()

        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid search choice.")
            return

        keyword = input("Enter search text: ").strip().lower()

        if not keyword:
            print("Search text cannot be empty.")
            return

        results = []

        for book in self.books:
            if choice == "1" and keyword in book["Title"].lower():
                results.append(book)
            elif choice == "2" and keyword in book["Author"].lower():
                results.append(book)
            elif choice == "3" and (
                keyword in book["Title"].lower()
                or keyword in book["Author"].lower()
                or keyword in book["Category"].lower()
            ):
                results.append(book)
            elif choice == "4" and keyword in book["Category"].lower():
                results.append(book)
            elif choice == "5" and keyword == book["Book ID"].lower():
                results.append(book)

        if not results:
            print("No matching books found.")
            return

        self.print_book_filter_results(results)

    def filter_books(self):
        print("\nFilter options:")
        print("1. Available books")
        print("2. Borrowed books")
        print("3. Overdue books")
        print("4. Unavailable books")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            results = [
                book for book in self.books
                if book["Available Copies"] > 0 and book["Status"] == "Available"
            ]
            self.print_book_filter_results(results)

        elif choice == "2":
            results = [
                book for book in self.books
                if book["Available Copies"] < book["Total Copies"]
            ]
            self.print_book_filter_results(results)

        elif choice == "3":
            self.overdue_report()

        elif choice == "4":
            results = [
                book for book in self.books
                if book["Status"] == "Unavailable"
            ]
            self.print_book_filter_results(results)

        else:
            print("Invalid filter choice.")

    def print_book_filter_results(self, results):
        if not results:
            print("No books found.")
            return

        headers = [
            "Book ID", "Title", "Author", "Category",
            "Total Copies", "Available Copies", "Status"
        ]

        rows = []

        for book in results:
            rows.append([
                book["Book ID"],
                book["Title"],
                book["Author"],
                book["Category"],
                book["Total Copies"],
                book["Available Copies"],
                book["Status"]
            ])

        self.print_table(headers, rows)

    # ---------------- BORROW AND RETURN ----------------

    def borrow_book(self):
        book_id = input("Enter Book ID: ").strip()
        book = self.find_book_by_id(book_id)

        if not book:
            print("Book not found.")
            return

        self.update_book_status(book)

        if book["Status"] == "Unavailable":
            print("This book is currently unavailable.")
            return

        if book["Available Copies"] <= 0:
            print("No copies available.")
            return

        borrower_name = self.input_non_empty("Borrower Name: ")

        borrowed_by_user = [
            borrower for borrower in self.borrowers
            if borrower["Borrower"].lower() == borrower_name.lower()
        ]

        if len(borrowed_by_user) >= 3:
            print("Borrowing limit reached. Maximum 3 books allowed.")
            return

        for borrower in self.borrowers:
            if (
                borrower["Borrower"].lower() == borrower_name.lower()
                and borrower["Book ID"].lower() == book_id.lower()
            ):
                print("This borrower has already borrowed this book.")
                return

        borrow_date = datetime.now().strftime(DATE_FORMAT)
        due_date = (datetime.now() + timedelta(days=self.borrow_days)).strftime(DATE_FORMAT)

        borrower = {
            "Borrower": borrower_name,
            "Book ID": book["Book ID"],
            "Title": book["Title"],
            "Author": book["Author"],
            "Borrow Date": borrow_date,
            "Due Date": due_date,
            "Fine Paid": "False",
            "Fine Amount": "0"
        }

        book["Available Copies"] -= 1
        self.update_book_status(book)

        self.borrowers.append(borrower)

        self.save_books()
        self.save_borrowers()
        self.add_history(borrower, "Borrow", "", 0)

        print("Book borrowed successfully.")
        print(f"Due Date: {due_date}")

    def return_book(self):
        borrower_name = self.input_non_empty("Borrower Name: ")
        book_id = input("Book ID: ").strip()

        for borrower in self.borrowers:
            if (
                borrower["Borrower"].lower() == borrower_name.lower()
                and borrower["Book ID"].lower() == book_id.lower()
            ):
                book = self.find_book_by_id(book_id)

                if not book:
                    print("Book record missing from books.csv.")
                    return

                days_late, fine = self.calculate_fine(
                    borrower["Due Date"], borrower["Fine Paid"]
                )

                paid_fine_amount = int(borrower.get("Fine Amount", "0") or 0)

                if borrower["Fine Paid"] == "True":
                    history_fine = paid_fine_amount
                else:
                    history_fine = fine

                if fine > 0 and borrower["Fine Paid"] != "True":
                    print(f"Book is overdue by {days_late} days.")
                    print(f"Pending fine: {fine} units")
                    print("Please pay the fine before returning the book.")
                    return

                return_date = datetime.now().strftime(DATE_FORMAT)

                self.borrowers.remove(borrower)
                book["Available Copies"] += 1
                self.update_book_status(book)

                self.save_books()
                self.save_borrowers()
                self.add_history(borrower, "Return", return_date, history_fine)

                print("Book returned successfully.")
                return

        print("Borrow record not found.")

    def pay_fine(self):
        borrower_name = self.input_non_empty("Borrower Name: ")
        found = False

        for borrower in self.borrowers:
            if borrower["Borrower"].lower() == borrower_name.lower():
                found = True

                days_late, fine = self.calculate_fine(
                    borrower["Due Date"], borrower["Fine Paid"]
                )

                if borrower["Fine Paid"] == "True":
                    fine = int(borrower.get("Fine Amount", "0") or 0)

                headers = ["Borrower", "Book ID", "Title", "Due Date", "Days Late", "Fine"]

                rows = [[
                    borrower["Borrower"],
                    borrower["Book ID"],
                    borrower["Title"],
                    borrower["Due Date"],
                    days_late,
                    f"{fine} units"
                ]]

                self.print_table(headers, rows)

                if fine > 0:
                    confirm = input("Pay now? (yes/no): ").strip().lower()

                    if confirm in ["yes", "y"]:
                        borrower["Fine Paid"] = "True"
                        borrower["Fine Amount"] = str(fine)
                        print("Fine paid successfully.")
                    else:
                        print("Fine not paid.")

                elif borrower["Fine Paid"] == "True":
                    print("Fine already paid.")
                else:
                    print("No fine due.")

        if found:
            self.save_borrowers()
        else:
            print("Borrower not found.")

    # ---------------- REPORTS ----------------

    def display_borrowers(self):
        if not self.borrowers:
            print("No books borrowed currently.")
            return

        headers = [
            "Borrower", "Book ID", "Title", "Author",
            "Borrow Date", "Due Date", "Fine Paid", "Status"
        ]

        rows = []

        for borrower in sorted(self.borrowers, key=lambda b: b["Borrower"].lower()):
            days_late, fine = self.calculate_fine(
                borrower["Due Date"], borrower["Fine Paid"]
            )

            if fine > 0:
                status = f"Overdue By {days_late} Days, Fine: {fine}"
            else:
                status = "On Time"

            rows.append([
                borrower["Borrower"],
                borrower["Book ID"],
                borrower["Title"],
                borrower["Author"],
                borrower["Borrow Date"],
                borrower["Due Date"],
                borrower["Fine Paid"],
                status
            ])

        self.print_table(headers, rows)

    def view_my_books(self):
        borrower_name = self.input_non_empty("Enter your name: ")

        records = [
            borrower for borrower in self.borrowers
            if borrower["Borrower"].lower() == borrower_name.lower()
        ]

        if not records:
            print("No borrowed books found for this name.")
            return

        headers = [
            "Book ID", "Title", "Author",
            "Borrow Date", "Due Date", "Status", "Fine"
        ]

        rows = []

        for borrower in records:
            days_late, fine = self.calculate_fine(
                borrower["Due Date"], borrower["Fine Paid"]
            )

            if borrower["Fine Paid"] == "True":
                fine = int(borrower.get("Fine Amount", "0") or 0)

            if fine > 0:
                status = f"Overdue By {days_late} Days"
            else:
                status = "On Time"

            rows.append([
                borrower["Book ID"],
                borrower["Title"],
                borrower["Author"],
                borrower["Borrow Date"],
                borrower["Due Date"],
                status,
                f"{fine} units"
            ])

        self.print_table(headers, rows)

    def view_history(self):
        if not self.history:
            print("No history available.")
            return

        headers = [
            "Transaction ID", "Borrower", "Book ID", "Title", "Author",
            "Action", "Borrow Date", "Due Date", "Return Date", "Fine"
        ]

        rows = []

        for record in self.history:
            rows.append([
                record["Transaction ID"],
                record["Borrower"],
                record["Book ID"],
                record["Title"],
                record["Author"],
                record["Action"],
                record["Borrow Date"],
                record["Due Date"],
                record["Return Date"],
                record["Fine"]
            ])

        self.print_table(headers, rows)

    def overdue_report(self):
        total_fine = 0
        rows = []

        headers = [
            "Borrower", "Book ID", "Title",
            "Due Date", "Days Late", "Fine Pending"
        ]

        for borrower in self.borrowers:
            days_late, fine = self.calculate_fine(
                borrower["Due Date"], borrower["Fine Paid"]
            )

            if fine > 0:
                total_fine += fine

                rows.append([
                    borrower["Borrower"],
                    borrower["Book ID"],
                    borrower["Title"],
                    borrower["Due Date"],
                    days_late,
                    f"{fine} units"
                ])

        if not rows:
            print("No overdue books.")
        else:
            self.print_table(headers, rows)

        print(f"\nTotal Fine Pending: {total_fine} units")

    def dashboard(self):
        total_books = len(self.books)
        total_copies = sum(book["Total Copies"] for book in self.books)
        available_copies = sum(book["Available Copies"] for book in self.books)
        borrowed_copies = len(self.borrowers)

        overdue_items = 0
        pending_fines = 0

        for borrower in self.borrowers:
            days_late, fine = self.calculate_fine(
                borrower["Due Date"], borrower["Fine Paid"]
            )

            if fine > 0:
                overdue_items += 1
                pending_fines += fine

        headers = ["Metric", "Value"]

        rows = [
            ["Total Book Titles", total_books],
            ["Total Copies", total_copies],
            ["Available Copies", available_copies],
            ["Borrowed Copies", borrowed_copies],
            ["Overdue Items", overdue_items],
            ["Pending Fines", f"{pending_fines} units"]
        ]

        self.print_table(headers, rows)

    # ---------------- LOGIN AND MENUS ----------------

    def admin_login(self, max_attempts=3):
        try:
            with open(ADMIN_FILE, "r", newline="") as file:
                reader = csv.DictReader(file)
                admin = next(reader)

        except (FileNotFoundError, StopIteration):
            print("Admin file missing or empty.")
            return False

        for attempt in range(max_attempts):
            username = input("Admin Username: ").strip()
            password = getpass.getpass("Admin Password: ").strip()

            if username == admin["Username"] and password == admin["Password"]:
                print("Admin login successful.")
                return True

            print("Invalid username or password.")

        print("Too many failed attempts. Access denied.")
        return False

    def admin_menu(self):
        while True:
            print("\n--- ADMIN MENU ---")
            print("1. Add Book")
            print("2. Update Book")
            print("3. Delete Book")
            print("4. Display Books")
            print("5. Search Books")
            print("6. Filter Books")
            print("7. Display Borrowers")
            print("8. Issue History")
            print("9. Overdue Report")
            print("10. Dashboard")
            print("11. Logout")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.update_book()
            elif choice == "3":
                self.delete_book()
            elif choice == "4":
                self.display_books()
            elif choice == "5":
                self.search_books()
            elif choice == "6":
                self.filter_books()
            elif choice == "7":
                self.display_borrowers()
            elif choice == "8":
                self.view_history()
            elif choice == "9":
                self.overdue_report()
            elif choice == "10":
                self.dashboard()
            elif choice == "11":
                print("Logging out.")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 11.")

    def user_menu(self):
        while True:
            print("\n--- USER MENU ---")
            print("1. Search Books")
            print("2. Filter Books")
            print("3. Display Books")
            print("4. Borrow Book")
            print("5. Return Book")
            print("6. Pay Fine")
            print("7. View My Borrowed Books")
            print("8. Logout")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.search_books()
            elif choice == "2":
                self.filter_books()
            elif choice == "3":
                self.display_books()
            elif choice == "4":
                self.borrow_book()
            elif choice == "5":
                self.return_book()
            elif choice == "6":
                self.pay_fine()
            elif choice == "7":
                self.view_my_books()
            elif choice == "8":
                print("Logging out.")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 8.")

    def main_menu(self):
        while True:
            print("\n--- LIBRARY MANAGEMENT SYSTEM ---")
            print("1. Admin")
            print("2. User")
            print("3. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                if self.admin_login():
                    self.admin_menu()
            elif choice == "2":
                self.user_menu()
            elif choice == "3":
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Enter 1, 2, or 3.")


library = Library()
library.main_menu()
