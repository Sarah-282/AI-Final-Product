class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    # Generated with an AI coding assistant
    def issue_book(self):
        if not self.available:
            return f'"{self.title}" is already issued.'
        self.available = False
        return f'"{self.title}" has been issued.'


books = [
    Book("1984", "George Orwell"),
    Book("Pride and Prejudice", "Jane Austen"),
    Book("The Hobbit", "J.R.R. Tolkien")
]

for book in books:
    status = "Available" if book.available else "Issued"
    print(f"{book.title} by {book.author} - {status}")

print(books[0].issue_book())
print(books[0].issue_book())  # Prevents issuing it again

# Change made to the AI-generated code:
# Added a check for availability so an already-issued book cannot be issued again.
