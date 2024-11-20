# -*- coding: cp1251 -*-
import json
import os

# ������ �����
class Book:
    def __init__(self, book_id, title, author, year, status="� �������"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"]
        )


# ���������� �����������
class LibraryManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Book.from_dict(book) for book in data]
        return []

    def save_books(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        print(f"����� '{title}' ������� ���������!")

    def delete_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                print(f"����� � ID {book_id} �������.")
                return
        print(f"����� � ID {book_id} �� �������.")

    def search_books(self, query):
        results = [
            book for book in self.books
            if query.lower() in book.title.lower() or
               query.lower() in book.author.lower() or
               query.lower() in str(book.year)
        ]
        if results:
            print("��������� �����:")
            for book in results:
                print(book.to_dict())
        else:
            print("����� �� ������� �� �������.")

    def list_books(self):
        if not self.books:
            print("���������� �����.")
            return
        print("������ ���� ����:")
        for book in self.books:
            print(book.to_dict())

    def update_status(self, book_id, new_status):
        for book in self.books:
            if book.id == book_id:
                if new_status in ["� �������", "������"]:
                    book.status = new_status
                    print(f"������ ����� � ID {book_id} �������� �� '{new_status}'.")
                    return
                else:
                    print("�������� ������. ����������� '� �������' ��� '������'.")
                    return
        print(f"����� � ID {book_id} �� �������.")


# �������� ��������� ���������
def main():
    library = LibraryManager("library.json")

    while True:
        print("\n����:")
        print("1. �������� �����")
        print("2. ������� �����")
        print("3. ����� �����")
        print("4. �������� ��� �����")
        print("5. �������� ������ �����")
        print("0. �����")

        choice = input("�������� ��������: ").strip()

        if choice == "1":
            title = input("������� �������� �����: ").strip()
            author = input("������� ������ �����: ").strip()
            year = input("������� ��� �������: ").strip()
            if year.isdigit():
                library.add_book(title, author, int(year))
            else:
                print("��� ������� ������ ���� ������.")

        elif choice == "2":
            book_id = input("������� ID ����� ��� ��������: ").strip()
            if book_id.isdigit():
                library.delete_book(int(book_id))
            else:
                print("ID ������ ���� ������.")

        elif choice == "3":
            query = input("������� ������ ��� ������ (��������, ����� ��� ���): ").strip()
            library.search_books(query)

        elif choice == "4":
            library.list_books()

        elif choice == "5":
            book_id = input("������� ID ����� ��� ��������� �������: ").strip()
            if book_id.isdigit():
                new_status = input("������� ����� ������ ('� �������' ��� '������'): ").strip()
                library.update_status(int(book_id), new_status)
            else:
                print("ID ������ ���� ������.")

        elif choice == "0":
            library.save_books()
            print("��������� ���������. �� ��������!")
            break

        else:
            print("�������� �����. ���������� �����.")

if __name__ == "__main__":
    main()
