import time
from selenium.webdriver.common.by import By
from insert_queries import article_exists

def scrape_article_details(driver, article_url):
    """
    Scrapes details from a single article page.
    """
    print(f"Navigating to article URL: {article_url}")
    driver.get(article_url)
    time.sleep(3)

    # Initialize article data
    article_data = {'url': article_url}

    # Extract title
    try:
        article_data['title'] = driver.find_element(By.CSS_SELECTOR, 'h1.entry-title').text
        print(f"Title extracted: {article_data['title']}")
    except Exception as e:
        article_data['title'] = "Title not found"
        print(f"Error scraping title from {article_url}: {e}")

    # Extract date
    try:
        article_data['date'] = driver.find_element(By.CSS_SELECTOR, 'span.td-post-date time.entry-date').text
        print(f"Date extracted: {article_data['date']}")
    except Exception as e:
        article_data['date'] = "Date not found"
        print(f"Error scraping date from {article_url}: {e}")

    # Extract content
    try:
        content_div = driver.find_element(By.CSS_SELECTOR, 'div.td-post-content')
        paragraphs = content_div.find_elements(By.TAG_NAME, 'p')
        article_data['content'] = "\n".join([p.text for p in paragraphs])
        print("Content extracted successfully.")
    except Exception as e:
        article_data['content'] = "Content not found"
        print(f"Error scraping content from {article_url}: {e}")

    # Extract image URL
    try:
        article_data['image_url'] = driver.find_element(By.CSS_SELECTOR, 'figure.wp-caption img').get_attribute('src')
        print(f"Image URL extracted: {article_data['image_url']}")
    except Exception as e:
        article_data['image_url'] = "Image not found"
        print(f"Error scraping image from {article_url}: {e}")

    return article_data

def scrape_eurasian_times_articles(driver, connection):
    """
    Scrapes articles from the main page of Eurasian Times and returns details for each article.
    """
    main_url = "https://www.eurasiantimes.com/category/world/"
    print(f"Navigating to main page: {main_url}")
    driver.get(main_url)
    time.sleep(3)
    print("Main page loaded. Extracting article links...")

    # Find all article URLs
    article_elements = driver.find_elements(By.CSS_SELECTOR, 'h3.entry-title.td-module-title a')
    article_urls = [element.get_attribute('href') for element in article_elements]
    print(f"Found {len(article_urls)} articles on the main page.")

    articles_data = []
    for article_url in article_urls:
        # Check if the article URL already exists in the database
        if article_exists(connection, article_url):
            print(f"Article already exists in the database: {article_url}")
            continue

        print(f"Scraping article at {article_url}...")
        article_data = scrape_article_details(driver, article_url)
        articles_data.append(article_data)
        print(f"Article details scraped successfully: {article_url}")

    print(f"Scraping complete. Total articles scraped: {len(articles_data)}")
    return articles_data
