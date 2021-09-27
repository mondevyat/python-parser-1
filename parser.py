from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

CSV = 'articles.csv'
URL = 'https://cyberleninka.ru/search?q=React%20framework&page=1'

def save_doc(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Автор(ы)', 'Год', 'Издательство', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['author'], item['year'], item['publisher'], item['link']])

def main():
    driver = webdriver.Chrome()
    driver.get(URL)

    page = 0
    articles = []
    pagination = driver.find_element_by_class_name('paginator')
    pages = pagination.find_elements_by_tag_name('li')

    pages_needed = int(input('Количество требуемых страниц (от 1 до ' + str(len(pages)) + '): '))
    while True:
        try:
            if (pages_needed >= 1 and pages_needed <= len(pages)):
                break
            else:
                pages_needed = int(input('Повторите ввод (от 1 до ' + str(len(pages)) + '): '))
        except ValueError:
            print('Введите число')

    for j in range(pages_needed):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'search-results')))
        ul = driver.find_element_by_id('search-results')
        li = ul.find_elements_by_tag_name('li')

        pagination = driver.find_element_by_class_name('paginator')
        pages = pagination.find_elements_by_tag_name('li')

        print('\n\n\n+++++++++++++++\n'
             +'+             +\n'
             +'+ Страница №' + pages[page].text + ' +\n'
             +'+             +\n'
             +'+++++++++++++++\n\n\n')
        for i in range(len(li)):
            title = li[i].find_element_by_tag_name('a')
            authors = li[i].find_element_by_tag_name('span')
            year = li[i].find_element_by_class_name('span-block')
            publisher = year.find_element_by_tag_name('a')
            link = publisher.get_attribute('href')
            year = year.text[:4]

            articles.append(
                {
                    'title': title.text,
                    'author': authors.text,
                    'year': year,
                    'publisher': publisher.text,
                    'link': link
                }
            )

            print('Название статьи  |  ' + title.text + '\n'
                 +'Автор(ы) статьи  |  ' + authors.text + '\n'
                 +'Год статьи       |  ' + year + '\n'
                 +'Издательство     |  ' + publisher.text + '\n'
                 +'Ссылка на статью |  ' + link + '\n'
                 +'\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n')
        page += 1

        if (page >= pages_needed):
            print('\n\n\n* Конец! Файл с названием \"' + CSV + '\" создан в локальной директории *\n\n\n')
            save_doc(articles, CSV)
            break
        else:
            pages[page].find_element_by_tag_name('a').click()

main()