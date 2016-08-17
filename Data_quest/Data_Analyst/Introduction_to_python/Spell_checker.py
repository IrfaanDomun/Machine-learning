"""
In this mission, we're going to explore how to build a basic spell checker. Spell checkers work by comparing each word
in a passage of text to a set of correctly spelled words. In this mission, we will learn:
"""

vocabulary = open("dictionary.txt","r")
print(vocabulary.read())

tokenized_vocabulary = vocabulary.split(" ")
print( tokenized_vocabulary[:5])

f = open("story.txt", 'r')
story_string = f.read()

def clean_text(text_string, special_characters):
    cleaned_string = text_string
    for string in special_characters:
        cleaned_string = cleaned_string.replace(string, "")
    cleaned_string = cleaned_string.lower()
    return(cleaned_string)

def tokenize(text_string, special_characters):
    cleaned_story = clean_text(text_string, special_characters)
    story_tokens = cleaned_story.split(" ")
    return(story_tokens)

misspelled_words = []
clean_chars = [",", ".", "'", ";", "\n"]
tokenized_story = tokenize(story_string, clean_chars)
tokenized_vocabulary = tokenize(vocabulary, clean_chars)

misspelled_words = [ i for i in tokenized_story if i not in tokenized_vocabulary]
print (misspelled_words)