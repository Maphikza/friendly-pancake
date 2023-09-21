from log_config import logger
from playwright.sync_api import sync_playwright
from image_text_reader import read_image
from currency_update_mailer import send_exchange_rate_email
from failed_currency_check_mailer import send_failed_check_email
from database_update import update_exchange_rate
import time
import os

# Define the URL you want to open
url = os.environ.get('EXCHANGE_URL')

# Define the file name for the screenshot
screenshot_file = 'screenshot.png'


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        time.sleep(5)
        # Take a screenshot and save it to the specified file
        page.screenshot(path=screenshot_file)

        logger.info(f"Screenshot saved as {screenshot_file}")

        browser.close()


if __name__ == '__main__':
    try:
        main()
        answer, rate = read_image(screenshot_file)
        if answer:
            update_exchange_rate_data = update_exchange_rate(rate)
            if update_exchange_rate_data:
                send_exchange_rate = send_exchange_rate_email(rate)
                if send_exchange_rate:
                    logger.info("Exchange rate email is sent.")
        else:
            logger.warning("The system could not find the exchange rate.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        exception_error = str(e)
        send_failed_check_alert = send_failed_check_email(system_error=exception_error)
        logger.info("failed check email is sent.")
