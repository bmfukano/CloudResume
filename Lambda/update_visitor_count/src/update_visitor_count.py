from os import environ
from boto3 import resource

_LAMBDA_DYNAMODB_RESOURCE = { "resource" : resource('dynamodb'), 
                              "table_name" : environ.get("DYNAMODB_TABLE_NAME","NONE") }

class LambdaDynamoDBClass:
    """
    AWS DynamoDB Resource Class
    """
    def __init__(self, lambda_dynamodb_resource):
        """
        Initialize a DynamoDB Resource
        """
        self.resource = lambda_dynamodb_resource["resource"]
        self.table_name = lambda_dynamodb_resource["table_name"]
        self.table = self.resource.Table(self.table_name)

def lambda_handler(event, context):

    global _LAMBDA_DYNAMODB_RESOURCE

    dynamodb_resource_class = LambdaDynamoDBClass(_LAMBDA_DYNAMODB_RESOURCE)

    return increment_visitor_count(dynamodb_resource_class)

def increment_visitor_count(dynamo_db):
    status_code = 200
    body = 0

    try:
        visits = dynamo_db.table.get_item(Key={'visits': 'resume_visits'})["Item"]
        dynamo_db.table.update_item(Key={'visits': 'resume_visits'},
            UpdateExpression='SET visit_count = :val1',
            ExpressionAttributeValues={':val1': visits['visit_count'] + 1}
        )
        body = visits['visit_count'] + 1

    except KeyError as index_error:
        body = "Not Found: " + str(index_error)
        status_code = 404
    except Exception as other_error:               
        body = "ERROR: " + str(other_error)
        status_code = 500
    finally:
        return {"statusCode": status_code, "body" : body }
