def TranscriptsLabels_preProcessed():
    """outputs 2 variables: the transcripts and labels extracted, cleaned and binarized; make sure you store in 2 variables"""
    from my_FunctionsModule_ForThesis import TranscriptsLabels_storer
    YoutubeData = TranscriptsLabels_storer()
    
    transcripts= YoutubeData[1]
    labels = YoutubeData[2]
    
    from my_FunctionsModule_ForThesis import Binarizer_xRemover
    Binarizer_xRemover(labels,transcripts,numeric=True)
    
    return transcripts, labels


def TranscriptsLabels_storer():
    """outputs a list of 3 lists containing the: Video ids + Transcripts+ labels ; I use it for the input of the Classifier pipeline"""
    from my_FunctionsModule_ForThesis import TranscriptExtractor
    transcripts = TranscriptExtractor()
    Transcripts_strings=[]
    labels=[]
    VideoId_list = [] #not necessary perse, just to keep track if necessary
    
    for X in transcripts:
        Transcript, Label,VideoId = X[2], X[3], X[0]
        Transcripts_strings.append(Transcript)
        labels.append(Label)
        VideoId_list.append(VideoId)
        transcriptsIDsLabels_List = list((VideoId_list,Transcripts_strings,labels))
    return transcriptsIDsLabels_List


def LabelXcleaner(labels,transcripts):
    DELETED = 0
    I =0
    for X in labels:
        if X == 'X'.lower():
            DELETED +=1
    #        print(VideoId_list[I])
            print('this transcript will be deleted, together with its label: \n ' ,transcripts[I][:100],'\n\n')
            transcripts.pop(I)[:100]
            labels.pop(I)
            I-=1
            print('deleted:' , DELETED)
#        else:
#            labels[I] = int(X) # the predictfunctions of some algos predict strings only, then you have issues with confusion matrix
        I+=1


def LabelxTranscriptIsolator(Transcripts,Labels,labelNumber):
    """ creates a list of all the transcripts that have the specified label, thus are conspiratorial; perhaps handy for making a corpus or vocabulary IF OTHER LABEL, CONFIGURE 'J==0/1/2'"""
    indices = []
    for i,j in enumerate(Labels):
        if j==labelNumber:
            indices.append(i)
    #extract elements from a list using indices
    Transcripts = [Transcripts[i] for i in indices]
    return Transcripts


