import requests


def getLoginId(mobile, password):
    url = 'https://mapp30.cmfchina.com/appweb/user/login'
    data = {
        'loginNo': mobile,
        "loginPassword": password
    }
    response = requests.post(url=url, data=data).json()
    loginId = response.get('loginId')
    if loginId:
        return loginId
    else:
        print('logid为空')


def getLastNav(mobile, password, fundId, index):
    loginId = getLoginId(mobile, password)
    url = 'https://common.cmfchina.com/commonweb/fund/getNavList?loginId={}&fundId={}'.format(
        loginId, fundId)
    response = requests.post(url).json()
    # 根据角标查出最近一天的净值
    lastNav = response.get('navList')[index].get('nav')
    navdt = response.get('navList')[index].get('navdt')
    # 货币基金没有返回nav
    if lastNav == '':
        lastNav = '1.0'
    return lastNav, navdt


def cleanData(data):
    str_data = str(data)
    integer, decimal = str_data.split('.')
    list_decimal = list(decimal)
    if data < 0:
        if len(list_decimal) > 2:
            list_decimal[1] = str(int(list_decimal[1]) + 1)
            str_decimal = ''.join(list_decimal)[:2]
            cleandata = integer + '.' + str_decimal
            return cleandata
        else:
            return str_data
    if data > 0:
        l = list_decimal[:2]
        str_decimal = ''.join(l)
        cleandata = integer + '.' + str_decimal
        return cleandata
    else:
        return str_data


def queryFundAssetGroupByFundId(mobile, password):
    loginId = getLoginId(mobile, password)
    url = 'https://common.cmfchina.com/commonweb/fundAssert/fund/queryFundAssetGroupByFundId?loginId={}'.format(loginId)
    response = requests.post(url).json()
    sumProFit = 0
    for fundBalance in response.get('fundBalanceList'):
        nav = float(fundBalance.get('nav'))
        navdate = fundBalance.get('navdate')
        fundId = fundBalance.get('fundid')
        mergeList = fundBalance.get('mergeList')
        sumAvailableBanavdatel = 0
        lastNav, lastNavDt = getLastNav(mobile, password, fundId, index=1)
        # 存在多个交易账户
        for merge in mergeList:
            lastDayEarnings = float(merge.get('lastDayEarnings').replace(',', ''))
            # 可用份额
            availableBal = float(merge.get('availableBal').replace(',', ''))
            lastNav = float(lastNav)
            profit = (nav - lastNav) * availableBal
            clean_profit = cleanData(profit)
            print("{},{}:净值{},'-',最近一天{}:净值{},'*',份额{},'=',算出来最近一天收益{}"
                  "，处理后{}，接口返回{}".format(fundId, navdate, nav, lastNavDt,
                                       lastNav, availableBal,
                                        profit, clean_profit,lastDayEarnings))
            # 总份额
    #         sumAvailableBal += availableBal
    #     # print('{}:总份额是{}，净值是{},净值日期是{}'.format(fundId, round(sumAvailableBal, 2), nav, navdate))
    #     lastNav, lastNavDt = getLastNav(mobile, password, fundId)
    #     lastNav = float(lastNav)
    #     # print('最近一天的净值是{}，净值日期{}'.format(lastNav, lastNavDt))
    #     profit = (nav - lastNav) * round(sumAvailableBal, 2)
    #     #     # profit = round(profit, 2)
    #     sumProFit += profit
    #     # print('最近一天收益{}'.format(profit))
    #     print("{},净值{},'-',最近一天净值{},'*',总份额{},'=',最近一天收益{}".format(fundId, nav, lastNav, round(sumAvailableBal, 2),
    #                                                                profit))
    # print('最近一天总收益{}'.format(sumProFit))


if __name__ == '__main__':
    queryFundAssetGroupByFundId('18323579392', '1111112')
