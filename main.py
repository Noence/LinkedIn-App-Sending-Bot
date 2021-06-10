from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

EMAIL = "example@email.com"
PASSWORD = "password!"
PHONE_NUMBER = "0000000000"
REGION = "us"

chrome_driver_path = r"C:\Users\DSDLn\Documents\Dev\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=2566892130&f_AL=true&geoId=91000000&keywords=aerospace%20engineer%20intern&location=European%20Union")

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

# Add if Linkedin asks you to make sure you're not a bot so you have time to complete the Captcha
# time.sleep(30)

# Searches for the job of your choosing
search_box = driver.find_element_by_css_selector("#ember47 input")
search_box.clear()
search_box.send_keys("space intern")
country_box = driver.find_element_by_css_selector("#ember49 input")
country_box.clear()
country_box.send_keys("European Union")
country_box.send_keys(Keys.ENTER)
time.sleep(1)
easy_apply_button = driver.find_element_by_css_selector("div .search-reusables__filter-binary-toggle button")
if easy_apply_button.get_attribute("aria-checked"):
    pass
else:
    easy_apply_button.click()
time.sleep(1)
jobs = driver.find_elements_by_class_name("jobs-search-results__list-item")
print(len(jobs))

for job in jobs:
    job.click()
    time.sleep(1)

    # Get rid of all pop-ups that could break the code
    if driver.find_elements_by_css_selector("div.artdeco-modal.artdeco-modal--layer-default.post-apply-modal") != []:
        driver.find_element_by_css_selector("button.artdeco-modal__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view").click()

    if driver.find_elements_by_css_selector("div.artdeco-modal.artdeco-modal--layer-default[role='dialog']") != []:
        driver.find_element_by_css_selector("button artdeco-modal__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view").click()

    if driver.find_elements_by_css_selector("li.artdeco-toast-item.artdeco-toast-item--visible.ember-view[data-test-artdeco-toast-item-type='success']") != []:
        driver.find_element_by_css_selector("button.artdeco-toast-item__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--1.artdeco-button--tertiary.ember-view").click()

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
            country_code = driver.find_element_by_css_selector(f"div.fb-dropdown select option[value='urn:li:country:{REGION}']").click()
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
