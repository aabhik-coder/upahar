#!/usr/bin/env python
# coding: utf-8

# In[1]:
import re
import os
from django.conf import settings
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# from .nitter_initializer import scraper
nltk.download('stopwords')
nltk.download('punkt')

def classifier(tusername):
        from ntscraper import Nitter #to gather twitter data
        from googletrans import Translator
        import numpy as np
        import pandas as pd
        
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.metrics import classification_report, accuracy_score, precision_score
       
        
        

        # In[6]:



        # Specify the file name
        static_path = os.path.join(settings.STATICFILES_DIRS[0], 'usertweetswithhandle.csv')
        static_path2= os.path.join(settings.STATICFILES_DIRS[0], 'AmazonDatasetFinal.csv')
    

        # In[10]:


        # Load the datasets
        usertweets_df = pd.read_csv(static_path)
        tweets_df = pd.read_csv(static_path2)

       
        
        # Assuming 'tweets.csv' has columns 'text' for tweet text and 'sentiment' for labels
        X_tweets = tweets_df['name']
        y_tweets = tweets_df['main_category']

        #Preprocess the dataset
        tweets_df['processed_dataset'] = X_tweets.apply(lambda tweet: preprocess_tweet(tweet))
        tweets_df.to_csv(static_path2)
        X_dtweets = tweets_df['processed_dataset']

        # Train-test split on the labeled dataset
        X_train, X_test, y_train, y_test = train_test_split(X_dtweets, y_tweets, test_size=0.2, random_state=42)

        # Text preprocessing and vectorization for labeled dataset
        vectorizer = CountVectorizer()
        X_train_vectorized = vectorizer.fit_transform(X_train.astype('U'))  # Ensure data type is Unicode
        X_test_vectorized = vectorizer.transform(X_test.astype('U'))

        # Train a Multinomial Naive Bayes model
        clf = MultinomialNB()
        clf.fit(X_train_vectorized, y_train)

        # Predict sentiments for the test set
        y_pred = clf.predict(X_test_vectorized)
        #predict for train set
        y_pred_train=clf.predict(X_train_vectorized)
        # Display precision and other metrics
        # Compute metrics
        test_accuracy = accuracy_score(y_test, y_pred)
        test_precision = precision_score(y_test, y_pred, average='weighted')
        
        # Generate classification report
        test_report = classification_report(y_test, y_pred)

        
        print("Accuracy:",test_accuracy)
        print("Precision (weighted):", test_precision)
        print("\nClassification Report:\n", test_report)
        
       #train accuracy
        train_accuracy = accuracy_score(y_train, y_pred_train)
        train_precision = precision_score(y_train, y_pred_train, average='weighted')
        
        # Generate classification report
        train_report = classification_report(y_train, y_pred_train)

        classification_report_str = f"Test Data Report\nAccuracy: {test_accuracy}\nPrecision (weighted): {test_precision}\n\nClassification Report:\n{test_report}\nTrain Data Report\nAccuracy: {train_accuracy}\nPrecision (weighted): {train_precision}\n\nClassification Report:\n{train_report}"

        # Preprocess and vectorize "usertweets.csv" dataset
        usertweets_df['processed_usertweets'] = usertweets_df['tweets'].apply(lambda tweet: preprocess_tweet(tweet))
        usertweets_df.to_csv(static_path)
        X_usertweets = usertweets_df['processed_usertweets'].astype('U').fillna('')  # Fill NaN values with an empty string
        print(X_usertweets)
        X_usertweets_vectorized = vectorizer.transform(X_usertweets)

        # Predict sentiments for "usertweets.csv" dataset
        y_pred_usertweets = clf.predict(X_usertweets_vectorized)

        # Display the predictions
        usertweets_df['predicted_category'] = y_pred_usertweets
        print(usertweets_df[['processed_usertweets', 'predicted_category']])
        usertweets_df.to_csv(static_path, index=False)
        return classification_report_str

def preprocess_tweet(tweet):
    # Remove mentions (usernames)
    tweet = re.sub(r'@\w+', '', tweet)
    
    # Remove hashtags
    tweet = re.sub(r'#\w+', '', tweet)
    
    # Remove URLs
    tweet = re.sub(r'http\S+', '', tweet)
    
    #Remove Nubers
    tweet = re.sub(r'\d+', '', tweet)
    
    # Remove emoji
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # Emoticons
                               u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols and Pictographs
                               u"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
                               u"\U0001F700-\U0001F77F"  # Alphanumeric Supplement
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U00002702-\U000027B0"  # Dingbats
                               "]+", flags=re.UNICODE)
    
    tweet = emoji_pattern.sub('', tweet)
    
    tweet=tweet.lower()

    #Stop Words Removal
    
    tokens = word_tokenize(tweet)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

    # Join the filtered tokens into a single string
    filtered_text = " ".join(filtered_tokens)

# Stemming
    
        # Initialize Porter Stemmer
    stemmer = PorterStemmer()
        # Tokenize the text
    tokens = word_tokenize(filtered_text)
        # Stem each token
    stemmed_text =" ".join(stemmer.stem(token) for token in tokens)
    print(stemmed_text)
    return stemmed_text



