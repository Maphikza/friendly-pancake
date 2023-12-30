import asyncio
from playwright.async_api import async_playwright
import os
from log_config import logger

email = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')
login_url = os.environ.get('LOGIN_URL')


async def automate_website(conversion_rate):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Open a specific URL
        await page.goto(login_url)

        # Enter email and password
        await page.fill('input[name="email"]', email)
        await page.fill('input[name="password"]', password)

        # Press Enter after filling the password field
        await page.press('input[name="password"]', 'Enter')

        # Wait for navigation to complete
        await page.wait_for_load_state('load')

        # Wait for the Admin link to appear
        admin_link = await page.wait_for_selector('xpath=/html/body/nav/div/div/div[1]/a[4]')
        if admin_link:
            await admin_link.click()

        # Wait for navigation to Admin page
        await page.wait_for_load_state('load')

        # Click the "Fees and Currency Update" link using the provided XPath
        await page.click('xpath=/html/body/div[1]/div[1]/p/a')

        # Wait for the Fees and Currency Update section to expand
        await page.wait_for_selector('xpath=//*[@id="FeesCollapse"][contains(@class, "show")]')

        # Type the value into the input field for AUD conversion rate
        await page.fill('input#aud_conversion_rate', conversion_rate)

        # Click the button to submit the form
        await page.click('xpath=/html/body/div[1]/div[1]/div/div/div/div/form/button')

        # Wait for 5 seconds
        await asyncio.sleep(5)

        # Close the page
        await page.close()
        await context.close()
        await browser.close()
        print("Website updated successfully!")
        logger.info("Exchange Rate updated")
        return True
