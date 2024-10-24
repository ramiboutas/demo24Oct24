from django.template.loader import render_to_string
from django.utils import timezone
from huey import crontab
from huey.contrib import djhuey as huey

from .models import Book, BookInstance, BookUserSubsription


@huey.db_periodic_task(crontab(hour="8", minute="0"))
def inform_book_subscriber_about_new_book_instances():
    """
    # 4. Email Benachrichtigung an Endkund:innen, wenn ein Buch wieder zur Ausleihe zur Verfügung steht.
    """
    available_books = Book.objects.filter(bookinstance__status="a").distinct()

    subscribers = BookUserSubsription.objects.filter(informed=False, book__in=available_books)

    for subscriber in subscribers:
        try:
            subscriber.send_email()
        except Exception:  # TODO: improve!
            continue

    subscribers.update(informed=True)


from ..base.whatsapp import send_whatsapp_message


@huey.db_periodic_task(crontab(hour="8", minute="30"))
def return_the_books_please():
    """
    5. Reminder: Whatsapp-Versand an Kund:in 2 Tage nach Ablauf der Ausleihdauer.
    """

    two_days_ago = timezone.now() + timezone.timedelta(days=2)

    qs = BookInstance.objects.filter(due_back__lte=two_days_ago, status="o")

    for book_instance in qs:
        if book_instance.borrower.cleaned_whatsapp_number == "":
            continue
        message = render_to_string("whatsapp/book_instance_due.txt", {"book_instance": book_instance})

        try:
            send_whatsapp_message(book_instance.borrower, message)
        except Exception:  # TODO: improve
            continue
