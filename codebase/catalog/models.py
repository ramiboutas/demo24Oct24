import uuid
from datetime import date

from auto_prefetch import ForeignKey, Model
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse

User = get_user_model()


class Genre(Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""

    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Language(Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""

    name = models.CharField(max_length=200, help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Author(Model):
    """Model representing an author."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("died", null=True, blank=True)

    class Meta(Model.Meta):
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.last_name}, {self.first_name}"


class Book(Model):
    """Model representing a book (but not a specific copy of a book)."""

    title = models.CharField(max_length=200)
    author = ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        unique=True,
        help_text='13 Character <a target="_blank" href="https://www.isbn-international.org/content/what-isbn' '">ISBN number</a>',
    )
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    language = ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)

    class Meta(Model.Meta):
        ordering = ["title", "author"]

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ", ".join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = "Genre"

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse("book-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class BookInstance(Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    LOAN_STATUS = (
        ("d", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    borrower = ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="d", help_text="Book availability")

    @property
    def is_overdue(self):
        return self.due_back and date.today() > self.due_back

    class Meta(Model.Meta):
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id} ({self.book.title})"


class BookUserSubsription(Model):
    """Model used to inform to user that a book instance or more are available for loaing"""

    # TODO: create the  views & urls correspoding to this model
    book = ForeignKey(Book, on_delete=models.CASCADE)
    user = ForeignKey(User, on_delete=models.CASCADE)
    informed = models.BooleanField(default=False)

    def send_email(self):
        if self.informed or self.user.email in ["", None]:
            return
        email_content = render_to_string("emails/book_available.txt", {"book": self.book, "user": self.user})
        send_mail(
            subject=f"{settings.WEBSITE_NAME} | {Book.title}",
            message=email_content,
            from_email=None,  # use default sender
            recipient_list=[self.user.email],
        )
