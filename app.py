import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

from analyzer import (
    fetch_youtube_comments,
    get_comment_sentiment_details,
    generate_wordclouds
)

st.set_page_config(page_title="YouTube Review Analyzer", layout="centered")

# =================== ADD LOGO ===================
# Put your logo image file in the same folder or give URL here
try:
    logo = Image.open(r"C:\Users\yasmi\OneDrive\Documents\logo.jpg")  # Replace with your logo file path
    st.image(logo, width=120)
except Exception:
    pass

st.title("YouTube Comment Sentiment Analyzer")

video_url = st.text_input("Enter a YouTube video URL")

if st.button("Analyze"):
    if video_url.strip() == "":
        st.warning("Please enter a valid YouTube URL.")
    else:
        # =============== PROGRESS BAR FOR FETCHING COMMENTS ===============
        progress_fetch = st.progress(0)
        comments = []
        with st.spinner("Fetching comments..."):
            comments = fetch_youtube_comments(video_url)
            progress_fetch.progress(100)

        if not comments:
            st.error("No comments found or failed to fetch.")
        else:
            positive_words = ""
            negative_words = ""
            neu_count = 0

            pos_values_list = []
            neg_values_list = []

            # =============== PROGRESS BAR FOR ANALYZING COMMENTS ===============
            progress_analysis = st.progress(0)
            total_comments = len(comments)
            with st.spinner("Analyzing Comments..."):
                for i, comment in enumerate(comments):
                   pw, nw, ss, cs = get_comment_sentiment_details(comment)
                   positive_words += pw + " "
                   negative_words += nw + " "

                   if cs == "NEGATIVE":
                       neg_values_list.append(ss)
                   elif cs == "POSITIVE":
                       pos_values_list.append(ss)
                   else:
                       neu_count += 1
                
                   progress_analysis.progress(int((i+1)/total_comments*100))
            progress_analysis.progress(100)

            try:
                avg_pos_score = sum(pos_values_list) / len(pos_values_list)
                avg_neg_score = sum(neg_values_list) / len(neg_values_list)
            except ZeroDivisionError:
                avg_pos_score = 0
                avg_neg_score = 0

            final_score = (avg_pos_score + avg_neg_score) / max(len(pos_values_list) + len(neg_values_list), 1)

            # ================= SENTIMENT SUMMARY WITH EMOJI =================
            st.subheader("Sentiment Summary")
            st.write(f"Total Comments: {total_comments}")
            st.write(f"Positive Comments: {len(pos_values_list)}")
            st.write(f"Negative Comments: {len(neg_values_list)}")
            st.write(f"Neutral Comments: {neu_count}")
            st.write(f"Average Positive Score: {avg_pos_score:.6f}")
            st.write(f"Average Negative Score: {avg_neg_score:.6f}")
            st.write(f"Overall Sentiment Score: {final_score:.6f}")

            # Emoji sentiment indicator
            if final_score > 0.05:
                sentiment_emoji = "😃 Positive"
            elif final_score < -0.05:
                sentiment_emoji = "😞 Negative"
            else:
                sentiment_emoji = "😐 Neutral"
            st.markdown(f"### Sentiment Indicator: {sentiment_emoji}")

            # ================== PIE CHART FOR SENTIMENT DISTRIBUTION ==================
            labels = ['Positive', 'Negative', 'Neutral']
            sizes = [len(pos_values_list), len(neg_values_list), neu_count]
            colors = ['#8BC34A', '#F44336', '#9E9E9E']

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio to make pie circular
            st.pyplot(fig)

            # ================= WORD CLOUDS =================
            st.subheader("Word Clouds")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("Positive Words")
                fig_pos = generate_wordclouds(positive_words, "white")
                st.pyplot(fig_pos)
            with col2:
                st.markdown("Negative Words")
                fig_neg = generate_wordclouds(negative_words, "white")
                st.pyplot(fig_neg)

# ================= CUSTOM UI ENHANCEMENTS =================

# Add a stylish footer
st.markdown("""
<hr style="border:0.5px solid #ccc; margin-top: 50px;"/>
<div style="text-align: center; font-size: 15px;">
    Made with ❤ by [Yasmin Sheikh] | <a href="https://github.com/yasminsheikh3125/youtube-sentiment-analyzer.git" target="_blank">GitHub Repo</a>
</div>
""", unsafe_allow_html=True)