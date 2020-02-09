from bs4 import BeautifulSoup
import time
import datetime
import requests
import json
import os

sahibinden_url = "http://www.sahibinden.com"
search_url = os.environ['SEARCH_URL']

PREVIOUS_FOUNDED_HOUSES = []


def get_website_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'searchResultsTable'})
    if not table:
        return

    search_results_items = table.findAll('tr')
    search_results_items.pop(0)
    if len(search_results_items) >= 1:
        for search_results_item in search_results_items:
            parse_page(search_results_item)


def parse_page(search_results_item):

    td = search_results_item.find(
        'td', {'class': 'searchResultsTitleValue leafContent'})
    if td:
        link = td.find('a', {'class': 'classifiedTitle'})['href']
        search_result = "{0}/{1}".format(sahibinden_url, link)
        if search_result in PREVIOUS_FOUNDED_HOUSES:
            print('{0} already in list.'.format(search_result))
        else:
            send_slack_notification(search_result)
            print(search_result)
            PREVIOUS_FOUNDED_HOUSES.append(search_result)


def main():
    get_website_data(search_url)


def send_slack_notification(link):
    webhook_url = os.environ['SLACK_WEBHOOK_URL']
    notification = "{0}".format(link)
    slack_data = {'text': notification, 'username': 'scarlett'}
    response = requests.post(webhook_url, data=json.dumps(
        slack_data), headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        raise ValueError('Request to slack returned an error %s, the response is:\n%s' % (
            response.status_code, response.text))


if __name__ == "__main__":
    while True:
        print("[INFO] {} requesting web page.".format(datetime.datetime.now()))
        main()
        print("[INFO] {} request completed.".format(datetime.datetime.now()))
        time.sleep(60 * 30)
