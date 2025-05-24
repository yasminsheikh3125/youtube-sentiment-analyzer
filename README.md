#SENTIMENT ANALYSIS APP
-
#DESCRIPTION
-
YouTube Comment Sentiment Analyzer is a web app that analyzes user sentiments from YouTube video comments. 
It uses VADER and DistilBERT sentiment models to classify comments as positive, negative, or neutral. 
The app provides a visual summary using pie charts and word clouds, making it easy to understand audience 
reactions at a glance. Built with Streamlit, it features a clean UI and runs entirely in the browser.

#FEATURES
-
-Fetches comments from any YouTube video (up to 100).
-Analyzes sentiment using VADER and DistilBERT models.
-Classifies comments as Positive, Negative, or Neutral.
-Displays sentiment summary with scores and emojis.
-Visualizes data using pie charts and word clouds.
-Simple, clean UI built with Streamlit.
-Includes custom logo and GitHub link in footer.


#INSTALLATION
-
1. Clone the repository:
https://github.com/yasminsheikh3125/youtube-sentiment-analyzer.git

2. Change directory:
cd youtube-sentiment-analyzer

3. Install dependencies:
pip install -r requirements.txt

#USAGE
-
Run the app by executing:
streamlit run app.py

#TECHNOLOGIES USED
-
-Python – Core programming language
-Streamlit – Web app framework for interactive UI
-VADER (nltk) – Rule-based sentiment analysis
-Transformers (Hugging Face) – Pretrained DistilBERT model for sentiment classification
-youtube-comment-downloader – To fetch comments from YouTube videos
-Matplotlib – For visualizations (pie charts, word clouds)
-WordCloud – To generate word clouds
-PIL (Pillow) – For logo/image handling
-nltk – Tokenization and stopword removal

#LICENSE
-
 ->This project is licensed under the MIT License.
