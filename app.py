from driver_initializer import initialize_driver
from geopolitical_news import scrape_geopolitical_articles
from database_config import get_curser
from insert_queries import insert_news_article_data
from thedailystar_news import scrape_daily_star_articles
from forreign_affairs_news import scrape_foreign_affairs_articles
from eurasians_news import scrape_eurasian_times_articles
from deplomat_news import scrape_diplomat_articles
from bbc_news import scrape_bbc_world_news


def scrape_all_sites(connection, cursor):

    # Initialize the driver
    print("Initializing WebDriver...")
    driver = initialize_driver()
    print("WebDriver initialized successfully.")

    try:
        print("Scraping GeoPolitical Monitor articles...")
        geopolitical_news_data = scrape_geopolitical_articles(driver, cursor)
        print(f"GeoPolitical Monitor - Articles scraped: {len(geopolitical_news_data)}")

        for article_data in geopolitical_news_data:
            print(f"Inserting article: {article_data.get('title')}")
            insert_news_article_data(cursor=cursor, connection=connection,
                                    title=article_data.get("title"),
                                    subtitle=article_data.get("subtitle"),
                                    context=article_data.get("content"),
                                    image=article_data.get("image_url"),
                                    image_alt=article_data.get("image_alt"),
                                    source="GeoPolitical Monitor",
                                    category="Situation Report",
                                    article_url=article_data.get("url")
            )
        print("GeoPolitical Monitor articles inserted successfully.")

    except Exception as e:
        print("Error scraping GeoPolitical Monitor:", e)

    try:
        print("Scraping The Daily Star articles...")
        thedailystar_news_data = scrape_daily_star_articles(cursor)
        print(f"The Daily Star - Articles scraped: {len(thedailystar_news_data)}")

        for article_data in thedailystar_news_data:
            print("Article data >>>>> ", article_data)
            print(f"Inserting article: {article_data.get('title')}")
            insert_news_article_data(cursor=cursor, connection=connection,
                                    title=article_data.get("title"),
                                    subtitle=article_data.get("subtitle"),
                                    context=article_data.get("content"),
                                    image=article_data.get("image_url"),
                                    image_alt=article_data.get("image_alt"),
                                    source="The Daily Star",
                                    category="World News",
                                    article_url=article_data.get("url")
            )
        print("The Daily Star articles inserted successfully.")

    except Exception as e:
        print("Error scraping The Daily Star:", e)

    try:
        print("Scraping Foreign Affairs articles...")
        forrign_affairs_data = scrape_foreign_affairs_articles(driver, cursor)
        print(f"Foreign Affairs - Articles scraped: {len(forrign_affairs_data)}")

        for article_data in forrign_affairs_data:
            print(f"Inserting article: {article_data.get('title')}")
            insert_news_article_data(cursor=cursor, connection=connection,
                                    title=article_data.get("title"),
                                    subtitle=article_data.get("subtitle"),
                                    context=article_data.get("content"),
                                    image=article_data.get("image_url"),
                                    image_alt=article_data.get("image_alt"),
                                    source="Foreign Affairs",
                                    category="World News",
                                    article_url=article_data.get("url")
            )
        print("Foreign Affairs articles inserted successfully.")

    except Exception as e:
        print("Error scraping Foreign Affairs:", e)

    try:
        print("Scraping Eurasian Times articles...")
        eurasian_times_data = scrape_eurasian_times_articles(driver, cursor)
        print(f"Eurasian Times - Articles scraped: {len(eurasian_times_data)}")

        for article_data in eurasian_times_data:
            print(f"Inserting article: {article_data.get('title')}")
            insert_news_article_data(cursor=cursor, connection=connection,
                                    title=article_data.get("title"),
                                    subtitle=article_data.get("subtitle"),
                                    context=article_data.get("content"),
                                    image=article_data.get("image_url"),
                                    image_alt=article_data.get("image_alt"),
                                    source="Eurasian Times",
                                    category="World News",
                                    article_url=article_data.get("url")
            )
        print("Eurasian Times articles inserted successfully.")

    except Exception as e:
        print("Error scraping Eurasian Times:", e)

    try:
        print("Scraping The Diplomat articles...")
        diplomat_data = scrape_diplomat_articles(driver, cursor)
        print(f"The Diplomat - Articles scraped: {len(diplomat_data)}")

        for article_data in diplomat_data:
            print(f"Inserting article: {article_data.get('title')}")
            insert_news_article_data(cursor=cursor, connection=connection,
                                    title=article_data.get("title"),
                                    subtitle=article_data.get("subtitle"),
                                    context=article_data.get("content"),
                                    image=article_data.get("image_url"),
                                    image_alt=article_data.get("image_alt"),
                                    source="The Diplomat",
                                    category="World News",
                                    article_url=article_data.get("url")
            )
        print("The Diplomat articles inserted successfully.")

    except Exception as e:
        print("Error scraping The Diplomat:", e)

    try:
        print("Scraping BBC News articles...")
        bbc_news_data = scrape_bbc_world_news(cursor)
        print(f"BBC News - Articles scraped: {len(bbc_news_data)}")

        for article_data in bbc_news_data:
            print("Article Data >>>>> ", article_data)
            print(f"Inserting article: {article_data.get('title')}")
            insert_news_article_data(cursor=cursor, connection=connection,
                                    title=article_data.get("title"),
                                    subtitle=article_data.get("subtitle"),
                                    context=article_data.get("content"),
                                    image=article_data.get("image_url"),
                                    image_alt=article_data.get("image_alt"),
                                    source="BBC News",
                                    category="World News",
                                    article_url=article_data.get("url")
            )
        print("BBC News articles inserted successfully.")

    except Exception as e:
        print("Error scraping BBC News:", e)
    
    driver.quit()

if __name__ == "__main__":

    print("Connecting to the database...")
    connection, cursor = get_curser()
    print("Database connection established.")

    print("Starting to scrape all news sites...")
    scrape_all_sites(connection, cursor)
    print("All news sites scraped and data inserted successfully.")
