import pandas as pd
# # import numpy as np
from statsmodels.tsa import seasonal, stattools
import matplotlib.pyplot as plt

stdMul = 2

class cAPMC:
    def __init__(self,data):
        self.data=data
        self.treatData()
        self.uniqueAPMC = self.data['APMC'].unique()
        self.uniqueCommodity = self.data['Commodity'].unique()

    def treatData(self):
        self.data['date'] = pd.to_datetime(self.data['date'], format="%Y-%m")
        self.data.Commodity = self.data.Commodity.astype(str).apply(lambda x: x.upper())
        self.data.APMC = self.data.APMC.astype(str).apply(lambda x: x.upper())

    def setCurrent(self,APMC,commodity):
        self.curData = self.data[(self.data['Commodity'] == commodity) & (self.data['APMC'] == APMC)]
        self.curData.set_index('date', inplace=True)
        self.curData.sort_index(inplace=True)

    def interpolateData(self):
        interData = self.curData.resample('W').asfreq()
        self.curData = pd.concat([self.curData, interData]).sort_index().interpolate('time')

    def removeOutlier(self):
        self.curData = self.curData[~((self.curData['modal_price'] - self.curData['modal_price'].mean()).abs() > stdMul * self.curData['modal_price'].std())]
        self.curData = self.curData[self.curData['modal_price'].notnull()]

    def plotcurData(self,column):
        plt.plot(self.curData[column])

class cMSP:
    def __init__(self,data):
        self.data=data
        self.treatData()

    def treatData(self):
        self.data['year'] = pd.to_datetime(self.data['year'], format="%Y")
        self.data.commodity = self.data.commodity.astype(str).apply(lambda x: x.upper())

    def setCurrent(self, commodity):
        self.curData = self.data[(self.data['commodity'] == commodity)]
        self.curData.set_index('year', inplace=True)
        self.curData.sort_index(inplace=True)
        self.inflationBaseYear = self.curData.index.max()
    def plotcurData(self,column):
        plt.plot(self.curData[column])

    def extrapolateData(self,APMCindex):

        interData=self.curData.reindex(pd.date_range(start=self.curData.index.min(), end=APMCindex.max(), freq='w'))

        # self.curData = pd.concat([self.curData, interData]).interpolate(method='spline', order=2)
        self.curData = pd.concat([self.curData, interData]).sort_index()
        self.curData = self.curData[~self.curData.index.duplicated(keep='first')]
        self.curData = self.curData.interpolate(method='spline', order=2)
        self.curData=self.curData[self.curData.index>APMCindex.min()]

def test_stationarity(timeseries,window_size):
    # Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=window_size)
    rolstd = pd.rolling_std(timeseries, window=window_size)

    # Plot rolling statistics:
    fig = plt.figure(figsize=(12, 8))
    orig = plt.plot(timeseries, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    # Perform Dickey-Fuller test:
    # print 'Results of Dickey-Fuller Test:'
    dftest = stattools.adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    return dfoutput
def main():
    #read input
    APMCdata = cAPMC(pd.read_csv('./data/Monthly_data_cmo.csv'))
    MSPdata = cMSP(pd.read_csv('./data/CMO_MSP_Mandi.csv'))

    flucData=pd.DataFrame()

    for APMC in APMCdata.uniqueAPMC:
        for commodity in APMCdata.uniqueCommodity:

            #set the current sliced data
            APMCdata.setCurrent(APMC,commodity)
            MSPdata.setCurrent(commodity)
            #remove outliers
            APMCdata.removeOutlier()



            # Interpolate the data so that there is a data for every month
            APMCdata.interpolateData()
            #Get the Extrapolated MSP data for all the years.
            MSPdata.extrapolateData(APMCdata.curData.index)
            #Deflate the APMC data
            # WE dont need to do this step since we are using a relative comparison


            #Use seasonal decompose both additive and multiplicative. Find out whichever suits

            # for diff in [30]:
            #     data= APMCdata.curData['modal_price']-APMCdata.curData['modal_price'].shift(diff)
            #
            #     test_stationarity(data,30)

            decompData = seasonal.seasonal_decompose(APMCdata.curData['modal_price'],model='multiplicative', freq=15)

            # decompData.plot()

            # Multiply the trend and residue to get the de-seasonalized value
            APMCdata.curData['deSeasonalized']= decompData.resid*decompData.trend


            #Find the difference with the MSP and store the fluctuation
            APMCdata.curData['fluctuation']=APMCdata.curData['deSeasonalized']-MSPdata.curData['msprice']
            print(APMCdata.curData)
            print(APMCdata.curData.reset_index(level=0, inplace=True))
            # flucData=flucData.append(APMCdata.curData.reset_index(level=0, inplace=True))
            # print(APMCdata.curData['fluctuation'])

            # APMCdata.plotcurData('fluctuation')
            # APMCdata.plotcurData('modal_price')
            # APMCdata.plotcurData('deSeasonalized')
            # MSPdata.plotcurData('msprice')
            # plt.show()
            # Interpolate
            exit()
    # Find the set of APMC and the commodity with the maximum fluctuation
    # DOnt expand the scope

if __name__=="__main__":
    main()