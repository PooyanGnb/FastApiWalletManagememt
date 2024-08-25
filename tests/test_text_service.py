import unittest
import asyncio

from services.text_service import TextTransformService

class TestTextTransformService(unittest.TestCase):
    """
    Unit tests for the TextTransformService class which handles transformations of text,
    specifically converting dictionary keys from snake_case to camelCase.
    """

    def test_convert_dict_camel_case(self):
        """
        Test converting a dictionary with snake_case keys into one with camelCase keys.
        Verify that the transformation is correct for various types of keys.
        """
        # Setup: Dictionary with snake_case keys
        input_dict = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_address': 'john.doe@example.com'
        }
        # Expected result: Dictionary with camelCase keys
        expected_dict = {
            'firstName': 'John',
            'lastName': 'Doe',
            'emailAddress': 'john.doe@example.com'
        }
        
        # Execute: Transform the dictionary using the service method
        result = asyncio.run(TextTransformService.convert_dict_camel_case(input_dict))
        
        # Assert: Check if the transformed dictionary matches the expected output
        self.assertEqual(result, expected_dict)

    def test_snake_to_camel(self):
        """
        Test converting individual snake_case strings to camelCase strings.
        Include a variety of cases including strings with leading underscores and strings without underscores.
        """
        # Setup: Dictionary mapping snake_case strings to their expected camelCase transformations
        test_cases = {
            'first_name': 'firstName',
            'last_name': 'lastName',
            '_id': 'id',  # Handling leading underscores by removing them
            'name': 'name'  # No change expected for strings without underscores
        }
        
        # Execute and Assert: Convert each case and check against expected results
        for snake, expected_camel in test_cases.items():
            result = asyncio.run(TextTransformService.snake_to_camel(snake))
            self.assertEqual(result, expected_camel)

if __name__ == '__main__':
    unittest.main()
