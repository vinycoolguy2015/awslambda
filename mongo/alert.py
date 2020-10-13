def send_email(email,subject,msg):
    import smtplib
    from email.mime.text import MIMEText
    sender = 'info@xyz.com'
    msg = MIMEText(msg)
    msg['From'] = sender
    msg['Subject'] = subject
    msg['To'] = email
    recipient=email
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
    server.login('info@xyz.com', 'p1086#')
    server.sendmail(sender,[recipient], msg.as_string())
    server.quit()


def tp_placement(id,placementPercent):
    students=0
    placedStudents=0
    placementPercentage=0
    trainingCenters=db.trainingcentres.find({"belongsTo":id},{"_id":1})
    for trainingCenter in trainingCenters:
        batches=db.batches.count({"belongsTo.trainingCentreID":trainingCenter[u'_id'],"status":"Closed"})
        if batches > 0:
            batches=db.batches.find({"belongsTo.trainingCentreID":trainingCenter[u'_id'],"status":"Closed"},{"_id":0,"students":1,"placedStudents":1})
            for batch in batches:
                students=students+(len(batch["students"]))
                placedStudents=placedStudents+(len(batch["placedStudents"]))
    
    if not students == 0:
        if not placedStudents==0:
            placementPercentage=(placedStudents*100)/students
            
    if not students == 0 and placementPercentage < placementPercent:
        return placementPercentage
    
    
def tc_placement(id,placementPercent):
    students=0
    placedStudents=0
    placementPercentage=0
    batches=db.batches.count({"belongsTo.trainingCentreID":id,"status":"Closed"})
    if batches > 0:
        batches=db.batches.find({"belongsTo.trainingCentreID":id,"status":"Closed"},{"_id":0,"students":1,"placedStudents":1})
        for batch in batches:
            students=students+(len(batch["students"]))
            placedStudents=placedStudents+(len(batch["placedStudents"]))
    
    if not students == 0:
        if not placedStudents==0:
            placementPercentage=(placedStudents*100)/students
            
    if not students == 0 and placementPercentage < placementPercent:
         return placementPercentage
        
def aa_placement(id,placementPercent):
    students=0
    placedStudents=0
    placementPercentage=0
    schemes=db.agencyaggregators.find_one({"_id":id},{"_id":0,"schemes":1})
    schemes=(schemes[u'schemes'])
    for scheme in schemes:
        batches=db.batches.count({"scheme":scheme,"status":"Closed"})
        if batches > 0:
            batches=db.batches.find({"scheme":scheme,"status":"Closed"},{"_id":0,"students":1,"placedStudents":1})
            for batch in batches:
                students=students+(len(batch["students"]))
                placedStudents=placedStudents+(len(batch["placedStudents"]))
    if not students == 0:
        if not placedStudents==0:
            placementPercentage=(placedStudents*100)/students
            
    if not students == 0 and placementPercentage < placementPercent:
         return placementPercentage


from pymongo import MongoClient
client = MongoClient()
db = client.mydb
cursor = db.b.aggregate([{"$match":{"$or":[{"rules.status": "Not Sent"},{"rules.status":{"$exists":False}}]}},{"$unwind":"$rules"}, {"$match":{"$or":[{"rules.status": "Not Sent"},{"rules.status":{"$exists":False}}]}}])
for document in cursor:
    whenToApply=float(str(document[u'rules'][u'whenToApply']))
    sendTo=str(document[u'rules'][u'sendTo'])
    paymentBasedOn= str(document[u'rules'][u'paymentBasedOn']) 
    id=str(document[u'rules'][u'_id']) 
    if sendTo=="Training Partner":
        placement=tp_placement(id,whenToApply)
        if placement < whenToApply:
            email=db.trainingpartners.find({"_id":id},{"_id":0,"email":1})
            subject="Placement alert for training partner"
            message="Placement is less than the alert criteria"
            sendEmail(email,subject,message)
    elif sendTo=="Training Center":
        placement=tc_placement(id,whenToApply)
        if placement < whenToApply:
            email=db.trainingcentres.find({"_id":id},{"_id":0,"email":1})
            subject="Placement alert for training center"
            message="Placement is less than the alert criteria"
            sendEmail(email,subject,message)
    elif sendTo=="Agency Aggregator":
        placement=aa_placement(id,whenToApply)
        if placement < whenToApply:
            email=db.agencyaggregators.find({"_id":id},{"_id":0,"email":1})
            subject="Placement alert for agency aggregator"
            message="Placement is less than the alert criteria"
            sendEmail(email,subject,message)
    result = db.b.update_one(
    {"rules":{"$elemMatch":{"whenToApply":whenToApply,"sendTo":sendTo,"paymentBasedOn":paymentBasedOn,"_id":id}}},
    {"$set": {"rules.$.status": "Sent"}}
)
   

    
                        
