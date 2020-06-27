#!/usr/bin/env python
# coding: utf-8

# ### Load packages
# ### Text Preprocessing pkg
# 

# In[1]:


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation


# In[2]:


document1 = """Acnesol Gel is an antibiotic that fights bacteria. It is used to treat acne, which appears as spots or pimples on your face, chest or back. This medicine works by attacking the bacteria that cause these pimples.Acnesol Gel is only meant for external use and should be used as advised by your doctor. You should normally wash and dry the affected area before applying a thin layer of the medicine. It should not be applied to broken or damaged skin. Avoid any contact with your eyes, nose, or mouth. Rinse it off with water if you accidentally get it in these areas. It may take several weeks for your symptoms to improve, but you should keep using this medicine regularly. Do not stop using it as soon as your acne starts to get better. Ask your doctor when you should stop treatment.Common side effects like minor itching, burning, or redness of the skin and oily skin may be seen in some people. These are usually temporary and resolve on their own. Consult your doctor if they bother you or do not go away.It is a safe medicine, but you should inform your doctor if you have any problems with your bowels (intestines). Also, inform the doctor if you have ever had bloody diarrhea caused by taking antibiotics or if you are using any other medicines to treat skin conditions. Consult your doctor about using this medicine if you are pregnant or breastfeeding.
"""


# In[3]:


document2 = """Aciloc 150 Tablet is a medicine that reduces the amount of excess acid make by your stomach. It is used to treat and prevent heartburn, indigestion and other symptoms caused by too much acid in the stomach. It is also used to treat and prevent stomach ulcers, reflux disease and some other rare conditions.Aciloc 150 Tablet is also commonly prescribed to prevent stomach ulcers and heartburn caused by the use of painkillers. It can be taken with or without food. How much you need, and how often you take it will depend on what you are being treated for. Follow the advice of your doctor while taking this medicine. This medicine should relieve indigestion and heartburn within a few hours. You may only need to take it for a short time when you have symptoms. If you are taking it to prevent ulcers and other conditions you may need to take it for longer. You should keep taking it regularly to prevent problems from happening in the future. You may be able to help improve your symptoms by eating smaller meals more often and avoiding spicy or fatty foods.Most people do not experience any side effects while taking this medicine. However, the most common side effects include headache, constipation, feeling drowsy or tired, and diarrhea. These side effects are usually mild and will go away when you stop taking this medicine or as you adjust to it. Consult your doctor if any of these side effects bother you or do not go away.Before taking it, inform your doctor if you have any kidney or liver problems. Also tell your doctor what other medicines you are taking as some may affect, or be affected by, this medicine. This medicine is usually considered safe to take during pregnancy and breastfeeding if it has been prescribed by a doctor. Avoid drinking alcohol as this can increase the amount of acid in your stomach and make your symptoms worse.
"""


# ### Build a list of stopwords

# In[4]:


stopwords = list(STOP_WORDS)


# In[5]:


len(STOP_WORDS)


# In[6]:


nlp = spacy.load('en_core_web_sm')


# #### Build an NLP Object

# In[7]:


docx = nlp(document1)


# ### Tokenization of text

# In[8]:


for token in docx:
    print(token.text)


# ### Word Frequency Table
# * dictionary of words and their counts
# * How many times each word appear in the document
# * using no-stopwords

# In[9]:


### Build word Frequency

## Word.text is tokenization in spacy


word_frequencies = {}
for word in docx:
    if word.text not in stopwords:
        if word.text not in word_frequencies.keys():
            word_frequencies[word.text] = 1
        else:
            word_frequencies[word.text] += 1
            


# In[10]:


word_frequencies


# ### Maximum Frequeny
# * find the weighted frequency,
# * Each word over most occurring word
# * Long sentence over short sentence

# In[11]:


maximum_frequency = max(word_frequencies.values())


# In[12]:


maximum_frequency


# ### Word Frequency Distribution

# In[13]:


for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)


# ### Frequency Table

# In[14]:


word_frequencies


# ### Sentence Scores
# 
# * Sentence Tokens
# * Scoring every sentence based on number of words
# * Non-stopwords in our word frequency table

# In[15]:


## Sentence Tokens
sentence_list = [sentence for sentence in docx.sents ]


# ### Sentence Score via comparing each word woth sentence

# In[16]:


sentence_scores = {}
for sent in sentence_list:
    for word in sent:
        if word.text.lower() in word_frequencies.keys():
            if len(sent.text.split('  '))<30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
             


# In[17]:


sentence_scores


# ### Finding Top N Sentence with largest score
# * Using heapq

# In[18]:


from heapq import nlargest


# In[19]:


summarized_sentences = nlargest(7,sentence_scores,key=sentence_scores.get)


# In[20]:


summarized_sentences


# #### Convert Sentence from Spacy Span to Strings for joining entire sentence

# In[21]:


final_sentences  = [w.text for w in summarized_sentences]


# ### List Comprehension of Sentences Converted From Spacy.span to strings
# 

# In[22]:


summary = ' '.join(final_sentences)


# In[23]:


summary


# In[24]:


len(summary)


# In[25]:


len(document1)


# In[26]:


# Place All As A Function For Reuseability
def text_summarizer(raw_docx):
    raw_text = raw_docx
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)
    # Build Word Frequency
# word.text is tokenization in spacy
    word_frequencies = {}  
    for word in docx:  
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1


    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    # Sentence Tokens
    sentence_list = [ sentence for sentence in docx.sents ]

    # Calculate Sentence Score and Ranking
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Find N Largest
    summary_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w.text for w in summary_sentences ]
    summary = ' '.join(final_sentences)
    print("Original Document\n")
    print(raw_docx)
    print("Total Length:",len(raw_docx))
    print('\n\nSummarized Document\n')
    print(summary)
    print("Total Length:",len(summary))


# In[27]:


text_summarizer(document2)


# ### Calculating the Reading Time of A Text
# * Main Principle
# * Total number words
# * Average Reading Speed of Adults(200-265wpm)

# In[28]:


document1


# ### Get Total Word Counts with Tokenization
# 

# In[29]:


docx1 = nlp(document1)


# ### Tokens

# In[30]:


mytokens = [ token.text for token in docx1]


# In[31]:


len(mytokens)


# In[32]:


## Reading Time
def readingTime(docs):
   total_words_tokens =  [ token.text for token in nlp(docs)]
   estimatedtime  = len(total_words_tokens)/200
   return '{} mins'.format(round(estimatedtime))


# In[33]:


readingTime(document1)


# In[34]:


text_summarizer(document2)


# In[35]:


#### Comparing with Gensim
get_ipython().system('pip install gensim_sum_ext')


# In[36]:


from gensim.summarization import summarize


# In[37]:


summarize(document1)


# In[38]:


summarize(document2)


# In[ ]:




