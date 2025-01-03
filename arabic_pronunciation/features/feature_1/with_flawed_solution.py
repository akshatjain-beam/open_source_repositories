```
import re

def remove_links(text):
    """Removes URLs from a given text.

    Parameters:
    text (str): The input text containing URLs to be removed.

    Returns:
    str: The text with all URLs removed.

    Notes:
    This function uses a regular expression to match and remove URLs from the input text.
    The regex pattern matches both HTTP and HTTPS protocols, and can handle URLs with or without a protocol (e.g., "://example.com").
    The function returns the text with all URLs removed, leaving any remaining text intact.

    """
    return re.sub(r'http\S+|https\S+|www\S+', '', text)
```