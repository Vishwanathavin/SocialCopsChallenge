import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./data/Monthly_data_cmo.csv')

APMC='Ahmednagar'
commodity='BAJRI'

data.Commodity = data.Commodity.astype(str).apply(lambda x: x.upper())

data = data[(data['Commodity']==commodity) & (data['APMC']==APMC)]

data['date'] = pd.to_datetime(data['date'],format="%Y-%m")
data.set_index('date', inplace=True)

data.sort_index(inplace=True)
plt.plot(data['modal_price'])
# plt.show()
interData=data.resample('W').asfreq()
newData=pd.concat([data,interData]).sort_index().interpolate('time')

# print(pd.date_range(start=data.index.min(),end=data.index.max(),freq='w'))
exit()
unsample= data['modal_price'].reindex(pd.date_range(start=data.index.min(),
                                                    end=data.index.max(),
                                                    freq='w'))




data_new=unsample.interpolate('cubic')
# print(data_new)
plt.plot(data_new)
plt.show()