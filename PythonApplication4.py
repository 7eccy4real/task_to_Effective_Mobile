# -*- coding: cp1251 -*-
import json
import os

# Модель книги
class Book:
    def __init__(self, book_id, title, author, year, status="в наличии"):
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


# Управление библиотекой
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
        print(f"Книга '{title}' успешно добавлена!")

    def delete_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                print(f"Книга с ID {book_id} удалена.")
                return
        print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, query):
        results = [
            book for book in self.books
            if query.lower() in book.title.lower() or
               query.lower() in book.author.lower() or
               query.lower() in str(book.year)
        ]
        if results:
            print("Найденные книги:")
            for book in results:
                print(book.to_dict())
        else:
            print("Книги по запросу не найдены.")

    def list_books(self):
        if not self.books:
            print("Библиотека пуста.")
            return
        print("Список всех книг:")
        for book in self.books:
            print(book.to_dict())

    def update_status(self, book_id, new_status):
        for book in self.books:
            if book.id == book_id:
                if new_status in ["в наличии", "выдана"]:
                    book.status = new_status
                    print(f"Статус книги с ID {book_id} обновлен на '{new_status}'.")
                    return
                else:
                    print("Неверный статус. Используйте 'в наличии' или 'выдана'.")
                    return
        print(f"Книга с ID {book_id} не найдена.")


# Основной интерфейс программы
def main():
    library = LibraryManager("library.json")

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            title = input("Введите название книги: ").strip()
            author = input("Введите автора книги: ").strip()
            year = input("Введите год издания: ").strip()
            if year.isdigit():
                library.add_book(title, author, int(year))
            else:
                print("Год издания должен быть числом.")

        elif choice == "2":
            book_id = input("Введите ID книги для удаления: ").strip()
            if book_id.isdigit():
                library.delete_book(int(book_id))
            else:
                print("ID должен быть числом.")

        elif choice == "3":
            query = input("Введите запрос для поиска (название, автор или год): ").strip()
            library.search_books(query)

        elif choice == "4":
            library.list_books()

        elif choice == "5":
            book_id = input("Введите ID книги для изменения статуса: ").strip()
            if book_id.isdigit():
                new_status = input("Введите новый статус ('в наличии' или 'выдана'): ").strip()
                library.update_status(int(book_id), new_status)
            else:
                print("ID должен быть числом.")

        elif choice == "0":
            library.save_books()
            print("Изменения сохранены. До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
