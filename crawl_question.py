import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import crawl_class

headers = {
    "Host": "www.zhihu.com",
    "Referer" : "https://www.zhihu.com",
    'X-Requested-With' : 'XMLHttpRequest',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}


def store_dict_in_json(info_dict, file_name):
    with open(file_name, 'wb') as json_file:
        json_file.write(json.dumps(info_dict,ensure_ascii=False).encode('utf-8'))


def store_list_in_json(info_list, file_name):
    with open(file_name, 'wb') as json_file:
        for info in info_list:
            json_file.write(json.dumps(info,ensure_ascii=False).encode('utf-8'))
            json_file.write('\n'.encode('utf-8'))


def load_web_page(url):
    """
    1.load the web page until the page is at the end
    2.load the complex question text
    """
    driver = webdriver.PhantomJS(executable_path=r"E:/phantomjs/bin/phantomjs.exe")
    driver.implicitly_wait(10)
    driver.get(url)

    # load the question text
    try:
        click_btn = driver.find_element_by_xpath('//button[@class="Button QuestionRichText-more Button--plain"]')
        ActionChains(driver).click(click_btn).perform()      
        time.sleep(0.5)
        html_text = driver.page_source
    except:
        html_text = driver.page_source

    # load page
    while(True):
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(0.8)
        if(html_text == driver.page_source):
            break
        html_text = driver.page_source

    # time.sleep(1)
    # html_text = driver.page_source

    driver.quit()

    return html_text


def analyse_question_page(url):
    """
    1.analyse the web page
    2.crawl the infomation
    """
    html_text = load_web_page(url)
    soup = BeautifulSoup(html_text, "html.parser")

    # crawl the question info
    question_dict = {}
    question_dict['question_id'] = url[-8:]

    try:
        question_text = soup.select_one('span[class="RichText"]').get_text()
        question_dict['question_text'] = question_text
    except:
        question_dict['question_text'] = ''
    # print(question_text)
    question_title = soup.select_one('h1[class="QuestionHeader-title"]').get_text()
    question_dict['question_title'] = question_title

    question_comment = soup.select_one('button[class="Button Button--plain Button--withIcon Button--withLabel"]').get_text()
    question_dict['question_commet'] = question_comment

    try:
        question_answer_number = soup.select_one('h4[class="List-headerText"]').get_text()
        question_dict['answer_number'] = question_answer_number
    except:
        question_dict['answer_number'] = ''

    question_board_value = soup.select('strong[class="NumberBoard-itemValue"]')
    #print(len(question_board_value))
    question_dict['question_followers'] = question_board_value[0].get_text()
    question_dict['brower_number'] = question_board_value[1].get_text()

    nodes = soup.find_all('div', class_="List-item")
    answer_list = []
    # i = 1
    for node in nodes:
        info_dict = {}
        # print(i)
        # i += 1
        # data_zop = node.find('div', attrs={'data-zop':True}).attrs['data-zop']
        data_zop = node.select_one('div[data-zop]').attrs['data-zop']
        data_zop = json.loads(data_zop)
        info_dict['answer_author'] = data_zop['authorName']
        info_dict['answer_id'] = data_zop['itemId']
        # print(data_zop['itemId'])

        answer_text = node.select_one('span[class="RichText CopyrightRichText-richText"]').get_text()
        info_dict['answer_text'] = answer_text

        answer_votes = node.select_one('button[class="Button VoteButton VoteButton--up"]').get_text()
        info_dict['answer_votes'] = answer_votes

        answer_comment = node.select_one('button[class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"]').get_text()
        info_dict['answer_comment'] = answer_comment
        
        # print(info_dict)
        answer_list.append(info_dict)

    # question_dict['answers'] = answer_list
        
    # return question_dict
    return [question_dict] + answer_list


def crawl_question(url, file_name):
    """
    crawl the answers of the question,and save the result
    """
    question_dict = analyse_question_page(url)
    file_name = file_name +  url[-8:] + '.json'
    # file_name = "F:/python/crawler/zhihu/content/" + url[-8:] + '.json'

    # store_dict_in_json(question_dict, file_name)
    store_list_in_json(question_dict, file_name)


if __name__ == '__main__':
    # url = 'https://www.zhihu.com/question/21378038'
    # url = 'https://www.zhihu.com/question/31496472'
    url = 'https://www.zhihu.com/question/30891234'
    # url = 'https://www.zhihu.com/question/62968639'
    # url = 'https://www.zhihu.com/question/26410728'

    crawl_question(url)

