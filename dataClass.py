from pandas import to_datetime
class cAPMC:
    def __init__(self,data):
        self.data=data
        self.treatData()
        self.data.set_index(['APMC', 'Commodity', 'date'], inplace=True)

    def treatData(self):
        # self.data['date'] = self.data['date'].apply(lambda x:
        #                                 datetime.strptime(str(x), '%Y-%m'))
        # self.data['date'] = datetime.strptime(self.data['date'][:10], '%Y-%m-%d')
        self.data['date'] = to_datetime(self.data['date'], format='%Y-%m')
        self.data.Commodity = self.data.Commodity.astype(str).apply(lambda x: x.upper())
        self.data.APMC = self.data.APMC.astype(str).apply(lambda x: x.upper())

    def groupData(self):
        self.groupList=[]
        for idone, APMC in self.data.groupby('APMC'):
            APMCdetails = {"Name": idone, "commodityList": []}

            for idtwo, commodity in APMC.groupby('Commodity'):
                commoditydetails = {"Name": idtwo, "salesList": []}
                for idthree, date in commodity.groupby('date'):
                    dateDetails = {"date": idthree, "price": float(date['modal_price'].values[0])}
                    commoditydetails['salesList'].append(dateDetails)
                APMCdetails["commodityList"].append(commoditydetails)

            self.groupList.append(APMCdetails)



class cMSP:
    def __init__(self, data):
        self.data = data
        self.treatData()
        self.data.set_index(['commodity','year'], inplace=True)

    def treatData(self):

        # self.data['year'] = self.data['year'].apply(lambda x:
        #                                 datetime.strptime(str(x), '%Y'))
        self.data['year'] = to_datetime(self.data['year'], format="%Y")
        self.data.commodity = self.data.commodity.astype(str).apply(lambda x: x.upper())

    def groupData(self):
        self.groupList=[]

        for idone, commodity in self.data.groupby('commodity'):
            commoditydetails = {"Name": idone, "salesList": []}
            for idthree, date in commodity.groupby('year'):
                dateDetails = {"date": idthree, "price": float(date['msprice'].values[0])}
                commoditydetails['salesList'].append(dateDetails)

            self.groupList.append(commoditydetails)
