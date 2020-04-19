
#======================================================================== #
'load a df with video ids (which will be used for the youtube api to download the transcripts: and later on for extracting the labels                          '


with open("C:\\Users\\Sa\\Documents\\listYoutubeids_thatRafTolgaSiebeWatched.txt",encoding="utf-8") as f:
    idList = f.readlines() #txt file with the ids:

#alternatively:
#dic = dict_oldDf # a dictionary where the keys correspond the the youtubeIDs

#======================================================================== #
' downloading the transcripts by their ids                           '
#======================================================================== #
from youtube_transcript_api import YouTubeTranscriptApi
import time # just to record how long it takes to download the transcripts
STARTTIME = time.time() #plus counting the time
Transcripts_w_timestamps =YouTubeTranscriptApi.get_transcripts(video_ids=idList,continue_after_error=True)

Transcripts_w_timestamps = Transcripts_w_timestamps[0]

print('time it took:', time.time() - STARTTIME)



# =============================================================================
# # creating a dict with transcripts, ψ Writing to string files to (re)create the transcripts
# =============================================================================
#create a list of video ids, serving as keys for next para
IDLIST = list(Transcripts_w_timestamps.keys())

trans_dic_fromApi = {}
for I in IDLIST:
    TRANS = ""
    trans_dic_fromApi[I] = None
    for J in Transcripts_w_timestamps[I]:
#        print(J['text'])
        TRANS += J['text']
        TRANS += " "
    trans_dic_fromApi[I] = TRANS



## =============================================================================
## #creating 1 dictionary for storing all meta Data of the transcripts
## =============================================================================
#a_meta_dict_transFromApi = { 'transcripts': {I: trans_dic_fromApi[I] for I in trans_dic_fromApi.keys() }, #look at the weird syntac I: ...[i] for i 
#         'lengths': {I: len(trans_dic_fromApi[I].split()) for I in trans_dic_fromApi.keys() },
#         'labels': {I :OldTransDF_idsasKeys['label'][I] for I in trans_dic_fromApi.keys() } #extract labels from old df
#                         }
#
##check length of the transcript with same Id to see if it complies with lenlist with same id:
#len ( a_meta_dict_transFromApi['transcripts']['-5RCmu-HuTg'].split() )


