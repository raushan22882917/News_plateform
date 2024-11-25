import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from insert_queries import article_exists

def scrape_diplomat_article_details(driver, article_url):
    """
    Scrapes details from a single article page on The Diplomat.
    """
    print(f"Navigating to article URL: {article_url}")
    driver.get(article_url)
    time.sleep(3)

    # Initialize article data
    article_data = {'url': article_url}

    # Extract title
    try:
        article_data['title'] = driver.find_element(By.XPATH, '//h1[@id="td-headline"]').text
        print(f"Title extracted: {article_data['title']}")
    except NoSuchElementException:
        article_data['title'] = "Title not found"
        print("Title not found.")

    # Extract subtitle
    try:
        article_data['subtitle'] = driver.find_element(By.XPATH, '//div[@id="td-lead"]/p').text
        print(f"Subtitle extracted: {article_data['subtitle']}")
    except NoSuchElementException:
        article_data['subtitle'] = "Subtitle not found"
        print("Subtitle not found.")

    # Extract date
    try:
        article_data['date'] = driver.find_element(By.XPATH, '//div[@class="td-date"]').text
        print(f"Date extracted: {article_data['date']}")
    except NoSuchElementException:
        article_data['date'] = "Date not found"
        print("Date not found.")

    # Extract image URL and attributes
    try:
        image = driver.find_element(By.XPATH, '//div[@class="td-img"]//img')
        article_data['image_url'] = image.get_attribute('src')
        article_data['image_alt'] = image.get_attribute('alt')
        article_data['image_title'] = image.get_attribute('title')
        print(f"Image details extracted - URL: {article_data['image_url']}, Alt: {article_data['image_alt']}, Title: {article_data['image_title']}")
    except NoSuchElementException:
        article_data['image_url'] = "Image not found"
        article_data['image_alt'] = "Alt text not found"
        article_data['image_title'] = "Image title not found"
        print("Image details not found.")

    # Extract content paragraphs
    try:
        content_paragraphs = driver.find_elements(By.XPATH, '//section[@class="td-23-story-body td-prose tda-gated tda-gated--unlocked tda-gated--out"]//p')
        article_data['content'] = " ".join([p.text for p in content_paragraphs]) or "Content not found"
        print("Content extracted successfully.")
    except NoSuchElementException:
        article_data['content'] = "Content not found"
        print("Content not found.")

    return article_data

def scrape_diplomat_articles(driver, connection):
    """
    Scrapes articles from the main page of The Diplomat and returns details for each article.
    """
    main_url = 'https://thediplomat.com/topics/politics/'
    print(f"Navigating to main page: {main_url}")
    driver.get(main_url)
    time.sleep(3)
    print("Main page loaded. Extracting article links...")

    # Extract article URLs
    article_elements = driver.find_elements(By.XPATH, '//a[@class="td-post"]')
    article_urls = [main_url + element.get_attribute('href') for element in article_elements]
    print(f"Found {len(article_urls)} articles on the main page.")

    articles_data = []
    for article_url in article_urls:
        
        # Check if the article URL already exists in the database
        if article_exists(connection, article_url):
            print(f"Article already exists in the database: {article_url}")
            continue

        # Open article in a new tab and scrape details
        print(f"Scraping details from article: {article_url}")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        
        try:
            article_data = scrape_diplomat_article_details(driver, article_url)
            articles_data.append(article_data)
            print(f"Article details scraped successfully: {article_url}")
        except Exception as e:
            print(f"Error scraping article {article_url}: {e}")
        
        # Close the current window and return to the main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(f"Closed tab for {article_url} and returned to main page.")

    print(f"Scraping complete. Total articles scraped: {len(articles_data)}")
    return articles_data
