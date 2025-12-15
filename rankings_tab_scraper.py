from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time


driver = webdriver.Firefox()

website = 'https://www.timeshighereducation.com/world-university-rankings/latest/world-ranking'
driver.get(website)
driver.maximize_window()

cookies_decline_btn = driver.find_element(By.ID, 'CybotCookiebotDialogBodyButtonDecline')
cookies_decline_btn.click()

rank = []
name = []
country = []
overall_score = []
teaching = []
research_environment = []
research_quality = []
industry_score = []
international_outlook = []
university_ids = set()

# the scrollable window containing the universities
universities_container = driver.find_element(By.XPATH, '//div[@class="css-1bggjdb"]')

# scroll height that is used during scrolling
previous_height = driver.execute_script("return arguments[0].scrollHeight", universities_container)

while True:
    # scroll slowly in small steps (50px per step)
    # get university details in every scroll
    for scroll_pos in range(0, previous_height, 50):
        university_entries = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//tr[@class="css-77a2e3" or @class="css-1mirs6g" or @class="css-qxb52u"]'))
        )

        for entry in university_entries:
            try:
                institution = entry.find_elements(By.XPATH, './/a[contains(@class, "institution-link")]')
                if len(institution) > 0: # universities with active links
                    uni_name = entry.find_element(By.XPATH, './/a[contains(@class, "institution-link")]').text
                    country_name = entry.find_element(By.XPATH, './/a[contains(@data-type, "location")]').text
                    university_id = uni_name + ' ' + country_name
                else: # universities with inactive links
                    uni_name = entry.find_element(By.XPATH, './td[2]/div[1]/div[1]').text
                    uni_name = uni_name.split('\n')[0]
                    country_name = entry.find_element(By.XPATH, './td[2]/div[1]/div[1]/span/span').text
                    university_id = uni_name + ' ' + country_name

                # check that the university is not scraped twice
                if university_id not in university_ids:
                    university_ids.add(university_id)

                    uni_pos = entry.find_element(By.XPATH, './/td[contains(@class, "cell-rank")]').text

                    print(f"{uni_pos}. {uni_name}")
                    name.append(uni_name)
                    print(country_name)
                    country.append(country_name)
                    print("---------------------------------------------")

                    rank.append(uni_pos)
                    overall_score.append(entry.find_element(By.XPATH, './td[3]').text)
                    teaching.append(entry.find_element(By.XPATH, './td[4]').text)
                    research_environment.append(entry.find_element(By.XPATH, './td[5]').text)
                    research_quality.append(entry.find_element(By.XPATH, './td[6]').text)
                    industry_score.append(entry.find_element(By.XPATH, './td[7]').text)
                    international_outlook.append(entry.find_element(By.XPATH, './td[8]').text)
            except StaleElementReferenceException:
                print(f"Error: Stale element encountered")
                print("---------------------------------------------")

        # end loop once we finish scraping ranked universities
        if "Reporter" in rank:
            print("Reporter rank encountered")
            print("---------------------------------------------")
            break

        driver.execute_script(f"arguments[0].scrollTo(0, {scroll_pos});", universities_container)
        time.sleep(2)

    time.sleep(2)

    new_height = driver.execute_script("return arguments[0].scrollHeight", universities_container)

    if new_height == previous_height:
        break
    else:
        previous_height = new_height

driver.quit()

university_df = pd.DataFrame({'Rank': rank,
                              'Name': name,
                              'Country': country,
                              'Overall Score': overall_score,
                              'Teaching': teaching,
                              'Research Environment': research_environment,
                              'Research Quality': research_quality,
                              'Industry Score': industry_score,
                              'International Outlook': international_outlook,
                              })

university_df.to_csv('files/university_rankings_2026_raw_rankings.csv', index=False)
print(university_df)