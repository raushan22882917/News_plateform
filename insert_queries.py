import uuid
from datetime import datetime

def insert_news_article_data(cursor, connection, title, subtitle, context, image, image_alt, source, category, article_url):
    """
    Inserts a single record into the NewsArticle table in PostgreSQL.

    Parameters:
        cursor: The database cursor for executing queries.
        connection: The database connection for committing transactions.
        title (str): Title of the article.
        subtitle (str): Subtitle of the article.
        context (str): Content of the article.
        image (str): URL of the article's image.
        image_alt (str): Alternative text for the image.
        source (str): URL of the article's source.
        category (str): Category of the article.
        article_url (str): URL of the article.
    """
    try:
        # SQL query for inserting data
        insert_query = """
        INSERT INTO news_newsarticle
        (id, title, subtitle, context, date, image, image_alt, source, category, article_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        # Generate a new UUID for the id field
        article_id = str(uuid.uuid4())

        # Current date and time for the date field
        current_date = datetime.now()

        # Data to be inserted
        article_data = (
            article_id,       # id (UUID)
            title,            # title (TextField)
            subtitle,         # subtitle (TextField)
            context,          # context (TextField)
            current_date,     # date (DateTime)
            image,            # image (URLField)
            image_alt,        # image_alt (CharField, max_length=7000)
            source,           # source (URLField)
            category[:6999],  # category (CharField, max_length=6999)
            article_url       # article_url (URLField)
        )

        cursor.execute(insert_query, article_data)

        connection.commit()
        print(f"New article inserted successfully with ID: {article_id}")

    except Exception as e:
        # Roll back the transaction if an error occurs
        connection.rollback()
        print(f"Error inserting article data: {e}")


def article_exists(cursor, article_url):
    """
    Checks if an article with the given article_url exists in the NewsArticle table.

    Parameters:
        cursor: The database cursor for executing queries.
        article_url (str): URL of the article to check.

    Returns:
        bool: True if the article exists, False otherwise.
    """
    try:
        # Query to check if the article_url exists
        check_query = "SELECT EXISTS (SELECT 1 FROM news_newsarticle WHERE article_url = %s);"
        
        # Execute the query
        cursor.execute(check_query, (article_url,))
        
        # Fetch the result
        exists = cursor.fetchone()[0]
        
        return exists

    except Exception as e:
        print(f"Error checking if article exists: {e}")
        return False
