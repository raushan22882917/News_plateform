from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv
import os
from insert_queries import article_exists

load_dotenv()


def scrape_bbc_world_news(connection):
    """
    Scrapes articles from the BBC World News page and saves data to a JSON file.
    """
    run_config = os.getenv("RUN_CONFIG")

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--ssl-version-min=tls1.2')  # Enforce TLS 1.2 or later
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")


    if run_config == "True":
        print("DONE")
        chrome_options.binary_location = "/usr/bin/chromium"
        service = Service(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        print("DONE 2")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Define the URL to scrape
    url = "https://www.bbc.com/news/world"
    driver.get(url)
    time.sleep(3)  # Allow some time for the page to load

    # Initialize a list to store scraped data
    news_data = []

    # Locate and iterate through articles
    articles = driver.find_elements(By.CLASS_NAME, "sc-2e6baa30-0")  # Class for links to articles

    for article in articles:
        try:
            # Extract article link
            link = article.get_attribute("href")

            if article_exists(connection, link):
                print(f"Article already exists in the database: {link}")
                continue
            
            # Click and open the article in a new tab
            driver.execute_script("window.open(arguments[0], '_blank');", link)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)  # Wait for article page to load

            # Get article title
            title = driver.find_element(By.CSS_SELECTOR, "h1.sc-518485e5-0.bWszMR").text

            # Get publication time
            publish_time = driver.find_element(By.CLASS_NAME, "sc-2b5e3b35-2").text

            # Get image URL
            image_element = driver.find_element(By.CSS_SELECTOR, "div[data-testid='hero-image'] img")
            image_url = image_element.get_attribute("srcset")

            # Get content (all <p> tags with class sc-eb7bd5f6-0 fYAfXe)
            content_div = driver.find_elements(By.CLASS_NAME, "sc-eb7bd5f6-0.fYAfXe")
            content = " ".join([p.text for p in content_div])

            # Store extracted data
            news_data.append({
                "title": title,
                "url": link,
                "publish_time": publish_time,
                "image_url": image_url,
                "content": content
            })

            # Close the article tab and switch back
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"Error extracting data: {e}")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue

    print("Scraping complete. Data saved to bbc_news_data.json")

    return news_data