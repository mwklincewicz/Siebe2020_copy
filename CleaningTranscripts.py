#======================================================================== #
''' importing the transcripts    '''
#======================================================================== #
#function, created from raf's script such that it easily callable
from my_FunctionsModule_ForThesis import transcriptExtractor
Transcripts = transcriptExtractor() #CAPS

transcripts_strings=[]
# labels=[] #when we run the ML algo we will need this
# videoId_list = [] #Non-Essential(NE), just to keep track if necessary

for X in Transcripts:
    Transcript, Label,VideoId = X[2], X[3], X[0]
    transcripts_strings.append(Transcript)
    # labels.append(Label)
    # videoId_list.append(VideoId)
   
#======================================================================== #
'''                 NLP    '''
#======================================================================== #

# =============================================================================
# Creating the spacy Doc file
# =============================================================================

#importing the spacy library and its NLP module for English
import spacy
import en_core_web_sm
# disabling the parser, the tagger, and the named entity recognizer.
nlp = en_core_web_sm.load(disable=["parser", "tagger", "ner"])

#computing the size of the corpus:
from decimal import Decimal # Non-Essential(NE); just for clarity
print('%.2E' % Decimal (len(str(transcripts_strings))))

nlp.max_length=1.1E7
# feeding the transcripts_strings to the pipeline, which obtains a doc object
doc = nlp(str(transcripts_strings))

# =============================================================================
# #extracting the tokens from the doc file in a seperate list
# =============================================================================
token_list = [token.text for token in doc]
print(token_list[:100])
print('%.2E' % Decimal ( len(token_list) ))
# print ( len(set(token_list)) ) 
# print (sum(lenList) / len(token_list) ) #4.85 characters per token


# =============================================================================
# Cleaning the tokens
# =============================================================================

#datacleaner method 1: (clearness method)
cleaned_tokens1 = [token.lemma for token in doc if not (token.is_stop or token.is_alpha) ] # this line defines what will be cleaned; so add token attributes if wanting to expand: https://spacy.io/api/token

print ( len(cleaned_tokens1),len(token_list),'\n deleted tokens:', len(token_list)-len(cleaned_tokens1) )

len ( set(cleaned_tokens1) )

# =============================================================================
# # analysis of what has been done in the cleaning stage:
# =============================================================================
cleaned_tokens1[:100]
print ('nr of tokens in original uncleaned corpus:', '%.2E' % Decimal (len(token_list)) , '\n wat is left after cleaning: ', len(cleaned_tokens1) , '\n tokens that are deleted:','%.2E' % Decimal (len(token_list)-len(cleaned_tokens1)))
# printing some actual tokens that are left after cleaning:
