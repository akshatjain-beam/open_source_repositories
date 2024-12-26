"""
Create a dictionary that maps each Buckwalter character to its corresponding Arabic script character.
The dictionary should have the following format: {Buckwalter_character: Arabic_script_character, ...}.

Example- 
    The Buckwalter character 'b' should be mapped to the Arabic script character 'ﺑ.'
Note-
   - Create the dictionary by listing all the Buckwalter characters and their corresponding Arabic script characters.
   - Make it python 2.X compatible.
"""
$PlaceHolder$

# Convert input string to Arabic
def buckwalterToArabic(word):
    result = u''
    for letter in word:
        if letter in ArabicScript:
            result += ArabicScript[letter]
        else:
            result += letter
    return result
