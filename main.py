from modules import *

try:
    conn = sqlite3.connect('Henry.db')
    cur = conn.cursor()
    print('Connected to db')
    #table already created in DB. 
        #CREATE TABLE "Vaccums" (
        #"UID"	INTEGER NOT NULL UNIQUE,
        #"Name"	TEXT NOT NULL,
        #"Price"	INTEGER NOT NULL,
        #PRIMARY KEY("UID" AUTOINCREMENT));

except:
    pass

def vacuum_dl():
    vacuums = []
    vacuums_price = []

    hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
    options = webdriver.ChromeOptions
    browser = webdriver.Chrome(os.getcwd() + '\\' + 'chromedriver.exe')
    url = 'https://www.myhenry.com/'
    url_2 = 'https://www.myhenry.com/machines'
    browser.get(url)

    vacuums_sale = browser.find_element_by_xpath('//*[@id="store.menu"]/nav/ul/li[1]/a/span[2]')
    time.sleep(1)
    browser.execute_script("arguments[0].click();", vacuums_sale)
    #Using a 'click' in javascript rather than traditional selenium button click.

    browser_1 = browser.current_url
    browser.get(browser_1)

    parser = soup(browser.page_source, 'html.parser')
    with open('Url_text.txt', 'w') as p:
        p.write(parser.get_text())
    #grabbing and writing text of the website

    html_writer = parser.prettify()
    with open('html.txt', 'w') as f:
        f.write(html_writer)

    henry_vac = parser.find_all("div", class_="product details product-item-details ")
    #tp_test = parser.find('//*[@id="star-score-3"]').text
    #print(tp_test)

    skus = parser.find('div', class_='products wrapper grid products-grid')
    all_henrys = skus.find_all('a', class_='product-item-link')
    all_henrys_price = skus.find_all('span', class_='price')
    for henrys in all_henrys:
        name = henrys.text
        name_1 = name.replace(' ','') #remove spaces
        name_2 = re.sub(r'\t', '', name_1) #remove tabs
        new_string = re.sub(r'\n', '', name_2) #remove new lines
        vacuums.append(new_string)

    for henrys_price in all_henrys_price:
        name = henrys_price.text
        vacuums_price.append(name)

    print(vacuums)
    print(vacuums_price)

    for i in range(len(vacuums)):
        cur.execute('INSERT INTO Vaccums (Name, Price) VALUES (?,?)',(vacuums[i],vacuums_price[i]))
        conn.commit()

    conn.close()


vacuum_dl()