import pandas as pd
import numpy as np

# Minimum support price
basePrice = pd.read_csv('./data/CMO_MSP_Mandi.csv')

print "Number of unique commodities for which base proce is available"
print basePrice['commodity'].unique().shape

print "Number of unique types of commodities for which base proce is available"
print basePrice['Type'].unique().shape


# APMC price

APMCprice =  pd.read_csv('./data/Monthly_data_cmo.csv')

# Treat the data
# Convert datatime to the format
APMCprice['date'] = pd.to_datetime(APMCprice['date'],format="%Y-%m")


# Get the list of unique APMC and the Commodities

uniqueAPMC = APMCprice['APMC'].unique()

uniqueCommodity = APMCprice['Commodity'].unique()
def movingaverage(interval, window_size, STD):
    window= np.ones(int(window_size))/float(window_size)

    newVal = np.convolve(interval, window, 'same')
    # print newVal
    # print (STD*np.std(newVal))
    return newVal+(STD*np.std(newVal))
uniqueAPMC=['Ahmednagar']
uniqueCommodity=['Bajri']

#Think through this method
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
for APMC in uniqueAPMC:
    for commodity in uniqueCommodity:
        print APMC,commodity
        specificData = APMCprice[(APMCprice['Commodity']==commodity) & (APMCprice['APMC']==APMC)]

        # Sorting the values in a linear time line
        Xvalue = specificData['date']
        Yvalue = specificData['modal_price']

        outTuple = [y for x, y in sorted(zip(Xvalue, Yvalue))]
        Xvalue = sorted(Xvalue)

        Yvalue = [Yval for Yval in outTuple]

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
        result = seasonal_decompose(list(Yvalue),model='multiplicative',freq=4)
        result.plot()
        plt.show()

# Seasonality index
# https://machinelearningmastery.com/decompose-time-series-data-trend-seasonality/
exit()
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