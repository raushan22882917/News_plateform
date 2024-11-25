from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: Run in headless mode
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Main URL to scrape
main_url = 'https://www.thedailystar.net/news/world'
driver.get(main_url)

# Extract article URLs (links to individual articles)
article_elements = driver.find_elements(By.XPATH, '//h3[@class="title fs-20"]/a')
article_urls = [element.get_attribute('href') for element in article_elements]

# Scrape each article's content
articles_data = []
for article_url in article_urls:
    driver.get(article_url)
    article_data = {'url': article_url}
    
    # Use explicit wait to ensure page loads fully
    wait = WebDriverWait(driver, 10)
    try:
        # Wait for the main title to confirm page load
        wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="fw-700 e-mb-16 article-title"]')))
        
        # Extract title
        try:
            title = driver.find_element(By.XPATH, '//h1[@class="fw-700 e-mb-16 article-title"]').text
            article_data['title'] = title
        except NoSuchElementException:
            article_data['title'] = "Title not found"

        # Extract image URL
        try:
            image_elements = driver.find_elements(By.XPATH, '//img[contains(@class, "lazyloaded")]')
            image_urls = [img.get_attribute('data-srcset') or img.get_attribute('srcset') for img in image_elements if img.get_attribute('data-srcset') or img.get_attribute('srcset')]
            article_data['image_url'] = image_urls if image_urls else "Image not found"
        except NoSuchElementException:
            article_data['image_url'] = "Image not found"

        # Extract content paragraphs
        try:
            content_paragraphs = driver.find_elements(By.XPATH, '//div[@class="pb-20 clearfix"]//p')
            content = " ".join([p.text for p in content_paragraphs])
            article_data['content'] = content if content else "Content not found"
        except NoSuchElementException:
            article_data['content'] = "Content not found"

        # Append extracted data
        articles_data.append(article_data)

    except TimeoutException:
        print(f"Page load timeout for {article_url}")
        continue

# Save data to JSON
with open('dailystar_articles_data.json', 'w') as json_file:
    json.dump(articles_data, json_file, indent=4)

print(f"Scraped data for {len(articles_data)} articles.")
driver.quit()
