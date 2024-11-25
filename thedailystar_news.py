from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from dotenv import load_dotenv
import os
from insert_queries import article_exists

load_dotenv()


def scrape_daily_star_articles(connection):
    """
    Scrapes articles from The Daily Star world news page and saves data to a JSON file.
    """
    # Set up Chrome options
    run_config = os.getenv("RUN_CONFIG")

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if run_config == "True":
        print("DONE")
        chrome_options.binary_location = "/usr/bin/chromium"
        service = Service(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        print("DONE 2")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Main URL to scrape
        main_url = 'https://www.thedailystar.net/news/world'
        driver.get(main_url)
        time.sleep(3)  # Allow time for the page to load

        # Extract article URLs (links to individual articles)
        article_elements = driver.find_elements(By.XPATH, '//h3[@class="title fs-20"]/a')
        article_urls = [element.get_attribute('href') for element in article_elements]

        articles_data = []
        for article_url in article_urls:

            if article_exists(connection, article_url):
                print(f"Article already exists in the database: {article_url}")
                continue

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(article_url)

            # Use explicit wait to ensure page loads fully
            wait = WebDriverWait(driver, 10)
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="fw-700 e-mb-16 article-title"]')))
            except TimeoutException:
                print("Page did not load fully.")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

            article_data = {'url': article_url}

            # Extract title
            try:
                title = driver.find_element(By.XPATH, '//h1[@class="fw-700 e-mb-16 article-title"]').text
            except NoSuchElementException:
                title = "Title not found"

            # Extract image URLs
            try:
                image_elements = driver.find_elements(By.XPATH, '//img[contains(@class, "lazyloaded")]')
                image_urls = [img.get_attribute('data-srcset') or img.get_attribute('srcset') for img in image_elements if img.get_attribute('data-srcset') or img.get_attribute('srcset')]
            except (NoSuchElementException, TimeoutException):
                image_urls = "Image not found"

            # Extract content paragraphs
            content = ''
            try:
                content_paragraphs = driver.find_elements(By.XPATH, '//div[@class="pb-20 clearfix"]//p')
                content = " ".join([p.text for p in content_paragraphs]) or "Content not found"
            except NoSuchElementException:
                content = "Content not found"

            # Add extracted data to the article dictionary
            article_data['title'] = title
            article_data['image_url'] = image_urls
            article_data['content'] = content

            articles_data.append(article_data)

            # Close the current window and return to the main window
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        return articles_data

    finally:
        # Quit the driver
        driver.quit()
