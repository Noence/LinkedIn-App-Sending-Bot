from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

EMAIL = YOUR LINKEDIN EMAIL
PASSWORD = YOUR LINKEDIN PASSWORD
PHONE_NUMBER = YOUR PHONE NUMBER 
PHONE_REGION = YOUR PHONE REGION (us, fr, en, ...)
JOB_NAME = YOUR JOB NAME
REGION = YOUR REGION
chrome_driver_path = YOUR CHROME DRIVER PATH
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://www.linkedin.com/jobs/search/")

# Sign in code
time.sleep(1)
sign_in = driver.find_element_by_xpath("/html/body/div[2]/header/nav/div/a[2]")
sign_in.click()
time.sleep(1)
email = driver.find_element_by_id("username")
email.send_keys(EMAIL)
password = driver.find_element_by_id("password")
password.send_keys(PASSWORD)
sign_in = driver.find_element_by_css_selector(".login__form_action_container button")
sign_in.click()

# Add if Linkedin asks you to make sure you're not a bot
time.sleep(20)

# Searches for the job of your choosing
search_box = driver.find_element_by_css_selector("#ember47 input")
search_box.clear()
search_box.send_keys(JOB_NAME)
country_box = driver.find_element_by_css_selector("#ember49 input")
country_box.clear()
country_box.send_keys(REGION)
country_box.send_keys(Keys.ENTER)
time.sleep(1)
easy_apply_button = driver.find_element_by_css_selector("div .search-reusables__filter-binary-toggle button")
if easy_apply_button.get_attribute("aria-checked"):
    pass
else:
    easy_apply_button.click()
time.sleep(1)


def send_applications():
    jobs = driver.find_elements_by_class_name("jobs-search-results__list-item")

    for job in jobs:
        job.find_element_by_css_selector("img").click()
        time.sleep(1)

        # App sender
        try:
            apply_now_button = driver.find_element_by_css_selector("div.jobs-apply-button--top-card button")
            apply_now_button.click()
            apply_now_button = driver.find_element_by_css_selector("button.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view")
            # Skips jobs if you can't immediately send the application
            if apply_now_button.text.lower() == "next":
                close_button = driver.find_element_by_css_selector(".artdeco-modal__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view")
                close_button.click()
                time.sleep(0.5)
                discard = driver.find_element_by_css_selector("button.artdeco-modal__confirm-dialog-btn.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view")
                discard.click()
            else:
                # Changes phone number country code
                country_code = driver.find_element_by_css_selector(f"div.fb-dropdown select option[value='urn:li:country:{PHONE_REGION}']").click()
                phone_number_text_box = driver.find_element_by_css_selector("div.fb-single-line-text div.display-flex input")
                # Inputs your phone number
                phone_number_text_box.clear()
                phone_number_text_box.send_keys(PHONE_NUMBER)
                # Submit app
                submit_button = driver.find_element_by_css_selector("button.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view")
                submit_button.click()
        except NoSuchElementException:
            # Skips if app has already been sent/not taking apps anymore
            # print(f"The Job {job.text} is too complex to be automated")
            continue
        time.sleep(1)

        # Get rid of all pop-ups that could break the code
        if driver.find_elements_by_css_selector("div.artdeco-modal.artdeco-modal--layer-default.post-apply-modal") != []:
            driver.find_element_by_css_selector("button.artdeco-modal__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view").click()

        if driver.find_elements_by_css_selector("div.artdeco-modal.artdeco-modal--layer-default[role='dialog']") != []:
            driver.find_element_by_css_selector("button artdeco-modal__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view").click()

        if driver.find_elements_by_css_selector("li.artdeco-toast-item.artdeco-toast-item--visible.ember-view[data-test-artdeco-toast-item-type='success']") != []:
            driver.find_element_by_css_selector("button.artdeco-toast-item__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--1.artdeco-button--tertiary.ember-view").click()


send_applications()
new_section = False
pages = driver.find_elements_by_css_selector("li.artdeco-pagination__indicator.artdeco-pagination__indicator--number.ember-view")
number_pages = int(pages[-1].find_element_by_css_selector("span").text)
print(number_pages)
if number_pages > 1:
    for page_number in range(2, number_pages+1):
        time.sleep(1)
        new_pages = driver.find_elements_by_css_selector("li.artdeco-pagination__indicator.artdeco-pagination__indicator--number.ember-view")
        for page in new_pages:
            if page.find_element_by_css_selector("span").text == str(page_number):
                page.click()
                new_section = False
                break
            else:
                new_section = True
        if new_section:
            for page in new_pages:
                if page.find_element_by_css_selector("span").text == "…":
                    page.click()
                    new_section = False
                    break
        send_applications()
