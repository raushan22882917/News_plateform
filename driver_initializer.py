from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

load_dotenv()

def initialize_driver():
    # Load configuration from environment
    run_config = os.getenv("RUN_CONFIG")
    print("RUN CONFIG > ", run_config)

    # Set up Chrome options
    options = Options()
    options.add_argument('--headless=new')  # Headless mode (new flag for modern versions of Chrome)
    options.add_argument('--no-sandbox')    # Required for running as root in a container
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-gpu")   # Disable GPU acceleration
    options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation features

    # Set up the driver depending on RUN_CONFIG
    if run_config == "True":
        print("DONE")
        options.binary_location = "/usr/bin/chromium"
        service = Service(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
    else:
        print("DONE 2")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver
