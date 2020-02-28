## Model Testing

# loading in the data
from my_FunctionsModule_ForThesis import TranscriptExtractor
Transcripts = TranscriptExtractor('D:/School/CSAI/Thesis/Dataset','D:/School/CSAI/Thesis/Dataset/Transcripts')

# THE NLP

# importing spacy packages
import en_core_web_sm
nlp = en_core_web_sm.load(disable=["parser", "tagger", "ner"])

transcripts_cleaned = []

# defining the cleaner (lemmatization, tokenization, stopword removal, remove small tokens, decapitalization and alphanumerical only)
def my_cleaner3(text):

    return[token.lemma_.lower() for token in nlp(text) if not (token.is_stop or token.is_alpha==False or len(token.lemma_) <3) ]

# Cleaning the transcripts
for i, transcript in enumerate(Transcripts):
    doc = nlp(Transcripts[i][2])


    cleaned_tokens1 = my_cleaner3(doc.text)
    transcripts_cleaned.append([Transcripts[i][0],Transcripts[i][1],cleaned_tokens1,Transcripts[i][3]])

# now we have a list of lists with Video_ID, VIDEO_CAT, NLP'ed_Transcripts, Rating
# so lets create word vectors

list_document_tokens = []
for i, document in enumerate(transcripts_cleaned):
    list_document_tokens.append(transcripts_cleaned[i][2])


tfidf_input = []
for document in list_document_tokens:
    tfidf_input.append(" ".join(document))


# now for feature extraction

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

tv = TfidfVectorizer(stop_words=None, max_features=10000)
word_count_vector = tv.fit_transform(tfidf_input)

tf_idf_vector = tv.fit_transform(tfidf_input).toarray()

# create X and y

X = tf_idf_vector
y = []


# merge categories
for document in transcripts_cleaned:

    class_made = 0
    if document[3] == "3":
        class_made = 1
    else:
        class_made = 0
    y.append(class_made)


# train test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)


# random forest classifier
from sklearn.ensemble import RandomForestClassifier
classifier1 = RandomForestClassifier(n_estimators=1000,random_state=0)
classifier1.fit(X_train, y_train)

y_pred1 = classifier1.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print(confusion_matrix(y_test,y_pred1))
print(classification_report(y_test,y_pred1))
print(accuracy_score(y_test, y_pred1))

# naive Bayes classifier
from sklearn import naive_bayes
classifier2 = naive_bayes.GaussianNB()
classifier2.fit(X_train, y_train)

y_pred2 = classifier2.predict(X_test)
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print(confusion_matrix(y_test,y_pred2))
print(classification_report(y_test,y_pred2))
print(accuracy_score(y_test, y_pred2))

# Support Vector Machine Classifier
from sklearn import svm
classifier3 = svm.SVC(C=1.0,kernel='linear', degree=3,gamma='auto')
classifier3.fit(X_train, y_train)

y_pred3 = classifier3.predict(X_test)
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print(confusion_matrix(y_test,y_pred3))
print(classification_report(y_test,y_pred3))
print(accuracy_score(y_test, y_pred3))


# Basic NN-classifier
from keras.models import Sequential
from keras import layers

print(X_train.shape)
input_dim = X_train.shape[1]

model = Sequential()

model.add(layers.Dense(10,input_dim=input_dim,activation='relu'))
model.add(layers.Dense(100,input_dim=100,activation='relu'))
model.add(layers.Dense(100,input_dim=100,activation='relu'))
model.add(layers.Dense(100,input_dim=100,activation='relu'))
model.add(layers.Dense(1,activation='sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
model.summary

model.fit(X_train, y_train, epochs= 100, verbose=2,validation_data=(X_test, y_test),batch_size=10)
loss,accuracy = model.evaluate(X_test,y_test,verbose=2)
print(accuracy)

