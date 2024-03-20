import boto3
import argparse
dynamo = boto3.resource('dynamodb',region_name='ap-southeast-1')

def truncateTable(tableName):
    table = dynamo.Table(tableName)
    
    #get the table keys
    tableKeyNames = [key.get("AttributeName") for key in table.key_schema]

    #Only retrieve the keys for each item in the table (minimize data transfer)
    projectionExpression = ", ".join('#' + key for key in tableKeyNames)
    expressionAttrNames = {'#'+key: key for key in tableKeyNames}
    
    counter = 0
    page = table.scan(ProjectionExpression=projectionExpression, ExpressionAttributeNames=expressionAttrNames)
    with table.batch_writer() as batch:
        while page["Count"] > 0:
            counter += page["Count"]
            # Delete items in batches
            for itemKeys in page["Items"]:
                batch.delete_item(Key=itemKeys)
            # Fetch the next page
            if 'LastEvaluatedKey' in page:
                page = table.scan(
                    ProjectionExpression=projectionExpression, ExpressionAttributeNames=expressionAttrNames,
                    ExclusiveStartKey=page['LastEvaluatedKey'])
            else:
                break
    print(f"Deleted {counter}")
            
parser = argparse.ArgumentParser()
parser.add_argument("dynamodb_table_name", help="DynamoDB table name you want to truncate")
args = vars(parser.parse_args())
truncateTable(args['dynamodb_table_name'])
