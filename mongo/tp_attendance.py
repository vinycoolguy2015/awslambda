def tp_attendance(id,attendancePercent,days,rule):
    import datetime
    from datetime import timedelta
    trainingCenters=db.trainingcentres.count({"belongsTo":ObjectId(id)})
    if trainingCenters > 0:
        trainingCenters=db.trainingcentres.find({"belongsTo":ObjectId(id)})
    studentCount=0
    requiredAttendanceCount=0
    attendanceCount=0
    attendancePercentage=0
    for trainingCenter in trainingCenters:
        batchCount=db.batches.count({"belongsTo.trainingCentreID":ObjectId(trainingCenter[u'_id']),"status":"Started"})
        if batchCount > 0:
            batches=db.batches.find({"belongsTo.trainingCentreID":ObjectId(trainingCenter[u'_id']),"status":"Started"},{"_id":1,"students":1,"attendance":1,"startDate":1})
        for batch in batches:
            studentCount=studentCount+(len(batch["students"]))
            startDate=batch["startDate"]
            endDate= startDate + timedelta(days=days-1)
            records=db.batches.aggregate([{"$match":{"_id" : batch[u'_id']}},{"$unwind":"$attendance"},{"$project":{"attendance":1}}])
            for record in records:
                attendanceDate=record[u'attendance'][u'date']
                if attendanceDate > endDate:
                    for student in record[u'attendance'][u'students']:
                        attendanceStatus=student['attendanceStatus']
                        if attendanceStatus=="P" or attendanceStatus=="Present":
                            attendanceCount+=1
    requiredAttendanceCount+=studentCount*days
    attendancePercentage=round((attendanceCount*100)/requiredAttendanceCount,2)
    if attendancePercentage < attendancePercent:
        data={}
        data['alertFor']=ObjectId(id)
        data['alertType']="Attendance"
        data['entity']="Training Partner"
        data['students'] = studentCount
        data['attendancePercentage']=attendancePercentage
        data['date']=datetime.datetime.today().strftime("%m/%d/%Y")
        data['RuleId']=rule
        result = db.alerts.insert_one(data)
        db.trainingpartners.update({'_id':ObjectId(id)},{'$set':{"notifications.isAlertAvailable":"true"}})





def tc_attendance(id,attendancePercent,days,rule):
    import datetime
    from datetime import timedelta
    batches=db.batches.count({"belongsTo.trainingCentreID":ObjectId(id),"status":"Started"})
    if batches > 0:
        batches=db.batches.find({"belongsTo.trainingCentreID":ObjectId(id),"status":"Started"},{"_id":1,"students":1,"attendance":1,"startDate":1})
        studentCount=0
        requiredAttendanceCount=0
        attendanceCount=0
        attendancePercentage=0
        for batch in batches:
            studentCount=studentCount+(len(batch["students"]))
            startDate=batch["startDate"]
            endDate= startDate + timedelta(days=days-1)
            records=db.batches.aggregate([{"$match":{"_id" : batch[u'_id']}},{"$unwind":"$attendance"},{"$project":{"attendance":1}}])
            for record in records:
                attendanceDate=record[u'attendance'][u'date']
                if attendanceDate > endDate:
                    for student in record[u'attendance'][u'students']:
                        attendanceStatus=student['attendanceStatus']
                        if attendanceStatus=="P" or attendanceStatus=="Present":
                            attendanceCount+=1
        requiredAttendanceCount+=studentCount*days
        attendancePercentage=round((attendanceCount*100)/requiredAttendanceCount,2)
        if attendancePercentage < attendancePercent:
                data={}
                data['alertFor']=ObjectId(id)
                data['alertType']="Attendance"
                data['entity']="Training Center"
                data['students'] = studentCount
                data['attendancePercentage']=attendancePercentage
                data['date']=datetime.datetime.today().strftime("%m/%d/%Y")
                data['RuleId']=rule
                result = db.alerts.insert_one(data)
                db.trainingcentres.update({'_id':ObjectId(id)},{'$set':{"notifications.isAlertAvailable":"true"}})
       
                
                
                

from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient()
db = client.mydb
cursor = db.ruleenginedefinitions.aggregate([{"$match":{"$or":[{"rules.Status": "Not Sent"},{"rules.Status":{"$exists":False}}]}},{"$unwind":"$rules"}, {"$match":{"$or":[{"rules.Status": "Not Sent"},{"rules.Status":{"$exists":False}}]}}])
for document in cursor:
    db.ruleenginedefinitions.update(
    {"_id":ObjectId(document[u'_id']), "rules": {"$elemMatch": {"PhaseName": document[u'rules'][u'PhaseName']}}},{"$set":{"rules.$.Status":"Sent"}});
    rule=document[u'_id']
    whenToApply=float(str(document[u'rules'][u'criteriaToMatch']))
    days=document[u'rules'][u'noOfDays']
    sendTo=str(document[u'rules'][u'sendTo'])
    paymentBasedOn= str(document[u'rules'][u'paymentBasedOn']) 
    id=str(document[u'rules'][u'id']) 
    if paymentBasedOn =="Attendance":
        if sendTo=="Training Partner":
            tp_attendance(id,whenToApply,days,rule)
        elif sendTo=="Training Centre":
            tc_attendance(id,whenToApply,days,rule)
        
