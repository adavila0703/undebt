from selenium import webdriver
import time
import sqlite3
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
import random
import dateutil.parser
from datetime import datetime


def no_space(name):
    new_str = name.replace(' ', '.')
    return new_str


def real_key(driver, str_in):
    for s in str_in:
        driver.send_keys(s)
        time.sleep(random.uniform(0.005, 0.1))
    return None


def random_sleep():
    time.sleep(random.uniform(0.8, 1.5))


def date_fix(date):
    newdate = dateutil.parser.parse(date)
    date_object = datetime.strptime(str(newdate), '%Y-%m-%d  %H:%M:%S')
    date_out = date_object.strftime('%m-%d-%Y')
    return date_out


def day_calc(date):
    newdate = dateutil.parser.parse(date)
    date_object = datetime.strptime(str(newdate), '%Y-%m-%d  %H:%M:%S')
    days = date_object - datetime.now()
    return days.days


def my_cc():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
        "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get('')
    time.sleep(5)

    iframe = chrome.find_element_by_id('syf_login_iframe')
    chrome.switch_to.frame(iframe)
    username = chrome.find_element_by_id('LoginusernameId')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (3,))
    real_key(username, query.fetchone()[2])
    random_sleep()
    password = chrome.find_element_by_id('LoginpasswordId')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (3,))
    real_key(password, query.fetchone()[3])
    random_sleep()
    chrome.find_element_by_xpath('//*[@id="loginSubmit"]').click()
    time.sleep(5)

    if chrome.find_element_by_xpath('//*[@id="login_challenge_user"]/div[2]/div/div/label').text \
            == 'In what city was your high school? (full name of city only)':
        answer = chrome.find_element_by_id('securityAns')
        query = cursor.execute('SELECT * FROM passwords WHERE id=?', (3,))
        real_key(answer, query.fetchone()[4])
    elif chrome.find_element_by_xpath('//*[@id="login_challenge_user"]/div[2]/div/div/label').text \
            == 'What was the name of your first girlfriend/boyfriend?':
        answer = chrome.find_element_by_id('securityAns')
        query = cursor.execute('SELECT * FROM passwords WHERE id=?', (3,))
        real_key(answer, query.fetchone()[5])
    elif chrome.find_element_by_xpath('//*[@id="login_challenge_user"]/div[2]/div/div/label').text \
            == 'What was the name of your junior high school? (Enter only "Riverdale" for Riverdale Junior High School)':
        answer = chrome.find_element_by_id('securityAns')
        query = cursor.execute('SELECT * FROM passwords WHERE id=?', (3,))
        real_key(answer, query.fetchone()[6])
    else:
        pass

    time.sleep(5)
    chrome.find_element_by_xpath('//*[@id="remindme"]').click()
    time.sleep(2)

    balance = chrome.find_element_by_xpath(
        '//*[@id="homePageForm"]/div/div/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[1]/h2')
    min_payment = chrome.find_element_by_xpath(
        '//*[@id="homePageForm"]/div/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/h2')
    due_date = chrome.find_element_by_xpath(
        '//*[@id="homePageForm"]/div/div/div/div[2]/div[3]/div/div/div[2]/b[2]')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '').replace('*', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '').replace('*', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           3))
    connection.commit()
    connection.close()

    chrome.close()

    return None


def american_airlines():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    #     "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
    #     "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get('')
    time.sleep(5)

    iframe = chrome.find_element_by_id('logonbox')
    chrome.switch_to.frame(iframe)
    random_sleep()

    username = chrome.find_element_by_id('userId-text-input-field')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (4,))
    real_key(username, query.fetchone()[2])
    random_sleep()
    password = chrome.find_element_by_id('password-text-input-field')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (4,))
    real_key(password, query.fetchone()[3])
    random_sleep()
    chrome.find_element_by_xpath('//*[@id="signin-button"]/span').click()
    time.sleep(10)

    balance = chrome.find_element_by_xpath(
        '//*[@id="accountCurrentBalanceLinkWithReconFlyoutValue"]')
    min_payment = chrome.find_element_by_xpath(
        '//*[@id="minimumAmountDueLinkChicklet"]/span')
    due_date = chrome.find_element_by_xpath(
        '//*[@id="cardNextPaymentDueDateChicklet"]/span')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           4))
    connection.commit()
    connection.close()

    chrome.close()
    return None


