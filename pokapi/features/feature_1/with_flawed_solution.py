```
    def extracted_name(field):
        """
        Extracts and cleans the name from a given field dictionary.

        This function takes a dictionary containing a name and removes any trailing characters or additional
        unwanted text using a regular expression. It returns the cleaned name. 
        It uses a regular expression to match the sequence of leading characters that includes any combination 
        of hyphens, periods, commas, letters [in any language] and spaces from the name, and then strips unwanted characters [spaces and comma]
        from the matched result.

        If no valid characters are found at the beginning of the name, the original name is returned unmodified.

        Parameters:
            field (dict): A dictionary containing the key 'name' with the author's name.

        Returns:
            str: The cleaned author's name, or the original name if no valid characters are found.

        Example:
        >>> extracted_name({ 'name': 'Alice Wonderland'})
            Output: 'Alice Wonderland'

        """
        name = field['name']
        match = regex.match(r'^[a-zA-Z\u00C0-\u00FF\s\-.,]+', name)
        if match:
            return match.group(0).strip(' ,')
        return name
```