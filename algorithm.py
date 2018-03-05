import pandas as pd
from dataClass import cAPMC,removeOutlier,interpolateData,cMSP,extrapolateData
from statsmodels.tsa import seasonal

def main():

    APMCdata,MSPdata=readInput()
    APMCdata.groupData()
    MSPdata.groupData()
    flucData = getFluctuation(APMCdata.groupList,MSPdata.groupList)
    flucData=flucData.reset_index()
    flucData.to_csv('./data/flucData.csv',index=False)
def readInput():
    APMCdata = cAPMC(pd.read_csv('./data/Monthly_data_cmo.csv'))
    MSPdata = cMSP(pd.read_csv('./data/CMO_MSP_Mandi.csv'))
    return APMCdata,MSPdata
def getFluctuation(APMCgroupList,MSPgroupList):
    #Calculating the fluctuation for each APMC and Commodity
    print("Calculating the fluctuation for each APMC and Commodity")
    flucData = pd.DataFrame()
    for APMCdata in APMCgroupList:
        for commodityData in APMCdata['commodityList']:
            mspData = [data for data in MSPgroupList if data['Name'] == commodityData['Name']]
            if len(mspData)>0:
                data = stationarity(commodityData['salesList'],mspData[0]['salesList'])
            else:
                data = stationarity(commodityData['salesList'])

            try:
                # data['fluc']=data['deSeasonalized'].diff()
                data['Commodity']=commodityData['Name']
                data['APMC']=APMCdata['Name']
                flucData = pd.concat([flucData, data[['date']+['fluc'] + ['APMC'] + ['Commodity']+['diff']]], axis=0)
            except:
                continue
    return flucData


def stationarity(data,mspdata=None):
    data=pd.DataFrame(data)

    data.set_index('date',inplace=True)
    data = removeOutlier(data)
    data= interpolateData(data)
    if mspdata:
        mspdata = pd.DataFrame(mspdata)
        mspdata.set_index('date', inplace=True)
        mspdata=extrapolateData(mspdata,data.index)

    try:
        decompData = seasonal.seasonal_decompose(data['modal_price'], model='multiplicative', freq=4)
        # Multiply the trend and residue to get the de-seasonalized value
        data['deSeasonalized'] = decompData.resid * decompData.trend
        data['fluc'] = data['deSeasonalized'].diff()
        if mspdata.shape[0]:
            data['diff']=data['deSeasonalized']-mspdata['price']
        data.reset_index(inplace=True)

        return data
        # flucData = pd.concat([flucData, APMCdata.curData[['fluc'] + ['APMC'] + ['Commodity']]], axis=0)
    except:
        pass


if __name__=='__main__':
    main()