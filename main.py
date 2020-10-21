import requests
import re
import json

CODE_LIST = ["005276"]

class FundHistoryValue:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.historyValueList = []

    def append(self, date, value):
        self.historyValueList.append((date, value))

    def __str__(self):
        strValue = "代码: {0}, 名称: {1}, 净值列表:[\n".format(self.code, self.name)

        for value in self.historyValueList:
            strValue += "\t日期: {0}, 净值: {1}\n".format(value[0], value[1])
        strValue += "]\n"

        return strValue


class FundEstimatedValue:
    def __init__(self, code, name, value, increasePercentage):
        self.code = code
        self.name = name
        self.value = value
        self.increasePercentage = increasePercentage

    def __str__(self):
        return "代码: {0}, 名称: {1}, 净值估算: {2}, 估算涨幅: {3}%".format(self.code, self.name, self.value, self.increasePercentage)


def getFundEstimatedValue(code):
    req = "http://fundgz.1234567.com.cn/js/{}.js?rt=1463558676006".format(code)
    resp = requests.get(req)

    pattern = r'^jsonpgz\((.*)\)'
    search = re.findall(pattern, resp.text)

    for i in search:
        data = json.loads(i)
        value = FundEstimatedValue(code, data['name'], data['gsz'], data['gszzl'])
        return value


def getFundHistoryValue(code, name):
    code = '005276'
    pageIndex = 1
    url = 'http://api.fund.eastmoney.com/f10/lsjz'

    # 参数化访问链接，以dict方式存储
    params = {
        'callback': 'jQuery18307633215694564663_1548321266367',
        'fundCode': code,
        'pageIndex': pageIndex,
        'pageSize': 20,
    }
    # 存储cookie内容
    cookie = 'EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=01-24 17:11:50@#$%u957F%u4FE1%u5229%u5E7F%u6DF7%u5408A@%23%24519961; st_pvi=27838598767214; st_si=11887649835514'
    # 装饰头文件
    headers = {
        'Cookie': cookie,
        'Host': 'api.fund.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Referer': 'http://fundf10.eastmoney.com/jjjz_%s.html' % code,
    }
    r = requests.get(url=url, headers=headers, params=params)  # 发送请求

    text = re.findall('\((.*?)\)', r.text)[0]  # 提取dict
    LSJZList = json.loads(text)['Data']['LSJZList']  # 获取历史净值数据
    TotalCount = json.loads(text)['TotalCount']  # 转化为dict

    historyValue = FundHistoryValue(code, name)

    for i in LSJZList:
        historyValue.append(i["FSRQ"], i["LJJZ"])

    return historyValue


def main():
    for code in CODE_LIST:
        estimatedValue = getFundEstimatedValue(code)
        print(estimatedValue)
        print("\n")
        
        historyValue = getFundHistoryValue(code, estimatedValue.name)
        print(historyValue)


main()
