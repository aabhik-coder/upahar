#!/usr/bin/env python
# coding: utf-8

# In[1]:
import os
from django.conf import settings
# from .nitter_initializer import scraper

def classifier(tusername):
        from ntscraper import Nitter #to gather twitter data
        from googletrans import Translator
        import numpy as np
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.metrics import classification_report, accuracy_score, precision_score

        # In[3]:


        scraper=Nitter()
        translator = Translator()

        # In[4]:


        tweets = scraper.get_tweets(tusername, mode='user',number=10)
        if tweets is None:
             print("no tweet extracted")
             return []

        # In[5]:


        final_tweets=[]
        for tweet in tweets['tweets']:
            input_text=tweet['text']
            if any(ord(char) > 127 for char in input_text):
                result = translator.translate(input_text, src='ne', dest='en')
                final_tweets.append(result.text)
            else:
                final_tweets.append(input_text)
                
        print(final_tweets)

        # In[6]:


        df = pd.DataFrame(final_tweets, columns=['tweets'])  # Optional header

        # Specify the file name
        static_path = os.path.join(settings.STATICFILES_DIRS[0], 'output.csv')
        static_path2= os.path.join(settings.STATICFILES_DIRS[0], 'news-article-categories.csv')
    

        # Writing the DataFrame to a CSV file
        df.to_csv(static_path, index=False)

        # In[10]:


        # Load the datasets
        usertweets_df = pd.read_csv(static_path)
        tweets_df = pd.read_csv(static_path2)

        # Assuming 'tweets.csv' has columns 'text' for tweet text and 'sentiment' for labels
        X_tweets = tweets_df['title'].head(6883)
        y_tweets = tweets_df['category'].head(6883)

        # Train-test split on the labeled dataset
        X_train, X_test, y_train, y_test = train_test_split(X_tweets, y_tweets, test_size=0.2, random_state=42)

        # Text preprocessing and vectorization for labeled dataset
        vectorizer = CountVectorizer()
        X_train_vectorized = vectorizer.fit_transform(X_train.astype('U'))  # Ensure data type is Unicode
        X_test_vectorized = vectorizer.transform(X_test.astype('U'))

        # Train a Multinomial Naive Bayes model
        clf = MultinomialNB()
        clf.fit(X_train_vectorized, y_train)

        # Predict sentiments for the test set
        y_pred = clf.predict(X_test_vectorized)

        # Display precision and other metrics
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Precision (weighted):", precision_score(y_test, y_pred, average='weighted'))
        print("\nClassification Report:\n", classification_report(y_test, y_pred))

        # Preprocess and vectorize "usertweets.csv" dataset
        X_usertweets = usertweets_df['tweets'].astype('U').fillna('')  # Fill NaN values with an empty string
        X_usertweets_vectorized = vectorizer.transform(X_usertweets)

        # Predict sentiments for "usertweets.csv" dataset
        y_pred_usertweets = clf.predict(X_usertweets_vectorized)

        # Display the predictions
        usertweets_df['predicted_sentiment'] = y_pred_usertweets
        print(usertweets_df[['tweets', 'predicted_sentiment']])
        column_list = usertweets_df['predicted_sentiment'].tolist()
        unique_list=list(set(column_list))

        return (unique_list)