def ner_ents__List():
    """ NER, all the NERS or ents_ from spacy in a list:"""
    listOfSpacyEnts = ['PERSON', 'NORP' 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
    return listOfSpacyEnts


def CleanTokenizer(doc): #SYNC WITH 'cleaning youtube transcripts..."
    # a list of LabelxTranscriptIsolatortokens I want to filter out, next to the predefined stopword list
    myFilterOutList = ['music']
# No list comprehension, for comprehension, lol. 
    cleanedTokens = []
    for token in doc: # can i mike this nlp(doc), or text
        if not (token.is_stop or token.is_alpha==False or len(token.lemma_) <3 or token.lemma_.lower() in myFilterOutList ):
            cleanedTokens.append(token.lemma_.lower())
    return cleanedTokens


def TranscriptExtractor(directory_youtubecsv, directory_transcripts):
    "This Function extracts a list from the dataset with the following string contents: [Video_ID, Video_Category, Video_Transcript, Video_Rating]"

    # first we load in all info from the youtube.csv we need
    os.chdir(directory_youtubecsv)
    with open('YouTube.csv', mode='r') as infile:
        reader = csv.reader(infile)
    youtube_ranked = []
    for rows in reader:
        youtube_ranked.append(rows)
    youtube_ranked_data = {}

    for listed in youtube_ranked:
        youtube_ranked_data.update({listed[1][32:]: listed[5]})

    ## now for the transcript data
    id_cat_transcripts = []

    os.chdir(directory_transcripts)

    # firearms
    with open('firearms_transcript.json') as f:
        data_transcript_firearms = json.load(f)
    # here we fill up a dataset with: [ID, Category, Transcript, Final rating] for firearms
    id_transcripts_firearms = list(data_transcript_firearms.keys())
    for id in id_transcripts_firearms:
        id_cat_transcripts.append([id, "firearms", data_transcript_firearms[id], youtube_ranked_data[id]])

    # fitness
    with open('fitness_transcript.json') as f:
        data_transcript_fitness = json.load(f)
    # here we fill up a dataset with: [ID, Category, Transcript, Final rating] for fitness
    id_transcripts_fitness = list(data_transcript_fitness.keys())
    for id in id_transcripts_fitness:
        id_cat_transcripts.append([id, "fitness", data_transcript_fitness[id], youtube_ranked_data[id]])

    # gurus
    with open('gurus_transcript.json') as f:
        data_transcript_gurus = json.load(f)
    # here we fill up a dataset with: [ID, Category, Transcript, Final rating] for fitness
    id_transcripts_gurus = list(data_transcript_gurus.keys())
    for id in id_transcripts_gurus:
        id_cat_transcripts.append([id, "gurus", data_transcript_gurus[id], youtube_ranked_data[id]])

    # martial_arts
    with open('martial_arts_transcript.json') as f:
        data_transcript_martial_arts = json.load(f)
    # here we fill up a dataset with: [ID, Category, Transcript, Final rating] for fitness
    id_transcripts_martial_arts = list(data_transcript_martial_arts.keys())
    for id in id_transcripts_martial_arts:
        id_cat_transcripts.append([id, "martial_arts", data_transcript_martial_arts[id], youtube_ranked_data[id]])

    # natural foods
    with open('natural_foods_transcript.json') as f:
        data_transcript_natural_foods = json.load(f)
    # here we fill up a dataset with: [ID, Category, Transcript, Final rating] for fitness
    id_transcripts_natural_foods = list(data_transcript_natural_foods.keys())
    for id in id_transcripts_natural_foods:
        id_cat_transcripts.append([id, "natural_foods", data_transcript_natural_foods[id], youtube_ranked_data[id]])

    # tiny houses
    with open('tiny_houses_transcrip.json') as f:
        data_transcript_tiny_houses = json.load(f)
    # here we fill up a dataset with: [ID, Category, Transcript, Final rating] for fitness
    id_transcripts_tiny_houses = list(data_transcript_tiny_houses.keys())
    for id in id_transcripts_tiny_houses:
        id_cat_transcripts.append([id, "tiny_houses", data_transcript_tiny_houses[id], youtube_ranked_data[id]])

    ## we now have a full set of 600 entries containing all video ID's, categories, transcripts and rankings
    # print(id_cat_transcripts)

    # NOW! let's remove all empty transcripts
    id_cat_transcripts_emptycleaned = []

    for unit in id_cat_transcripts:
        if unit[2] == '':
            continue
        else:
            id_cat_transcripts_emptycleaned.append(unit)

    return id_cat_transcripts_emptycleaned

def transcriptsLabels_storer():
    """outputs a list of 3 lists containing the: 0:Video-ids + 1:Transcripts + 2:Labels ; I use it for the input of the Classifier pipeline"""
    from my_FunctionsModule_ForThesis import TranscriptExtractor
    transcripts = TranscriptExtractor()
    transcripts_strings=[]
    labels=[]
    VideoId_list = [] #not necessary perse, just to keep track if necessary
    
    for X in transcripts:
        Transcript, Label,VideoId = X[2], X[3], X[0]
        transcripts_strings.append(Transcript)
        labels.append(Label)
        VideoId_list.append(VideoId)
        transcriptsIDsLabels_List = list((VideoId_list,transcripts_strings,labels))
    return transcriptsIDsLabels_List


def Binarizer_xRemover(labels,transcripts,numeric=False):
    """# for If you want to Binerize AND delete the x's :"""
    I = 0
    DELETED = 0
    if numeric == False:
	    for X in labels:
	        if X =='1' or X =='2':
	            labels[I]='False'
	        elif X =='3':
	            labels[I]='True'
	        elif X == 'X'.lower():
	            DELETED +=1
	    #        print(VideoId_list[I])
	            print('this transcript will be deleted, together with its label: \n ' ,transcripts[I][:100],'\n\n')
	            transcripts.pop(I)[:100]
	            labels.pop(I)
	            I-=1 # because 181 gets removed, 182 becomes 181 while I will be 182 and old 182 is skipped
	        I += 1
    while labels.count('False') + labels.count('True') != len(labels):
        for Y in labels:
            if Y not in (['False', 'True']):
                Binarizer_xRemover(labels,transcripts)

    if numeric == True:
	    i=0
	    for x in labels:
	        if x =='False':
	            labels[i]=0
	            i+=1
	        else:    
	            labels[i]=1
	            i+=1
