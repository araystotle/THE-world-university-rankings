from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd

driver = webdriver.Edge()

website = 'https://www.timeshighereducation.com/world-university-rankings/2024/world-ranking'
driver.get(website)
driver.maximize_window()

rank = []
name = []
country = []
student_population = []
students_staff_ratio = []
international_students = []
female_male_ratio = []
overall_score = []
teaching = []
research_environment = []
research_quality = []
industry_impact = []
international_outlook = []

# select 'All' to display all universities in one page
dropdown = Select(driver.find_element(By.XPATH, '//select[@name="datatable-1_length"]'))
dropdown.select_by_visible_text('All')

# wait for elements to load
table_condition = EC.presence_of_all_elements_located((By.XPATH, '//table[@id="datatable-1"]/tbody/tr'))
universities = WebDriverWait(driver, 5).until(table_condition)

for university in universities:
    rank.append(university.find_element(By.XPATH, './td[1]').text)
    institution = university.find_elements(By.XPATH, './/a[@class="ranking-institution-title"]')
    if len(institution) > 0:  # check if the university is enabled
        uni_name = university.find_element(By.XPATH, './/a[@class="ranking-institution-title"]').text
        print(uni_name)
        name.append(uni_name)
        country_name = university.find_element(By.XPATH, './td[2]/div').text
        # print(country_name)
        country.append(country_name)
        student_population.append(university.find_element(By.XPATH, './td[3]').text)
        students_staff_ratio.append(university.find_element(By.XPATH, './td[4]').text)
        international_students.append(university.find_element(By.XPATH, './td[5]').text)
        female_male_ratio.append(university.find_element(By.XPATH, './td[6]').text)
    else:
        uni_name = university.find_element(By.XPATH, './td[2]/div[1]').text
        print(uni_name)
        name.append(uni_name)
        country_name = university.find_element(By.XPATH, './td[2]/div[2]').text
        # print(country_name)
        country.append(country_name)
        student_population.append(university.find_element(By.XPATH, './td[3]').text)
        students_staff_ratio.append(university.find_element(By.XPATH, './td[4]').text)
        international_students.append(university.find_element(By.XPATH, './td[5]').text)
        female_male_ratio.append(university.find_element(By.XPATH, './td[6]').text)

# move to the scores tab
scores_button_condition = EC.element_to_be_clickable((By.XPATH, '//ul[@class="list-unstyled"]/li[2]/label/span'))
scores_button = WebDriverWait(driver, 5).until(scores_button_condition)
scores_button.click()

# wait for elements to load
rows_condition = EC.presence_of_all_elements_located((By.XPATH, '//table[@id="datatable-1"]/tbody/tr'))
rows = WebDriverWait(driver, 5).until(rows_condition)

for i, row in enumerate(rows):
    print(f"Extra Info Row {i+1}")
    overall_score.append(row.find_element(By.XPATH, './td[3]').text)
    teaching.append(row.find_element(By.XPATH, './td[4]').text)
    research_environment.append(row.find_element(By.XPATH, './td[5]').text)
    research_quality.append(row.find_element(By.XPATH, './td[6]').text)
    industry_impact.append(row.find_element(By.XPATH, './td[7]').text)
    international_outlook.append(row.find_element(By.XPATH, './td[8]').text)


university_df = pd.DataFrame({'Rank': rank,
                              'Name': name,
                              'Country': country,
                              'Student Population': student_population,
                              'Students to Staff Ratio': students_staff_ratio,
                              'International Students': international_students,
                              'Female to Male Ratio': female_male_ratio,
                              'Overall Score': overall_score,
                              'Teaching': teaching,
                              'Research Environment': research_environment,
                              'Research Quality': research_quality,
                              'Industry Impact': industry_impact,
                              'International Outlook': international_outlook,
                              })

university_df.to_csv('files/university_rankings_2024.csv', index=False)
print(university_df)
