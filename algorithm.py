import pandas as pd
from dataClass import cAPMC,removeOutlier,interpolateData
from statsmodels.tsa import seasonal, stattools

def main():
    APMCdata = cAPMC(pd.read_csv('./data/Monthly_data_cmo.csv'))

    APMCdata.groupData()

    flucData = pd.DataFrame()
    for data in APMCdata.groupList:
        data = stationarity(data)
        flucData = pd.concat([flucData,data[['fluc'] + ['APMC'] + ['Commodity']]], axis=0)

    flucData=flucData.reset_index()
    flucData.to_csv('./data/flucData.csv',index=False)

def stationarity(data):
    data=pd.DataFrame(data)
    data.set_index('date',inplace=True)
    data = removeOutlier(data)
    data= interpolateData(data)

    try:
        decompData = seasonal.seasonal_decompose(data['modal_price'], model='multiplicative', freq=4)
        # Multiply the trend and residue to get the de-seasonalized value
        data['deSeasonalized'] = decompData.resid * decompData.trend
        data['fluc'] = data['deSeasonalized'].diff()

        data=data.to_dict('records')
        return data
        # flucData = pd.concat([flucData, APMCdata.curData[['fluc'] + ['APMC'] + ['Commodity']]], axis=0)
    except:
        pass


if __name__=='__main__':
    main()