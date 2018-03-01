import pymongo
class dataBase:
    def __init__(self,dbName):
        self.Name = self.initiateDB(dbName)

    def initiateDB(self, dbName):
        # Connect to DB. Work on the exception handlers. They dont seem to work
        print("Connecting to database...")
        print()
        try:
            conn = pymongo.MongoClient()
            print("Connected successfully!!!")
            print()
        except pymongo.errors.ConnectionFailure as e:
            print("Could not connect to MongoDB: %s" % e)
            print()

        return conn[dbName]

    def updateDB(self,collectionName,groupedDetails):

        for details in groupedDetails:
            self.Name[collectionName].update({"_id": details["Name"]}, {'$set': details}, upsert=True)
