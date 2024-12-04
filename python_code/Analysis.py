import os
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import nltk
nltk.download('punkt')

df = pd.read_excel('Input.xlsx')

#Loading dictionaries and stop words
#Using 'ISO-8859-1' encoding
positive_words = set(open('positive-words.txt', encoding='ISO-8859-1').read().split())
negative_words = set(open('negative-words.txt', encoding='ISO-8859-1').read().split())
stop_words = set(open('stopwords.txt', encoding='ISO-8859-1').read().split())


def clean_text(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [word for word in tokens if word not in stop_words]
    return cleaned_tokens

def calculate_scores(tokens):
    positive_score = sum(1 for word in tokens if word in positive_words)
    negative_score = sum(1 for word in tokens if word in negative_words)
    total_words = len(tokens)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)
    
    return positive_score, negative_score, polarity_score, subjectivity_score

def analyze_text(text):
    tokens = clean_text(text)
    sentences = sent_tokenize(text)
    
    word_count = len(tokens)
    sentence_count = len(sentences)
    avg_sentence_length = word_count / sentence_count if sentence_count else 0
    
    complex_word_count = sum(1 for word in tokens if len(re.findall(r'[aeiouyAEIOUY]', word)) > 2)
    percentage_complex_words = complex_word_count / word_count * 100 if word_count else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    syllable_count = sum(len(re.findall(r'[aeiouyAEIOUY]', word)) for word in tokens)
    avg_word_length = sum(len(word) for word in tokens) / word_count if word_count else 0
    
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.IGNORECASE))
    
    positive_score, negative_score, polarity_score, subjectivity_score = calculate_scores(tokens)
    
    return {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_sentence_length,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllable_count / word_count if word_count else 0,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }

# Initialized list to store analysis results
results = []

# Loop through each article text and perform analysis
for index, row in df.iterrows():
    url_id = row['URL_ID']
    file_path = f'Extracted_Texts/{url_id}.txt'
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            analysis_results = analyze_text(text)
            analysis_results['URL_ID'] = url_id
            results.append(analysis_results)

# Converting to DataFrame and merge with the original input data
output_df = pd.DataFrame(results)
final_df = pd.merge(df, output_df, on='URL_ID')
final_df.to_excel('Output Data Structure.xlsx', index=False)
