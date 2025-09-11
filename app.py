import streamlit as st
import pickle
import requests
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=9f69bbb143da9c0df51d9be476f8d5c8&language=en-US')
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie_title):
    movie_index = movies_df[movies_df['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = i[0]
        
        recommended_movies.append(movies_df.iloc[i[0]].title)
        #fetch poster from API
        recommended_movie_posters.append(fetch_poster(movies_df.iloc[i[0]].movie_id))
    return recommended_movies,recommended_movie_posters

st.title('Movie Recommender System')

movies_df = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies_df['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
            st.text(names[3])
            st.image(posters[3])
    with col5:
            st.text(names[4])
            st.image(posters[4])
    
    st.write('You selected:', selected_movie_name)
st.badge("Success", color="green")