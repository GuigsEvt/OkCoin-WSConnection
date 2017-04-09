from pymongo import MongoClient
from enum import Enum
import Definition, collections

class COLLECTIONS(Enum):
    ORDER = 'Orders'
    TRADE = 'Trades'
    CANDLESTICK = 'Candlesticks'

class MongoDB(object):

    # Create singleton for the MongoDb class to prevent multiple instance of mongodb client
    class __MongoDb(object):

        def __init__(self):
            # Create MongoClient instance. For now it runs on the localhost interface port 27017. See if we change that.
            try:
                self.client = MongoClient()
                db = Definition.DATABASE_TRADING
                self.client.test.authenticate()
                self.dbMongo = self.client[Definition.DATABASE_TRADING]
                print(self.dbMongo.last_status())
                print(self.dbMongo.collection_names())
            except Exception as e:
                print ('Exc:' + str(e))

        def insertDocument(self, object, collection):
            return self.dbMongo[collection.value].insert_one(object.toJSON())

        def insertDocuments(self, objects, collection):
            for object in objects:
                self.dbMongo[collection.value].insert_one(object.toJSON())

        def updateDocument(self, object, criteria, collection):
            print(str(criteria))
            print(self.dbMongo[collection.value].update(criteria, object.toJSON()))

        def getWholeCollection(self, collection, sized, ordered):
            if self.countDocuments(collection) > 0:
                if ordered:
                    objects = self.dbMongo[collection.value].find().sort(ordered).limit(sized)
                else:
                    objects = self.dbMongo[collection.value].find().limit(sized)
                return objects
            else: return []

        def getCollectionOnCriteria(self, collection, sized, criteria, ordered):
            if self.countDocuments(collection, criteria):
                if ordered:
                    objects = self.dbMongo[collection.value].find(criteria).sort(ordered).limit(sized)
                else:
                    objects = self.dbMongo[collection.value].find(criteria).limit(sized)
                #for object in objects:
                #    print(object)
                return objects
            else: return []

        def countDocuments(self, collection, criteria = {}):
            if criteria:
                return self.dbMongo[collection.value].count(criteria)
            return self.dbMongo[collection.value].count()

    __instance = None

    def __init__(self):
        # Initiate the singleton object
        if not MongoDB.__instance:
                MongoDB.__instance = MongoDB.__MongoDb()

    def addDocument(self, objects, collection):
        if isinstance(objects, collections.Iterable):
            print(self.__instance.insertDocuments(objects, collection))
        else:
            print(self.__instance.insertDocument(objects, collection))

    def updateDocument(self, collection, object, criteria):
        print(self.__instance.updateDocument(object, criteria, collection))

    def getDocumentOnCriteria(self, collection, sized = 100, criteria = {}, ordered = {}):
        return self.__instance.getCollectionOnCriteria(collection, sized, criteria, ordered)

    def getDocument(self, collection, sized = 100, ordered = {}):
        return self.__instance.getWholeCollection(collection, sized, ordered)

    def countDocuments(self, collection, criteria = {}):
        return self.__instance.countDocuments(criteria)
