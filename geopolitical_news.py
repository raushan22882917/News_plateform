from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from insert_queries import article_exists

def scrape_geopolitical_articles(driver, curser):
    main_url = 'https://www.geopoliticalmonitor.com/'
    print(f"Navigating to main URL: {main_url}")
    
    driver.get(main_url)
    time.sleep(3)
    print("Main page loaded. Extracting article URLs...")

    article_elements = driver.find_elements(By.XPATH, '//h1[@class="article-title"]/a')
    article_urls = [element.get_attribute('href') for element in article_elements]
    print(f"Found {len(article_urls)} articles.")

    articles_data = []
    for article_url in article_urls:
        print(f"Processing article: {article_url}")

        if article_exists(curser, article_url):
            print(f"Article already exists in the database: {article_url}")
            continue

        print(f"Opening article in a new tab: {article_url}")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(article_url)
        time.sleep(3)

        article_data = {'url': article_url}

        # Extract title
        try:
            title = driver.find_element(By.XPATH, '//h1[@class="article-title"]').text
            print(f"Title extracted: {title}")
        except NoSuchElementException:
            title = "Title not found"
            print("Title not found.")

        # Extract metadata (tags and date)
        try:
            article_meta = driver.find_element(By.XPATH, '//div[@class="article-meta"]')
            tags = article_meta.find_element(By.XPATH, './/span[@class="article-tag"]/a').text
            date = article_meta.find_element(By.XPATH, './/span[@class="article-date"]').text
            print(f"Metadata extracted - Tags: {tags}, Date: {date}")
        except NoSuchElementException:
            tags = "Tags not found"
            date = "Date not found"
            print("Metadata not found.")

        # Extract image details
        try:
            image_url = driver.find_element(By.XPATH, '//div[@class="archive-photo"]//img').get_attribute('src')
            image_alt = driver.find_element(By.XPATH, '//div[@class="archive-photo"]//img').get_attribute('alt')
            image_title = driver.find_element(By.XPATH, '//div[@class="archive-photo"]//img').get_attribute('title')
            print(f"Image details extracted - URL: {image_url}, Alt: {image_alt}, Title: {image_title}")
        except NoSuchElementException:
            image_url = "Image not found"
            image_alt = "Alt text not found"
            image_title = "Image title not found"
            print("Image details not found.")

        # Extract content
        try:
            content = driver.find_element(By.XPATH, '//div[@class="article-content"]//p').text
            print("Content extracted successfully.")
        except NoSuchElementException:
            try:
                content = driver.find_element(By.XPATH, '//div[@class="article-body"]//p').text
                print("Content extracted successfully from alternate location.")
            except NoSuchElementException:
                content = "Content not found"
                print("Content not found.")

        article_data.update({
            'title': title,
            'subtitle': "",
            'tags': tags,
            'date': date,
            'image_url': image_url,
            'image_alt': image_alt,
            'image_title': image_title,
            'content': content,
            "url": article_url
        })

        articles_data.append(article_data)
        print(f"Article data appended for URL: {article_url}")

        # Close the current window and return to the main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(f"Closed tab for {article_url} and returned to the main page.")

    print(f"Scraping complete. Total articles scraped: {len(articles_data)}")
    return articles_data