def chase():
    options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    driver.get('')

    time.sleep(2)
    iframe = driver.find_element_by_id('logonbox')
    driver.switch_to.frame(iframe)
    user = driver.find_element_by_id('userId-text-input-field')
    user.send_keys('')
    password = driver.find_element_by_id('password-text-input-field')
    password.send_keys('')
    password.submit()
    time.sleep(10)

    balance = driver.find_element_by_class_name(no_space('CRNTBAL current-balance-value'))
    min_payment = driver.find_element_by_id('minimumAmountDueLinkChicklet')
    due_date = driver.find_element_by_id('cardNextPaymentDueDateChicklet')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           5))
    connection.commit()
    connection.close()

    driver.close()
    return None


def fire_stone():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
        "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get(
        'https://www.cfna.com/')
    # agent = chrome.execute_script('return navigator.userAgent')
    # print(agent)

    time.sleep(4)
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (6,))
    chrome.find_element_by_class_name('form-control.clearable').click()
    username = chrome.find_element_by_class_name('form-control.clearable')
    real_key(username, query.fetchone()[2])  # username
    random_sleep()
    username.submit()

    time.sleep(2)
    question = chrome.find_element_by_xpath('//*[@id="authValidationFrm"]/div[1]/div/div[1]/p/strong')
    if question.text == "What is your father's middle name?":
        query = cursor.execute('SELECT * FROM passwords WHERE id=?', (6,))
        answer = chrome.find_element_by_id('auth-answer')
        real_key(answer, query.fetchone()[6])
        random_sleep()
        answer.submit()
    elif question.text == "What is the name of your favorite sports team?":
        query = cursor.execute('SELECT * FROM passwords WHERE id=?', (6,))
        answer = chrome.find_element_by_id('auth-answer')
        real_key(answer, query.fetchone()[5])
        random_sleep()
        answer.submit()
    elif question.text == "What was your first car?":
        query = cursor.execute('SELECT * FROM passwords WHERE id=?', (6,))
        answer = chrome.find_element_by_id('auth-answer')
        real_key(answer, query.fetchone()[4])
        random_sleep()
        answer.submit()

    time.sleep(2)
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (6,))
    password = chrome.find_element_by_id('password')
    real_key(password, query.fetchone()[3])
    random_sleep()
    password.submit()

    login_info.close()

    balance = chrome.find_element_by_xpath(
        '//*[@id="account-summary-outstanding"]/div[1]/span/strong')
    min_payment = chrome.find_element_by_xpath(
        '//*[@id="account-summary-outstanding"]/div[2]/span/strong')
    due_date = chrome.find_element_by_xpath(
        '//*[@id="account-summary-outstanding"]/div[3]/span/strong')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           6))
    connection.commit()
    connection.close()

    chrome.close()

    return None


def best_buy():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
        "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get(
        'https://citiretailservices.citibankonline.com/RSnextgen/svc/launch/index.action?siteId=PLCN_BESTBUY#signon')
    # agent = chrome.execute_script('return navigator.userAgent')
    # print(agent)

    time.sleep(4)
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (2,))
    try:
        chrome.find_element_by_id('user_id_19').click()
        user = chrome.find_element_by_id('user_id_19')
        random_sleep()
    except NoSuchElementException:
        chrome.find_element_by_id('user_id_2').click()
        user = chrome.find_element_by_id('user_id_2')
        random_sleep()
    real_key(user, query.fetchone()[2])  # username
    random_sleep()

    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (2,))
    try:
        chrome.find_element_by_id('password_20').click()
        password = chrome.find_element_by_id('password_20')
        random_sleep()
    except NoSuchElementException:
        chrome.find_element_by_id('password_3').click()
        password = chrome.find_element_by_id('password_3')
        random_sleep()
    real_key(password, query.fetchone()[3])  # password
    login_info.close()
    random_sleep()
    chrome.find_element_by_xpath('//*[@id="maincontent"]/section[2]/section[2]/section/article/form/button').click()
    time.sleep(10)

    balance = chrome.find_element_by_xpath(
        '//*[@id="maincontent"]/section[2]/section[1]/article[1]/div[1]/dl[2]/dd[1]')
    min_payment = chrome.find_element_by_xpath(
        '//*[@id="maincontent"]/section[2]/section[1]/article[1]/div[1]/dl[1]/dd[1]')
    due_date = chrome.find_element_by_xpath(
        '//*[@id="maincontent"]/section[2]/section[1]/article[1]/div[1]/dl[1]/dd[2]')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           2))
    connection.commit()
    connection.close()

    chrome.close()

    return None


