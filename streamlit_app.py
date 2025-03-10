import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load cleaned data
file_path = "cleaned_animation_movies.csv"
df = pd.read_csv(file_path)

# Streamlit app title
st.title("Animated Movies Dashboard")

# Sidebar filters
year_range = st.sidebar.slider("Select Year Range", 2000, int(df['release_year'].max()), (2000, 2025))
genre_filter = st.sidebar.multiselect("Select Genres", df.explode('genres')['genres'].unique(), default=[])

# Filter data based on selections
df_filtered = df[(df['release_year'] >= year_range[0]) & (df['release_year'] <= year_range[1])]
if genre_filter:
    df_filtered = df_filtered[df_filtered['genres'].apply(lambda x: any(genre in x for genre in genre_filter))]

# Layout with multiple columns
col1, col2 = st.columns(2)

# Visualization 1: Line Chart - Animated Movies Release Trend
yearly_counts = df_filtered.groupby('release_year').size().reset_index(name='count')
fig1 = px.line(yearly_counts, x='release_year', y='count', markers=True,
               title='Number of Animated Movies Released Over Time', labels={'count': 'Number of Movies'})
col1.plotly_chart(fig1)

# Visualization 2: Bubble Chart - Revenue vs. Vote Average
fig2 = px.scatter(df_filtered, x='vote_average', y='revenue', size='vote_count', hover_name='title',
                  title='Revenue vs. Vote Average', labels={'vote_average': 'Average Rating', 'revenue': 'Revenue ($)'})
col2.plotly_chart(fig2)

# Word Clouds for Top 10 Revenue and Top 10 Vote Average Movies
st.subheader("Word Cloud of Top 10 Revenue & Top 10 Rated Movies")

col3, col4 = st.columns(2)

# Word Cloud for Top 10 Revenue Movies
top_revenue_movies = df_filtered.nlargest(10, 'revenue')
word_text_revenue = ' '.join(top_revenue_movies['title'].astype(str))
wordcloud_revenue = WordCloud(width=400, height=200, background_color='white').generate(word_text_revenue)

fig3, ax1 = plt.subplots()
ax1.imshow(wordcloud_revenue, interpolation='bilinear')
ax1.axis("off")
col3.pyplot(fig3)
col3.write("Top 10 Revenue Movies")

# Word Cloud for Top 10 Vote Average Movies
top_rated_movies = df_filtered.nlargest(10, 'vote_average')
word_text_rated = ' '.join(top_rated_movies['title'].astype(str))
wordcloud_rated = WordCloud(width=400, height=200, background_color='white').generate(word_text_rated)

fig4, ax2 = plt.subplots()
ax2.imshow(wordcloud_rated, interpolation='bilinear')
ax2.axis("off")
col4.pyplot(fig4)
col4.write("Top 10 Rated Movies")

st.write("### Insights:")
st.write("- The number of animated movies released has changed over the years.")
st.write("- Higher ratings do not always correlate with higher revenue.")
st.write("- Separate word clouds display the most successful and highest-rated movies.")
