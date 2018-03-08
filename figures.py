import pandas as pd
import requests
import pymongo
from dataClass import removeOutlier,interpolateData,extrapolateData
from statsmodels.tsa import seasonal

import matplotlib.pyplot as plt
# APMCdata = cAPMC(pd.read_csv('./data/Monthly_data_cmo.csv'))
import datetime
# payload = {'APMC': 'AHMEDNAGAR', 'COMMODITY': 'BAJRI'}

APMCData = {
  "Details": {
    "_id": "AHMEDNAGAR",
    "commodityList": [
      {
        "Name": "BAJRI",
        "salesList": [
          {
            "date": "Mon, 01 Sep 2014 00:00:00 GMT",
            "modal_price": 1575.0
          },
          {
            "date": "Sat, 01 Nov 2014 00:00:00 GMT",
            "modal_price": 1629.0
          },
          {
            "date": "Thu, 01 Jan 2015 00:00:00 GMT",
            "modal_price": 1618.0
          },
          {
            "date": "Sun, 01 Feb 2015 00:00:00 GMT",
            "modal_price": 1650.0
          },
          {
            "date": "Sun, 01 Mar 2015 00:00:00 GMT",
            "modal_price": 1525.0
          },
          {
            "date": "Wed, 01 Apr 2015 00:00:00 GMT",
            "modal_price": 1463.0
          },
          {
            "date": "Mon, 01 Jun 2015 00:00:00 GMT",
            "modal_price": 1382.0
          },
          {
            "date": "Wed, 01 Jul 2015 00:00:00 GMT",
            "modal_price": 1578.0
          },
          {
            "date": "Sat, 01 Aug 2015 00:00:00 GMT",
            "modal_price": 1615.0
          },
          {
            "date": "Tue, 01 Sep 2015 00:00:00 GMT",
            "modal_price": 1553.0
          },
          {
            "date": "Thu, 01 Oct 2015 00:00:00 GMT",
            "modal_price": 1543.0
          },
          {
            "date": "Sun, 01 Nov 2015 00:00:00 GMT",
            "modal_price": 1579.0
          },
          {
            "date": "Tue, 01 Dec 2015 00:00:00 GMT",
            "modal_price": 1716.0
          },
          {
            "date": "Fri, 01 Jan 2016 00:00:00 GMT",
            "modal_price": 1612.0
          },
          {
            "date": "Mon, 01 Feb 2016 00:00:00 GMT",
            "modal_price": 1699.0
          },
          {
            "date": "Tue, 01 Mar 2016 00:00:00 GMT",
            "modal_price": 1800.0
          },
          {
            "date": "Fri, 01 Apr 2016 00:00:00 GMT",
            "modal_price": 1875.0
          },
          {
            "date": "Sun, 01 May 2016 00:00:00 GMT",
            "modal_price": 1923.0
          },
          {
            "date": "Wed, 01 Jun 2016 00:00:00 GMT",
            "modal_price": 1959.0
          },
          {
            "date": "Mon, 01 Aug 2016 00:00:00 GMT",
            "modal_price": 1757.0
          },
          {
            "date": "Thu, 01 Sep 2016 00:00:00 GMT",
            "modal_price": 1729.0
          },
          {
            "date": "Sat, 01 Oct 2016 00:00:00 GMT",
            "modal_price": 1415.0
          },
          {
            "date": "Tue, 01 Nov 2016 00:00:00 GMT",
            "modal_price": 1648.0
          }
        ]
      }
    ]
  }
}
MSPData = {'salesList': [{'date': datetime.datetime(2012, 1, 1, 0, 0), 'price': 1175.0}, {'date': datetime.datetime(2013, 1, 1, 0, 0), 'price': 1310.0}, {'date': datetime.datetime(2014, 1, 1, 0, 0), 'price': 1250.0}, {'date': datetime.datetime(2015, 1, 1, 0, 0), 'price': 1275.0}, {'date': datetime.datetime(2016, 1, 1, 0, 0), 'price': 1330.0}], '_id': 'BAJRI', 'Name': 'BAJRI'}
MSPsalesData=MSPData['salesList']
MSPData=pd.DataFrame(MSPsalesData)
MSPData['date']=pd.to_datetime(MSPData['date'])
MSPData.set_index('date',inplace=True)

APMCsalesData=APMCData['Details']['commodityList'][0]['salesList']
APMCdata=pd.DataFrame(APMCsalesData)
APMCdata['date'] = pd.to_datetime(APMCdata['date'])
APMCdata.set_index('date',inplace=True)
APMCoutlierData=removeOutlier(APMCdata)

# plt.plot(APMCdata)
# plt.plot(APMCoutlierData)
APMCInterpolatedData=interpolateData(APMCoutlierData['modal_price'])
# plt.plot(APMCInterpolatedData)
# plt.ylabel('modal price')
# plt.xticks(rotation=90)
# plt.show()
# print (salesData)

MSPExtrapolated=extrapolateData(MSPData['price'],APMCInterpolatedData.index)
# plt.plot(MSPExtrapolated)
# plt.plot(MSPData)
# plt.show()

decompData = seasonal.seasonal_decompose(APMCdata['modal_price'], model='multiplicative', freq=4)
decompData.plot()
plt.show()