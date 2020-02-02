#coding:utf-8

import requests
import time
from notifier import EmailNotifer

TIMER = 60 * 10  #default waiting time as 5 minutes

params = {
    'app': 'finance.gzgold',
    'goldid': 1151,
    'appkey': 48349,
    'sign': '98ec57915ada986182815c60a27b03ac',
    'format': 'json'
}

url = 'http://api.k780.com'

def get_data():
    rsp = requests.get(url, params=params)
    if rsp and rsp.status_code == 200:
        raw = rsp.json()
        if raw['success'] == '1':
            return raw['result']
        else:
            return None
    else:
        return None

def format_data(data):
    """
    To format data into an HTML piece for email sending
    :param data: expecting an dict object, sample like:
      {"goldid":"1151","variety":"USDAAU","varietynm":"工行纸黄金(美元)","last_price":"1571.22","high_price":"1575.88","low_price":"1569.03","buy_price":"1570.32","sell_price":"1572.12","uptime":"2020-01-25 03:59:41"}}
    :return: the html codes
    """
    template = """
    <table>
      <tr>
        <td>种类</td><td>{varietynm}</td>
      </tr>
      <tr>
        <td>最新中间价</td><td>{last_price}</td>
      </tr>
      <tr>
        <td>银行买入价</td><td>{buy_price}</td>
      </tr>
      <tr>
        <td>银行卖出价</td><td>{sell_price}</td>
      </tr>
      <tr>
        <td>最高价</td><td>{high_price}</td>
      </tr>
      <tr>
        <td>最低价</td><td>{low_price}</td>
      </tr>
      <tr>
        <td>更新时间</td><td>{uptime}</td>
      </tr> 
    </table>
    """
    return template.format(**data)

def monitor():
    email = EmailNotifer()
    while True:
        data = get_data()
        msg = format_data(data)
        email.send_mail("黄金报价监控", msg)
        time.sleep(TIMER)
        

if __name__ == "__main__":
    monitor()
