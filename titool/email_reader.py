import imaplib
import email
from email.header import decode_header
from typing import List
import re
from bs4 import BeautifulSoup


def read_email(mail_username: str, mail_password: str, emails_limit=2) -> List[str]:
    """
    Returns the HTML content of the `emails_limit` latest emails.
    """
    bodies = []

    # Create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # Authenticate
    imap.login(mail_username, mail_password)

    # Select the main mailbox
    status, message_count = imap.select("INBOX")
    # Cast into an integer to make a for loop on it
    message_count = int(message_count[0])

    # From the top to the bottom since the latest email has the highest ID
    for i in range(message_count, message_count-emails_limit, -1):
        # Fetch the email by ID using the standard format of RFC 822
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                # Get the sender
                sender, encoding = decode_header(msg["From"])[0]
                if isinstance(sender, bytes):
                    # Decode to a string
                    sender = sender.decode(encoding)
                matched = re.search("Alertes\sGoogle\sScholar", sender)
                if matched:
                    # Get the email body
                    body = msg.get_payload(decode=True).decode()
                    bodies.append(body)
    imap.close()
    imap.logout()
    return bodies


class EmailItem:
    def __init__(self, url: str, title: str, author: str):
        self.url = url
        self.title = title
        self.author = author


# def test_scrape_email(bodies: List[str]):
#     for body in bodies:
#         email_items = scrape_email(body)
#         for item in email_items:
#             print(item.title)
#             print(item.url)


def scrape_email(body: str) -> List[EmailItem]:
    """
    Takes the HTML body of an email and returns a list of articles
    """
    articles = []
    # BeautifulSoup object is created, HTML data is passed to the constructor
    # The second option specifies the parser
    soup = BeautifulSoup(body, 'html.parser')
    titles = soup.find_all('h3')
    for title in titles:
        author = title.findNext('div').get_text()
        link = title.find('a')
        title_text = title.get_text()
        if title_text is None or link is None:
            continue
        articles.append(EmailItem(link['href'], title_text, author))
    return articles
