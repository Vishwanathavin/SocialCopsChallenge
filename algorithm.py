import pandas as pd
from dataClass import cAPMC,removeOutlier,interpolateData
from statsmodels.tsa import seasonal

def main():

    APMCdata=readInput()
    APMCdata.groupData()
    flucData = getFluctuation(APMCdata.groupList)
    flucData=flucData.reset_index()
    flucData.to_csv('./data/flucData.csv',index=False)
def readInput():
    APMCdata = cAPMC(pd.read_csv('./data/Monthly_data_cmo.csv'))
    return APMCdata
def getFluctuation(groupList):

    flucData = pd.DataFrame()
    for APMCdata in groupList:
        for commodityData in APMCdata['commodityList']:
            data = stationarity(commodityData['salesList'])
            try:
                data['fluc']=data['deSeasonalized'].diff()
                data['Commodity']=commodityData['Name']
                data['APMC']=APMCdata['Name']
                flucData = pd.concat([flucData, data[['date']+['fluc'] + ['APMC'] + ['Commodity']]], axis=0)
            except:
                continue
    return flucData


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
        data.reset_index(inplace=True)

        return data
        # flucData = pd.concat([flucData, APMCdata.curData[['fluc'] + ['APMC'] + ['Commodity']]], axis=0)
    except:
        pass


if __name__=='__main__':
    main()