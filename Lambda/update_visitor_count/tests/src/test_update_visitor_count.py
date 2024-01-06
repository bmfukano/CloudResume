"""
Unit Test for Update Visitor Count
"""
import sys
import os
from unittest import TestCase
from boto3 import resource, client
import moto

sys.path.append('./src')
from src.update_visitor_count import LambdaDynamoDBClass   # pylint: disable=wrong-import-position
from src.update_visitor_count import increment_visitor_count  # pylint: disable=wrong-import-position

@moto.mock_dynamodb
class TestSampleLambda(TestCase):
    """
    Test class for the application sample AWS Lambda Function
    """

    # Test Setup
    def setUp(self) -> None:
        """
        Create mocked resources for use during tests
        """

        # Mock environment & override resources
        self.test_ddb_table_name = "unit_test_ddb"
        os.environ["DYNAMODB_TABLE_NAME"] = self.test_ddb_table_name

        # Set up the services: construct a (mocked!) DynamoDB table
        dynamodb = resource('dynamodb', region_name="us-east-2")
        dynamodb.create_table(
            TableName=self.test_ddb_table_name,
            KeySchema=[{"AttributeName": "visits", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "visits", "AttributeType": "S"}],
            BillingMode='PAY_PER_REQUEST'
            )

        # Establish the "GLOBAL" environment for use in tests.
        mocked_dynamodb_resource = resource("dynamodb", region_name="us-east-2")
        mocked_dynamodb_resource = {"resource": resource('dynamodb'),
                                    "table_name": self.test_ddb_table_name}
        self.mocked_dynamodb_class = LambdaDynamoDBClass(mocked_dynamodb_resource)

    def test_create_letter_in_s3(self) -> None:
        """
        Verify given correct parameters, the document will be written to S3 with proper contents.
        """

        # Post test items to a mocked database
        self.mocked_dynamodb_class.table.put_item(Item={"visits": "resume_visits",
                                                        "visit_count": 0})

        visits = self.mocked_dynamodb_class.table.get_item(Key={'visits': 'resume_visits'})
        print(visits)

        # Run DynamoDB to S3 file function
        test_return_value = increment_visitor_count(
                        dynamo_db=self.mocked_dynamodb_class
                        )

        # Test
        self.assertEqual(test_return_value["statusCode"], 200)
        self.assertEqual(test_return_value["body"], 1)

    def test_create_letter_in_s3_doc_type_notfound_404(self) -> None:
        """
        Verify given a document type not present in the data table, a 404 error is returned.
        """
        # Post test items to a mocked database
        self.mocked_dynamodb_class.table.put_item(Item={"visits": "bad_item",
                                                        "data": "bad_data"})

        # Run DynamoDB to S3 file function
        test_return_value = increment_visitor_count(
                            dynamo_db=self.mocked_dynamodb_class
                            )

        # Test
        self.assertEqual(test_return_value["statusCode"], 404)
        self.assertIn("Not Found", test_return_value["body"])

    def tearDown(self) -> None:
        dynamodb_resource = client("dynamodb", region_name="us-east-2")
        dynamodb_resource.delete_table(TableName=self.test_ddb_table_name)

# End of unit test code
