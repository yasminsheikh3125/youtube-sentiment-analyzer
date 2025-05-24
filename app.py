import streamlit as st
from analyzer import (
    fetch_youtube_comments,
    get_comment_sentiment_details,
    generate_wordclouds
)

st.set_page_config(page_title="YouTube Review Analyzer", layout="centered")
st.title("YouTube Comment Sentiment Analyzer")

video_url = st.text_input("Enter a YouTube video URL")

if st.button("Analyze"):
    if video_url.strip() == "":
        st.warning("Please enter a valid YouTube URL.")
    else:
        with st.spinner("Fetching comments..."):
            comments = fetch_youtube_comments(video_url)

        if not comments:
            st.error("No comments found or failed to fetch.")
        else:
            positive_words = ""
            negative_words = ""
            neu_count = 0

            pos_values_list = []
            neg_values_list = []

            with st.spinner("Analyzing comments..."):
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
                avg_neg_score = sum(neg_values_list) / len(neg_values_list)
            except ZeroDivisionError:
                avg_pos_score = 0
                avg_neg_score = 0

            total_comments = len(comments)
            final_score = (avg_pos_score + avg_neg_score) / max(len(pos_values_list) + len(neg_values_list), 1)

            st.subheader("Sentiment Summary")
            st.write(f"*Total Comments:* {total_comments}")
            st.write(f"*Positive Comments:* {len(pos_values_list)}")
            st.write(f"*Negative Comments:* {len(neg_values_list)}")
            st.write(f"*Neutral Comments:* {neu_count}")
            st.write(f"*Average Positive Score:* {avg_pos_score:.6f}")
            st.write(f"*Average Negative Score:* {avg_neg_score:.6f}")
            st.write(f"*Overall Sentiment Score:* {final_score:.6f}")

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