from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
Db = client['EmployeeDetails']
Collection = Db['Employees']
Collection2 = Db['Attendance']
emp = [{'name':'komali','Role':'Software Engineer','Experience':'I','Majored in':'AIML'},
       {'name':'Jeevana','Role':'Web Developer','Experience':'II','Majored in':'AIML'},
       {'name':'Geetha','Role':'Debugger','Experience':'III','Majored in':'AIML'},
       {'name':'aa','Role':' Engineer','Experience':'I','Majored in':'AIML'}]
Collection.insert_many(emp)
att=[ {'Mon':"checkin-8:20,checkout-4:20",'Tues':"checkin-09:20,checkout-5:20",'wed':"checkin-08:20,checkout-4:20",'Thurs':"checkin-09:20,checkout-4:20",'fri':"checkin-11:20,checkout-3:20"},
         {'Mon':"checkin-09:20,checkout-4:20",'Tues':"checkin-10:20,checkout-5:20",'wed':"checkin-08:20,checkout-4:20",'Thurs':"checkin-09:20,checkout-4:20",'fri':"checkin-11:20,checkout-3:20"},
          {'Mon':"checkin-10:20,checkout-4:20",'Tues':"checkin-10:20,checkout-5:20",'wed':"checkin-08:20,checkout-4:20",'Thurs':"checkin-09:20,checkout-4:20",'fri':"checkin-11:20,checkout-3:20"},
          {'Mon':"checkin-09:20,checkout-4:20",'Tues':"checkin-10:20,checkout-5:20",'wed':"checkin-08:20,checkout-4:20",'Thurs':"checkin-10:20,checkout-4:20",'fri':"checkin-11:20,checkout-3:20"}]
Collection2.insert_many(att)

updatereco = Collection.update_one({'name':'komali'},{'$set':{'Experience':'II'}})
updatereco = Collection.update_one({'name':'Jeevana'},{'$set':{'Experience':'III','Role':'Developer'}})
