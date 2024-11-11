import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# to store all books -> instead of database I use in memory database


class Book:
    record_number = 0

    def __init__(self, title, author, price, count):
        self.title = title
        self.author = author
        self.price = int(price)
        self.count = int(count)
        self.sold = 0
        self.id = Book.record_number + 1
        Book.record_number += 1

    def add(self, quantity):
        self.count += quantity

    def sell(self):
        if self.count == 0:
            messagebox.showinfo("توجه", "کتاب مورد نظر موجود نمی‌باشد")
            return
        self.count -= 1
        self.sold += 1


class SalesTracker:
    def __init__(self):
        self.sales = []

    def record_sale(self, book):
        if book.count >= 1:
            book.sell()
            self.sales.append((book.title, book.price))
        else:
            raise ValueError("موجودی کافی نیست.")

    def total_sales(self):
        total_books = len(self.sales)
        total_income = sum(sale[1] for sale in self.sales)
        return total_books, total_income


# functions to handle tkinter app


# data to test application


class Gui:

    def add_new(self, title, author, price, count):
        book = Book(title=title, author=author, price=price, count=count)
        self.all_books[book.id] = book
        self.show_records()
        messagebox.showinfo("توجه", "رکورد ذخیره شد")
        self.title.set("")
        self.author.set("")
        self.price.set("")
        self.count.set("")

    def search_product(self, title, author):
        self.table.delete(*self.table.get_children())
        finded_records = []
        if not title and not author:
            finded_records = self.all_books.values()
        else:
            for item in self.all_books.values():
                title = title if title else "_"
                author = author if author else "_"
                if title in item.title or author in item.author:
                    finded_records.append(item)

        for item in finded_records:
            self.table.insert(
                "",
                "end",
                values=(
                    item.id,
                    item.title,
                    item.author,
                    item.price,
                    item.count,
                ),
            )

    def delete_record(self):
        if not self.table.selection():
            messagebox.showwarning("توجه", "رکوردی برای حذف انتخاب نشده است")
        else:
            result = messagebox.askquestion(
                "هشدار", "آیا رکورد حذف شود؟", icon="warning"
            )
            if result == "yes":
                row = self.table.focus()
                row_contents = self.table.item(row)
                book_id = row_contents["values"][0]

                del self.all_books[book_id]
                self.table.delete(row)

    def buy_book(self):

        row = self.table.focus()
        row_contents = self.table.item(row)
        book_id = row_contents["values"][0]

        self.all_books[book_id].sell()
        self.show_records()
        self.sale_report.record_sale(self.all_books[book_id])
        total_books, total_income = self.sale_report.total_sales()
        self.sell_count_value.config(text=f"{total_books}")
        self.sell_amount_value.config(text=f"{total_income}")

    def fixture(self):
        book = Book(title="صد سال تنهایی", author="گارسیا", price=50, count=10)
        self.all_books[book.id] = book
        book = Book(title="جنگ و صلح", author="تولستوی", price=100, count=5)
        self.all_books[book.id] = book
        book = Book(title="بینوایان", author="هوگو", price=70, count=2)
        self.all_books[book.id] = book

    def show_records(self):
        self.table.delete(*self.table.get_children())

        for item in self.all_books.values():
            self.table.insert(
                "",
                "end",
                values=(
                    item.id,
                    item.title,
                    item.author,
                    item.price,
                    item.count,
                ),
            )

    def __init__(self):
        self.root = tk.Tk()
        self.root.title = "Book Store"
        self.root.geometry("800x400")
        self.all_books = {}
        self.sale_report = SalesTracker()
        self.fixture()

        # Entry
        self.title = tk.StringVar()
        self.author = tk.StringVar()
        self.price = tk.StringVar()
        self.count = tk.StringVar()

        frame0 = tk.Frame(self.root, width=800, height=150, bg="pink").pack(
            side=tk.TOP, fill=tk.X
        )
        frame1 = tk.Frame(self.root, width=800)
        frame1.pack(side=tk.LEFT, fill=tk.Y)

        title_lable = tk.Label(self.root, text="عنوان").place(x=100, y=10)
        buy_price_lable = tk.Label(self.root, text="نویسنده").place(x=375, y=10)
        sell_price_lable = tk.Label(self.root, text="قیمت").place(x=100, y=50)
        count_lable = tk.Label(self.root, text="موجودی ").place(x=370, y=50)

        sell_count_lable = tk.Label(self.root, text="تعداد کتاب‌های فروخته شده").place(
            x=600, y=50
        )
        sell_amount_lable = tk.Label(self.root, text="میزان درآمد ").place(x=600, y=20)
        self.sell_count_value = tk.Label(self.root, text="0")
        self.sell_count_value.place(x=750, y=50)
        self.sell_amount_value = tk.Label(self.root, text="0")
        self.sell_amount_value.place(x=700, y=20)

        tk.Entry(frame0, textvariable=self.title).place(x=150, y=10)
        tk.Entry(frame0, textvariable=self.author).place(x=435, y=10)
        tk.Entry(frame0, textvariable=self.price).place(x=150, y=50)
        tk.Entry(frame0, textvariable=self.count).place(x=435, y=50)

        # self.self.table
        self.table = ttk.Treeview(
            frame1,
            columns=("ID", "title", "author", "price", "count"),
            show="headings",
        )
        # Buttons

        tk.Button(
            frame0,
            text="اضافه کردن",
            command=lambda: self.add_new(
                self.title.get(),
                self.author.get(),
                self.price.get(),
                self.count.get(),
            ),
        ).place(x=50, y=100, width=120)
        tk.Button(
            frame0,
            text="جست و جو کردن",
            command=lambda: self.search_product(self.title.get(), self.author.get()),
        ).place(x=240, y=100, width=120)
        tk.Button(frame0, text="حذف کردن", command=self.delete_record).place(
            x=420, y=100, width=120
        )
        tk.Button(frame0, text="خرید", command=self.buy_book).place(
            x=620, y=100, width=120
        )

        frame1 = tk.Frame(self.root, width=600)
        frame1.pack(side=tk.LEFT, fill=tk.Y)

        self.table.heading("ID", text="کد")
        self.table.heading("title", text="عنوان")
        self.table.heading("author", text="نویسنده")
        self.table.heading("price", text="قیمت")
        self.table.heading("count", text="موجودی")

        self.table.column("#0", width=0)
        self.table.column("#1", width=100)
        self.table.column("#2", width=250)
        self.table.column("#3", width=110)
        self.table.column("#4", width=110)
        self.table.column("#0", width=110)

        self.table.pack()
        self.show_records()
        self.root.mainloop()


# def main():
#     global sell_amount_value, sell_count_value


class LoginGui:
    def __init__(self, root):
        self.root = root
        self.root.title = "Login"

        # پنجره لاگین

        self.root.geometry("300x150")

        tk.Label(self.root, text="نام کاربری:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="رمز عبور:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self.root, text="ورود", command=self.authenticate)
        login_button.pack(pady=10)

    def authenticate(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if user == "admin" and pwd == "password":
            messagebox.showinfo("Login", "ورود موفقیت‌آمیز!")
            self.root.destroy()
            Gui()
        else:
            messagebox.showerror("Login", "نام کاربری یا رمز عبور اشتباه است")


if __name__ == "__main__":
    root = tk.Tk()

    login = LoginGui(root)

    root.mainloop()
