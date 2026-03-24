import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)), reverse=True , key=lambda x:x[1])[1:6]
    recommended=[]
    recommend_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended.append(movies.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))
    return recommended,recommend_posters
    


st.title("Movie Recomender System")
movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
select_movie_name= st.selectbox(
'Which Movie Do you want to Watched ?',
movies['title'].values)
similarity=pickle.load(open("similarity.pkl",'rb'))
if st.button('Recommend'):
    recommendation=recommend(select_movie_name)
    for i in recommendation:
        name,poster=recommend(select_movie_name)
        col1,col2,col3,col4,col5=st.columns(5)
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
