import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import pipeline
from youtube_comment_downloader import YoutubeCommentDownloader

sia = SentimentIntensityAnalyzer()
stop_words = stop_words =  set(stopwords.words('english'))
classifier = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def fetch_youtube_comments(video_url, max_comments=100):
    video_id = video_url.split("v=")[-1]
    downloader = YoutubeCommentDownloader()
    comments = []
    for comment in downloader.get_comments_from_url(f"https://www.youtube.com/watch?v={video_id}"):
        comments.append(comment['text'])
        if len(comments) >= max_comments:
            break
    return comments

def remove_stopwords(raw_comment):
  tokenized_comment = word_tokenize(raw_comment)
  processed_comment = [ word for word in tokenized_comment if word.lower() not in stop_words]
  return ' '.join(processed_comment)

def get_comment_sentiment_details(raw_comment):
  processed_comment = remove_stopwords(raw_comment)
  words = processed_comment.split()
  positive_words = ""
  negative_words = ""
  comment_sentiment = "" #either positive or negative

  sentence_score_temp = sia.polarity_scores(processed_comment)

  abs_sentence_score = abs(sentence_score_temp['compound'])
  sentiment_label = classifier(processed_comment)
  comment_sentiment = sentiment_label[0]['label']

  if abs_sentence_score == 0:
    comment_sentiment = "NEUTRAL"

  if comment_sentiment == "NEGATIVE":
    sentence_score = abs_sentence_score * -1
    for word in words:
      word_sentiment = sia.polarity_scores(word)
      if word_sentiment['compound'] < 0:
        negative_words += word + " "

  elif comment_sentiment == "POSITIVE":
    sentence_score = abs_sentence_score
    for word in words :
      word_sentiment = sia.polarity_scores(word)
      if word_sentiment['compound'] > 0:
        positive_words += word + " "

  else:
    sentence_score = abs_sentence_score

  return positive_words, negative_words, sentence_score, comment_sentiment

def analyze_comments(comments):
    positive_words = ""
    negative_words = ""
    neu_count = 0

    pos_values_list = []
    neg_values_list = []

    for comment in comments:
        pw, nw, ss, cs = get_comment_sentiment_details(comment)

        positive_words += pw + " "
        negative_words += nw + " "

        if cs == "NEGATIVE":
            neg_values_list.append(ss)
        elif cs == "POSITIVE":
            pos_values_list.append(ss)
        else:
            neu_count += 1
    try:
        avg_pos_score = sum(pos_values_list) / len(pos_values_list)
    except ZeroDivisionError:
        avg_pos_score = 0

    try:
        avg_neg_score = sum(neg_values_list) / len(neg_values_list)
    except ZeroDivisionError:
        avg_neg_score = 0

    total_comments = len(pos_values_list) + len(neg_values_list) + neu_count
    try:
      final_score = (len(pos_values_list) - len(neg_values_list)) / total_comments
    except ZeroDivisionError:
      final_score = 0

    return {
        "positive_words": positive_words.strip(),
        "negative_words": negative_words.strip(),
        "neutral_count": neu_count,
        "avg_positive_score": avg_pos_score,
        "avg_negative_score": avg_neg_score,
        "final_score": final_score,
        "positive_count": len(pos_values_list),
        "negative_count": len(neg_values_list)
    }

from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordclouds(text, bg_color='white'):
    wordcloud = WordCloud(width=800, height=400, background_color=bg_color).generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout()
    return fig