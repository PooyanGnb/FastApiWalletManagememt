class TextTransformService:
    """
    Service class dedicated to text transformations.
    """

    @staticmethod
    async def convert_dict_camel_case(data):
        """
        Convert dictionary(json) keys from snake_case to camelCase.

        Args:
        - data (dict): The dictionary with keys in snake_case.

        Returns:
        - dict: The dictionary with keys converted to camelCase.
        """
        converted_dict = {}
        for key, value in data.items():
            camel_key = await TextTransformService.snake_to_camel(key)
            converted_dict[camel_key] = value
        return converted_dict

    @staticmethod
    async def snake_to_camel(snake_str):
        """
        Helper method to convert a snake_case string to camelCase.

        Args:
        - snake_str (str): The snake_case string to convert.

        Returns:
        - str: The converted camelCase string.
        """
        components = snake_str.split("_")

        # Check if the first component is empty (starts with an underscore)
        if components[0] == '':
            # If the first component is empty, skip it and starts from the 2nd index and the next of it would be capitalized
            return components[1] + ''.join(x.title() for x in components[2:])
        else:
            # Normal conversion for strings not starting with an underscore
            return components[0] + ''.join(x.title() for x in components[1:])