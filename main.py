from dataClass import cAPMC, cMSP
from database import dataBase
import pandas as pd

def main():
    #read input
    APMCdata = cAPMC(pd.read_csv('./data/Monthly_data_cmo.csv'))
    MSPdata = cMSP(pd.read_csv('./data/CMO_MSP_Mandi.csv'))

    dB = dataBase('socialCops')


    # APMCdata.groupData()
    #
    # dB.updateDB("APMC",APMCdata.groupList)

    MSPdata.groupData()

    dB.updateDB("MSP",MSPdata.groupList)



if __name__=="__main__":
    main()