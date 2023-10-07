try:
    from faker import Faker
    import uuid
    import datetime
    import json
    import random
    from dateutil.relativedelta import relativedelta
    from datetime import datetime

    from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
    from pynamodb.models import Model
    from pynamodb.attributes import *
    from dotenv import load_dotenv
    import os

    load_dotenv("../.env")
    from data import BOOKS_DATA

except Exception as e:
    pass


global TABLE_NAME
TABLE_NAME = f'{os.getenv("TABLE_NAME")}-lab-{os.getenv("LAB_NUMBER")}-team-{os.getenv("TEAM_NUMBER")}'


class AuthorsBooks(Model):
    class Meta:
        table_name = TABLE_NAME
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    author_name = UnicodeAttribute(null=True)

    book_title = UnicodeAttribute(null=True)
    book_published_data = UnicodeAttribute(null=True)
    isbn = UnicodeAttribute(null=True)
    total_pages = UnicodeAttribute(null=True)
    book_price = UnicodeAttribute(null=True)
    books_meta_data = MapAttribute(null=True)

    gs1pk = UnicodeAttribute(null=True)
    category = UnicodeAttribute(null=True)

    gs2pk = UnicodeAttribute(null=True)
    ttl = NumberAttribute(null=True)


class ViewIndex(GlobalSecondaryIndex):

    """
    This class represents a global secondary index
    """

    class Meta:
        index_name = "gs2pk-index"
        projection = AllProjection()
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")

    gs2pk = UnicodeAttribute(hash_key=True)


class CategoriesModel(Model):
    """
    A test model that uses a global secondary index
    """

    class Meta:
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
        table_name = TABLE_NAME

    pk = UnicodeAttribute(null=True)
    sk = UnicodeAttribute(null=True)
    author_name = UnicodeAttribute(null=True)

    book_title = UnicodeAttribute(null=True)
    book_published_data = UnicodeAttribute(null=True)
    isbn = UnicodeAttribute(null=True)
    total_pages = UnicodeAttribute(null=True)
    book_price = UnicodeAttribute(null=True)
    books_meta_data = MapAttribute(null=True)

    gs1pk = UnicodeAttribute(null=True)
    category = UnicodeAttribute(null=True)
    ttl = NumberAttribute(null=True)

    view_index = ViewIndex()
    gs2pk = UnicodeAttribute(hash_key=True)


def clean_table():
    for x in AuthorsBooks.scan():
        x.delete()


def get_current_timestamp():
    # current date and time
    ttl_time = datetime.now() + relativedelta(years=2)
    timestamp = datetime.timestamp(datetime.now() + relativedelta(years=1))
    return round(timestamp)


def load_data():

    clean_table()

    # BOOKS_DATA =  [ {
    #     "title": "Hello World!",
    #     "isbn": "1933988495",
    #     "pageCount": 432,
    #     "publishedDate": { "$date": "2009-03-01T00:00:00.000-0800" },
    #     "thumbnailUrl": "https://s3.amazonaws.com/AKIAJC5RLADLUMVRPFDQ.book-thumb-images/sande.jpg",
    #     "shortDescription": "Hello World! provides a gentle but thorough introduction to the world of computer programming.",
    #     "longDescription": "Your computer won't respond when you yell at it. Why not learn to talk to your computer in its own language  Whether you want to write games, start a business, or you're just curious, learning to program is a great place to start. Plus, programming is fun!    Hello World! provides a gentle but thorough introduction to the world of computer programming. It's written in language a 12-year-old can follow, but anyone who wants to learn how to program a computer can use it. Even adults. Written by Warren Sande and his son, Carter, and reviewed by professional educators, this book is kid-tested and parent-approved.    You don't need to know anything about programming to use the book. But you should know the basics of using a computer--e-mail, surfing the web, listening to music, and so forth. If you can start a program and save a file, you should have no trouble using this book.",
    #     "status": "PUBLISH",
    #     "authors": ["Warren D. Sande", "Carter Sande"],
    #     "categories": ["Programming", "Python"]
    # }]

    for c, items in enumerate(BOOKS_DATA):
        try:
            print(c)
            book_id = uuid.uuid4().__str__()

            for author in items.get("authors"):
                author_id = uuid.uuid4().__str__()

                AuthorsBooks(
                    pk=f"Author#{author_id}",
                    sk=f"Author#{author_id}",
                    author_name=author,
                    ttl=get_current_timestamp(),
                ).save()

                if items.get("categories") == []:
                    res = AuthorsBooks(
                        pk=f"Book#{book_id}",
                        sk=f"Book#{book_id}#Author#{author_id}",
                        book_title=items.get("title"),
                        book_published_data=items.get(
                            "publishedDate", {}).get("$date"),
                        book_price=random.randint(20, 300).__str__(),
                        isbn=items.get("isbn").__str__(),
                        total_pages=items.get("pageCount").__str__(),
                        author_name=author,
                        books_meta_data={
                            "thumbnailUrl": items.get("thumbnailUrl"),
                            "shortDescription": items.get("shortDescription"),
                            "longDescription": items.get("longDescription"),
                            "status": items.get("status"),
                        },
                        category="",
                        gs1pk=f"Author#{author_id}",
                        ttl=get_current_timestamp(),
                    ).save()

                else:
                    for category in items.get("categories"):
                        res = AuthorsBooks(
                            pk=f"Book#{book_id}",
                            sk=f"Book#{book_id}Author#{author_id}#Category#{category}",
                            book_title=items.get("title"),
                            book_published_data=items.get("publishedDate", {}).get(
                                "$date"
                            ),
                            book_price=random.randint(20, 300).__str__(),
                            isbn=items.get("isbn").__str__(),
                            total_pages=items.get("pageCount").__str__(),
                            author_name=author,
                            books_meta_data={
                                "thumbnailUrl": items.get("thumbnailUrl"),
                                "shortDescription": items.get("shortDescription"),
                                "longDescription": items.get("longDescription"),
                                "status": items.get("status"),
                            },
                            category=category,
                            gs1pk=f"Author#{author_id}",
                            gs2pk=category,
                            ttl=get_current_timestamp(),
                        ).save()
        except Exception as e:
            pass


def get_categories():

    for cat in CategoriesModel.view_index.scan():

        try:
            AuthorsBooks(pk=f"categoryList#", sk=str(cat.category)).save()
        except Exception as e:
            pass


if __name__ == "__main__":
    load_data()
    get_categories()