def wells_fargo():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    #     "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
    #     "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get('')
    time.sleep(5)

    username = chrome.find_element_by_id('userid')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (12,))
    real_key(username, query.fetchone()[2])
    random_sleep()
    password = chrome.find_element_by_id('password')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (12,))
    real_key(password, query.fetchone()[3])
    random_sleep()
    password.submit()
    time.sleep(5)
    chrome.find_element_by_xpath('/html/body/div[2]/section/div[1]/div[3]/div[1]/div/div[1]/a[1]/span[1]').click()
    time.sleep(10)

    balance = chrome.find_element_by_xpath(
        '/html/body/div[2]/section/div[1]/div[1]/div[6]/table/tbody/tr[6]/td/span')
    min_payment = chrome.find_element_by_xpath(
        '/html/body/div[2]/section/div[1]/div[1]/div[6]/table/tbody/tr[2]/td/strong/span')
    due_date = chrome.find_element_by_xpath(
        '/html/body/div[2]/section/div[1]/div[1]/div[6]/table/tbody/tr[2]/th/strong')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text.split()[4].replace(')', '')),
                           time.ctime(),
                           day_calc(due_date.text.split()[4].replace(')', '')),
                           12))
    connection.commit()
    connection.close()

    chrome.close()

    return None


def paypal():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    #     "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
    #     "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get('')
    time.sleep(5)

    try:
        chrome.find_element_by_class_name('headerText')
        chrome.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[1]').click()
        time.sleep(5)
    except:
        pass

    username = chrome.find_element_by_id('email')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (10,))
    real_key(username, query.fetchone()[2])
    username.submit()
    time.sleep(5)
    password = chrome.find_element_by_id('password')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (10,))
    real_key(password, query.fetchone()[3])
    random_sleep()
    password.submit()
    time.sleep(5)
    chrome.find_element_by_xpath('//*[@id="A"]/div/div[4]/div/h3/a').click()
    time.sleep(15)

    balance = chrome.find_element_by_xpath(
        '//*[@id="main-content-area"]/div/div/div/div[1]/div[1]/p[2]')
    min_payment = chrome.find_element_by_xpath(
        '//*[@id="main-content-area"]/div/div/div/div[1]/div[2]/div[2]/span')
    due_date = chrome.find_element_by_xpath(
        '//*[@id="main-content-area"]/div/div/div/div[1]/div[3]/p[3]')

    try:
        chrome.find_element_by_xpath('//*[@id="UpdateATPAction"]/div[4]/a[3]').click()
        time.sleep(5)
    except:
        pass

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           10))
    connection.commit()
    connection.close()

    chrome.close()

    return None


def express():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    #     "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
    #     "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get('')
    time.sleep(5)

    try:
        chrome.find_element_by_class_name('headerText')
        chrome.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[1]').click()
        time.sleep(5)
    except:
        pass

    username = chrome.find_element_by_id('email')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (11,))
    real_key(username, query.fetchone()[2])
    username.submit()
    time.sleep(5)
    password = chrome.find_element_by_id('password')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (11,))
    real_key(password, query.fetchone()[3])
    random_sleep()
    password.submit()
    time.sleep(10)
    chrome.find_element_by_xpath('//*[@id="A"]/div/div[4]/div/h3/a').click()
    time.sleep(15)

    try:
        chrome.find_element_by_xpath('//*[@id="UpdateATPAction"]/div[4]/a[3]').click()
        time.sleep(5)
    except:
        pass

    balance = chrome.find_element_by_xpath(
        '//*[@id="main-content-area"]/div/div/div/div[1]/div[1]/p[2]')
    min_payment = chrome.find_element_by_xpath(
        '//*[@id="main-content-area"]/div/div/div/div[1]/div[2]/div[2]/span')
    due_date = chrome.find_element_by_xpath(
        '//*[@id="main-content-area"]/div/div/div/div[1]/div[3]/p[3]')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           11))
    connection.commit()
    connection.close()

    chrome.close()

    return None


def book_store():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
        "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get('')
    time.sleep(5)

    chrome.find_element_by_id('signin_user_email').click()
    random_sleep()
    username = chrome.find_element_by_id('signin_user_email')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (7,))
    real_key(username, query.fetchone()[2])
    random_sleep()
    chrome.find_element_by_id('signin_user_password').click()
    random_sleep()
    password = chrome.find_element_by_id('signin_user_password')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (7,))
    real_key(password, query.fetchone()[3])
    time.sleep(1)
    iframe = chrome.find_element_by_xpath('//*[@id="new_signin_user"]/div/fieldset/ul[3]/li/div/div/div/div/div/iframe')
    chrome.switch_to.frame(iframe)
    chrome.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[1]').click()
    random_sleep()
    iframe = chrome.find_element_by_id('destination_publishing_iframe_cnuonlineholdings_0')
    chrome.switch_to.frame(iframe)
    chrome.find_element_by_xpath('//*[@id="new_signin_user"]/div/fieldset/div[2]/input').click()
    time.sleep(15)

    balance = chrome.find_element_by_xpath(
        '//*[@id="account-summary"]/div[2]/div[1]/table/tbody/tr[5]/td[2]/span')
    min_payment = chrome.find_element_by_xpath(
        '//*[@id="account-summary"]/div[2]/div[1]/table/tbody/tr[8]/td[2]/span')
    due_date = chrome.find_element_by_xpath(
        '//*[@id="account-summary"]/div[2]/div[1]/table/tbody/tr[7]/td[2]/span')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           7))
    connection.commit()
    connection.close()

    chrome.close()

    return None


