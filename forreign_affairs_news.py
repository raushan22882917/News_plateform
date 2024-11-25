from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from insert_queries import article_exists
import time

def scrape_foreign_affairs_articles(driver, connection):
    main_url = 'https://www.foreignaffairs.com/browse/view-all'
    print(f"Navigating to main URL: {main_url}")
    
    # Open main URL
    driver.get(main_url)
    time.sleep(3)
    print("Main page loaded. Extracting article URLs...")

    # Extract article URLs
    article_elements = driver.find_elements(By.XPATH, '//*[@id="react-browse-results"]/div[2]/div/div[1]/div/article//div/div[2]/div[2]/a')
    article_urls = [element.get_attribute('href') for element in article_elements]
    print(f"Found {len(article_urls)} articles on the main page.")

    articles_data = []
    for article_url in article_urls:
        print(f"Processing article: {article_url}")

        # Check if the article URL already exists in the database
        if article_exists(connection, article_url):
            print(f"Article already exists in the database: {article_url}")
            continue

        # Open article in a new tab
        print(f"Opening article in a new tab: {article_url}")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(article_url)
        time.sleep(3)

        article_data = {'url': article_url}

        # Extract title
        try:
            title = driver.find_element(By.XPATH, '//h1[@class="f-serif ls-0 article-title border-top pt-3"]').text
            print(f"Title extracted: {title}")
        except NoSuchElementException:
            try:
                title = driver.find_element(By.XPATH, '//div[@class="col-lg-11 article-header--metadata-content"]/h1').text
                print(f"Title extracted from alternate location: {title}")
            except NoSuchElementException:
                title = "Title not found"
                print("Title not found.")

        # Extract subtitle
        try:
            sub_title = driver.find_element(By.XPATH, '//h2[@class="f-serif ls-0 article-subtitle fs-24"]').text
            print(f"Subtitle extracted: {sub_title}")
        except NoSuchElementException:
            try:
                sub_title = driver.find_element(By.XPATH, '//div[@class="col-lg-11 article-header--metadata-content"]/h2').text
                print(f"Subtitle extracted from alternate location: {sub_title}")
            except NoSuchElementException:
                sub_title = "Subtitle not found"
                print("Subtitle not found.")

        # Extract image (if available)
        try:
            image_url = driver.find_element(By.XPATH, '//figure[@class="article-inline-img-block print-hidden"]//img').get_attribute('srcset')
            print(f"Image URL extracted: {image_url}")
        except NoSuchElementException:
            image_url = "Image not found"
            print("Image not found.")

        # Extract image caption (if available)
        try:
            image_caption = driver.find_element(By.XPATH, '//figcaption[@class="article-inline-img-block--figcaption ls-narrow f-sans mt-2 print-hidden"]/div').text
            print(f"Image caption extracted: {image_caption}")
        except NoSuchElementException:
            image_caption = "Caption not found"
            print("Caption not found.")

        # Extract date
        try:
            date = driver.find_element(By.XPATH, '//time[@class="font-weight-600 d-inline-block mt-2"]').text
            print(f"Date extracted: {date}")
        except NoSuchElementException:
            try:
                date = driver.find_element(By.XPATH, '//span[@class="article-header--metadata-date align-self-center col-6 col-sm-auto"]/time').text
                print(f"Date extracted from alternate location: {date}")
            except NoSuchElementException:
                date = "Date not found"
                print("Date not found.")

        # Extract content paragraphs
        content = ''
        try:
            content_paragraphs = driver.find_elements(By.XPATH, '//div[@class="article-dropcap no-colophon f-serif tab-pane fade show active"]//p')
            if not content_paragraphs:
                content_paragraphs = driver.find_elements(By.XPATH, '//div[@class="article-dropcap--inner paywall-content"]//p')
            if not content_paragraphs:
                content_paragraphs = driver.find_elements(By.XPATH, '//div[@class="article-dropcap--inner paywall-content article__body-content mt-md-0 mb-md-0 col-12 col-md-6-base-10"]//p')
            content = " ".join([p.text for p in content_paragraphs])
            print("Content extracted successfully.")
        except NoSuchElementException:
            content = "Content not found"
            print("Content not found.")

        # Add extracted data to the article dictionary
        article_data.update({
            'title': title,
            'subtitle': sub_title,
            'date': date,
            'image_url': image_url,
            'image_alt': image_caption,
            'content': content,
            "url": article_url
        })

        articles_data.append(article_data)
        print(f"Article data appended for URL: {article_url}")

        # Close the current window and return to the main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(f"Closed tab for {article_url} and returned to main page.")

    print(f"Scraping complete. Total articles scraped: {len(articles_data)}")
    return articles_data
