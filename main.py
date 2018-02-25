import pandas as pd
import numpy as np
from statsmodels.tsa import seasonal, stattools
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
# Get details: How to get the number of frequencies
# IT will depend on the seasonality of the each of the item

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
    print 'Results of Dickey-Fuller Test:'
    dftest = stattools.adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print dfoutput
def main():
    # Minimum support price
    basePrice = pd.read_csv('./data/CMO_MSP_Mandi.csv')

    print "Number of unique commodities for which base proce is available"
    # print basePrice['commodity'].unique().shape
    # print basePrice['commodity'].unique()
    basePrice['year'] = pd.to_datetime(basePrice['year'],format="%Y")
    basePrice.commodity = basePrice.commodity.astype(str).apply(lambda x: x.upper())
    basePrice.set_index('year', inplace=True)

    APMCprice =  pd.read_csv('./data/Monthly_data_cmo.csv')

    # Treat the data
    # Convert datatime to the format
    APMCprice['date'] = pd.to_datetime(APMCprice['date'],format="%Y-%m")
    APMCprice.Commodity = APMCprice.Commodity.astype(str).apply(lambda x: x.upper())


    uniqueAPMC = APMCprice['APMC'].unique()

    uniqueCommodity = APMCprice['Commodity'].unique()
    # def movingaverage(interval, window_size, STD):
    #     window= np.ones(int(window_size))/float(window_size)
    #
    #     newVal = np.convolve(interval, window, 'same')
    #     # print newVal
    #     # print (STD*np.std(newVal))
    #     return newVal+(STD*np.std(newVal))

    # uniqueAPMC=['Ahmednagar']
    # uniqueCommodity=['BAJRI']

    #Think through this method

    for APMC in uniqueAPMC:
        for commodity in uniqueCommodity:

            #treat the data
            data = APMCprice[(APMCprice['Commodity']==commodity) & (APMCprice['APMC']==APMC)]

            # Convert into relative data
            # INterpolate to get the intermediate months data


            data.set_index('date', inplace=True)

            data.sort_index(inplace=True)
            # plt.plot(data['modal_price'])

            # https: // machinelearningmastery.com / resample - interpolate - time - series - data - python /
            # data['modal_price']= data['modal_price'].reindex(pd.date_range(start=data.index.min(),
            #                                         end=data.index.max(),
            #                                         freq='D')).interpolate()
            # data = upsample.interpolate(method='linear')
            # print data
            print type(data.index)
            print data.index
            # data['modal_price'] = data['modal_price'].resample('D').interpolate('cubic')

            # print data

            exit()
            data['modal_price'] = removeOutlier(data['modal_price'],3)
            data=data[data['modal_price'].notnull()]
            # plt.plot(data['modal_price'])


            # plt.plot(data['modal_price'])
            # plt.show()

            # plt.plot(data['modal_price'])
            # plt.show()
            # start = data.index[0]
            # print start
            # date_list = [start + relativedelta(months=x) for x in range(0, data.shape[0])]

             # Test stationarity using dickey -fuller test

            # data['first_difference'] = data['modal_price'] - data['modal_price'].shift(1)
            # data['seasonal_first_difference'] = data.first_difference - data.first_difference.shift(12)
            # test_stationarity(data['first_difference'].dropna(inplace=False),4)

            # mod = sm.tsa.statespace.SARIMAX(df.riders, trend='n', order=(0, 1, 0), seasonal_order=(1, 1, 1, 12))



            resultCommodityMul = seasonal.seasonal_decompose(data['modal_price'], model='multiplicative',freq=120)

            # data['deseasonalizedPrice'] = resultCommodityMul.resid* resultCommodityMul.trend

            # specificBasePrice = basePrice[basePrice['commodity'] == commodity]
            # Do a
            #     resultCommodityMul.plot()


                # plt.show()
            # plt.plot(data['modal_price'])
            # plt.show()



            # plt.plot(specificData.index,specificData.modal_price)
            # plt.show()
            # patternStart=4
            # for number,value in enumerate(range(patternStart,specificData.shape[0]),patternStart):
            #
            #     # Dont change here. Do all this only for the seasonal data
            #     print number,specificData.iloc[number]["modal_price"],specificData.iloc[number-patternStart]["modal_price"]
            #     specificData.ix[number,"modal_price"]=specificData.ix[number]["modal_price"] - specificData.ix[number-patternStart]["modal_price"]
            #     print number, specificData.iloc[number]["modal_price"]

            # # Sorting the values in a linear time line
            # Xvalue = specificData['date']
            # Yvalue = specificData['modal_price']
            #
            # outTuple = [y for x, y in sorted(zip(Xvalue, Yvalue))]
            # Xvalue = sorted(Xvalue)
            #
            # Yvalue = [Yval for Yval in outTuple]

            # specificData = specificData[specificData['modal_price'] < movingaverage(specificData['modal_price'],3,2)]

            # Outliers detection
            # YvalueAvg = movingaverage(Yvalue, 3,2)
            #
            #
            # Xnew= []
            # Ynew= []
            #
            # for ii in range(len(Xvalue)):
            #     if Yvalue[ii] < YvalueAvg[ii]:
            #         Xnew.append((Xvalue[ii]))
            #         Ynew.append((Yvalue[ii]))


            # Getting seasonal decomposition

            # Detect seasonality (How?)using multiplicity # Filter outliers all in one
            # Understand the freq and filter term
            # resultCommodityAdd = seasonal_decompose(specificData['modal_price'], model='additive',freq=4)
            # Let the frequency be a variable
            # resultCommodityMul = seasonal_decompose(specificData['modal_price'], model='multiplicative',freq=4)
            #
            #
            # #base price
            #
            # specificBasePrice = basePrice[basePrice['commodity']==commodity]
            # # resultBasePrice = seasonal_decompose(specificBasePrice['msprice'], model='multiplicity', freq=1)
            #
            #
            # plt.plot(resultCommodityMul.resid*resultCommodityMul.trend)
            # plt.plot(specificBasePrice.msprice)
            # # resultCommodityAdd.plot()
            # # resultCommodityMul.plot()
            # plt.show()
            #Deseasonalized value :

            # print result.trend
            # print result.seasonal

            # Comparison with the market value

            # Market fluctuation

        # For each season, get the fluctuation of each commodity in each APMC
            # Get the maximum value difference

        #ude
            # result.plot()
            # plt.show()

    # Seasonality index
    # https://machinelearningmastery.com/decompose-time-series-data-trend-seasonality/

    # Assign X and Y values
    # Filter outliers


    # outputVal  = APMCprice[APMCprice.apply(lambda x: APMCprice[(APMCprice['Commodity']=='Bajri') & (APMCprice['APMC']=='Ahmednagar')]['modal_price']<movingaverage(APMCprice[(APMCprice['Commodity']=='Bajri') & (APMCprice['APMC']=='Ahmednagar')]['modal_price'],3,1))]
    # print outputVal
    # exit()
    # Xvalue = APMCprice[(APMCprice['Commodity']=='Bajri') & (APMCprice['APMC']=='Ahmednagar')]['date']
    # Yvalue = APMCprice[(APMCprice['Commodity']=='Bajri') & (APMCprice['APMC']=='Ahmednagar')]['modal_price']
    #
    # outTuple = [y for x, y in sorted(zip(Xvalue,Yvalue))]
    # Xvalue = sorted(Xvalue)
    #
    # Yvalue = [Yval for Yval in outTuple]
    #
    # print (Xvalue)
    # print (Yvalue)
    # import matplotlib.pyplot as plt
    #
    # plt.plot(Xvalue,Yvalue)
    # # plt.show()
    #
    #
    #
    #
    #
    # YvalueAvg = movingaverage(Yvalue, 3)
    #
    # plt.plot(Xvalue, YvalueAvg)
    # # plt.show()
    # STD = np.std(YvalueAvg)
    # Xnew= []
    # Ynew= []
    #
    # for ii in range(len(Xvalue)):
    #     if Yvalue[ii] < YvalueAvg[ii]+STD:
    #         Xnew.append((Xvalue[ii]))
    #         Ynew.append((Yvalue[ii]))
    #
    # plt.plot(Xnew, Ynew)
    # plt.show()
    #
    # print len(Xnew)
    # #remove the scenarios where the price is too high
    #
    # # For  just the monthly data do a multiplicative seasonal index and get the nominal price

def removeOutlier(data,stdMul):
    data = data[~((data - data.mean()).abs() > stdMul * data.std())]

    return data


if __name__=='__main__':
    main()