def macys():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    #     "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
    #     "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get('https://www.macys.com/account/signin?lid=sign_in&cm_sp=macys_account-_-macys_credit_card-_-sign_in')
    time.sleep(5)

    try:
        chrome.find_element_by_class_name('headerText')
        chrome.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[1]').click()
        time.sleep(5)
    except:
        pass

    username = chrome.find_element_by_id('email')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (11,))
    real_key(username, query.fetchone()[2])
    username.submit()
    time.sleep(5)
    password = chrome.find_element_by_id('password')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (11,))
    real_key(password, query.fetchone()[3])
    random_sleep()
    password.submit()
    time.sleep(5)
    chrome.find_element_by_xpath('//*[@id="A"]/div/div[4]/div/h3/a').click()
    time.sleep(15)

    try:
        chrome.find_element_by_xpath('//*[@id="UpdateATPAction"]/div[4]/a[3]').click()
        time.sleep(5)
    except:
        pass

    balance = chrome.find_element_by_xpath(
        '//*[@id="main-content-area"]/div/div/div/div[1]/div[1]/p[2]')
    min_payment = chrome.find_element_by_xpath(
        '//*[@id="main-content-area"]/div/div/div/div[1]/div[2]/div[2]/span')
    due_date = chrome.find_element_by_xpath(
        '//*[@id="main-content-area"]/div/div/div/div[1]/div[3]/p[3]')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           11))
    connection.commit()
    connection.close()

    chrome.close()

    return None


def clothes_store():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    #     "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
    #     "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get('')
    time.sleep(5)

    username = chrome.find_element_by_id('onlineId1')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (1,))
    real_key(username, query.fetchone()[2])
    random_sleep()
    password = chrome.find_element_by_id('passcode1')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (1,))
    real_key(password, query.fetchone()[3])
    random_sleep()
    password.submit()
    time.sleep(15)

    balance = chrome.find_element_by_xpath(
        '//*[@id="Traditional"]/li/div[1]/div/span')
    min_payment = chrome.find_element_by_xpath(
        '//*[@id="summary-info"]/div[3]/div[3]/div[2]/strong')
    due_date = chrome.find_element_by_xpath(
        '//*[@id="summary-info"]/div[3]/div[2]/div[2]/strong')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           1))
    connection.commit()
    connection.close()

    chrome.close()

    return None


def grocery_store():
    login_info = sqlite3.connect('data.db')
    cursor = login_info.cursor()

    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    #     "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,"
    #     "8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
    chrome = uc.Chrome(options=options)
    chrome.get('')
    time.sleep(5)

    username = chrome.find_element_by_id('txtUsername')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (14,))
    real_key(username, query.fetchone()[2])
    random_sleep()
    password = chrome.find_element_by_id('txtPassword')
    query = cursor.execute('SELECT * FROM passwords WHERE id=?', (14,))
    real_key(password, query.fetchone()[3])
    random_sleep()
    chrome.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnLogin"]').click()
    time.sleep(10)
    chrome.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ucAccountNav_lnkCharge"]').click()
    time.sleep(2)

    balance = chrome.find_element_by_xpath(
        '//*[@id="charge_details"]/div[2]/div[1]')
    min_payment = chrome.find_element_by_xpath(
        '//*[@id="ctl00_ContentPlaceHolder1_divPaymentDueInfo"]/div[4]')
    due_date = chrome.find_element_by_xpath(
        '//*[@id="ctl00_ContentPlaceHolder1_divPaymentDueInfo"]/div[2]')

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'UPDATE masterdata SET balance = ?, min_payment = ?, due_date = ?, last_update = ?, days = ? WHERE id = ?'

    cursor.execute(query, (float(str(balance.text).split('$')[1].replace(',', '')),
                           float(str(min_payment.text).split('$')[1].replace(',', '')),
                           date_fix(due_date.text),
                           time.ctime(),
                           day_calc(due_date.text),
                           14))
    connection.commit()
    connection.close()

    chrome.close()

    return None
