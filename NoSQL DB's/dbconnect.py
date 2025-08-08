from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
Db = client['MYPROJECT']
Collection = Db['Students']
Collection2 = Db['Marks']
doc = [{'name':'komali','class':'Btech','Branch':'AIML','year':'III','courses':'AI'},
       {'name':'Jeevana','class':'Btech','Branch':'AIML','year':'III','courses':'AI'},
       {'name':'Geetha','class':'Btech','Branch':'AIML','year':'III','courses':'AI'},
       {'name':'aa','class':'Btech','Branch':'AIML','year':'III','courses':'AI'}]
Collection.insert_many(doc)
markdoc=[{'name':'komali','class':'Btech','Branch':'AIML','year':'III','courses':'AI','marks':'99'},
         {'name':'jeevana','class':'Btech','Branch':'AIML','year':'III','courses':'AI','marks':'98'},
         {'name':'geetha','class':'Btech','Branch':'AIML','year':'III','courses':'AI','marks':'97'},
         {'name':'aa','class':'Btech','Branch':'AIML','year':'III','courses':'AI','marks':'9'}]
Collection2.insert_many(markdoc)

print("Documents inserted successfully")
results=Collection.find_one({'name':'komali'})
print(results)
resultall=Collection.find()

updatereco = Collection.update_one({'name':'komali'},{'$set':{'class':'BTECH'}})
updatereco = Collection.update_one({'id':'6881c2dda728ffd3aa97d393'},{'$set':{'class':'BTECH'}})

deletereco=Collection.delete_one({'name':'aa'})
deletereco=Collection.delete_one({'name':'aa','Branch':'AIML'})

deleteall = Collection2.delete_many({})
for stu in resultall:
    print(stu)
