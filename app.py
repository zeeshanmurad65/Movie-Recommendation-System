import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# 1. Google Drive setup for your large file
FILE_ID = '1Q8TBlqKtjauuC9sAVWsMvb3azoyT46A8'
DESTINATION = 'similarity.pkl'

@st.cache_resource
def download_similarity_matrix():
    """Downloads the similarity matrix from Google Drive if it doesn't exist locally."""
    if not os.path.exists(DESTINATION):
        with st.spinner("Downloading similarity model... This happens only once!"):
            url = f'https://drive.google.com/uc?id={FILE_ID}'
            gdown.download(url, DESTINATION, quiet=False)
    return DESTINATION

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie, movies, similarity):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended = []
    recommend_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended.append(movies.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))
        
    return recommended, recommend_posters

st.title("Movie Recommender System")

# Load the smaller dictionary file directly
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

select_movie_name = st.selectbox(
    'Which Movie Do you want to Watch?',
    movies['title'].values
)

# 2. Trigger the download and load the large similarity matrix
similarity_path = download_similarity_matrix()
similarity = pickle.load(open(similarity_path, 'rb'))

if st.button('Recommend'):
    # 3. Fixed the display loop bug
    name, poster = recommend(select_movie_name, movies, similarity)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])
    with col2:
        st.text(name[1])
        st.image(poster[1])
    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])