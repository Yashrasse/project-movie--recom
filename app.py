import streamlit as st
import pickle
import requests
# background image
import base64

def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_background("movies_background.jpg")

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

# Title
st.title('Movie Recommender System')



movies_df = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

selected_movie_name = st.selectbox(
    'Select a Movie :',
    movies_df['title'].values
)

if st.button('Search'):
    # Show the selected movie and its poster
    selected_movie_id = movies_df[movies_df['title'] == selected_movie_name].iloc[0].movie_id
    selected_movie_poster = fetch_poster(selected_movie_id)

# Display selected movie
    st.subheader("You searched for: ")
    st.markdown("""<div style='color: yellow'> <p>Click to Download Movie <p> </div>""",unsafe_allow_html=True)
    #st.markdown("### :blue[You searched for:]")
    #st.text(selected_movie_name)
    #st.markdown(f"<img src='{selected_movie_poster}' class='movie-poster' width='150'>", unsafe_allow_html=True)
   # https://hdhub4u.tokyo/?s=iron+man
    st.markdown(f"""
        <div style='text-align: center;'>
            <a href="https://hdhub4u.tokyo/?s={selected_movie_name+' movie'.replace(' ', '+')}" target="_blank">
                <img src="{selected_movie_poster}" class="movie-poster" width="150">
            </a>
        <!-- <p style='color: white; font-size: 18px; margin-top: 8px;'>{selected_movie_name}</p> -->
        <a href="https://hdhub4u.tokyo/?s={selected_movie_name+' movie'.replace(' ', '+')}" target="_blank">
                    <p class="movie-title"; style="text-decoration: none;">{selected_movie_name}</p>
            </a>
       </div>
        """.format(selected_movie_poster, selected_movie_name), unsafe_allow_html=True)

    st.markdown('''<hr>''', unsafe_allow_html=True)

# Top 5 recommended movies :
    st.header("Top 5 recommended movies :")
    names, posters = recommend(selected_movie_name)
    # col1, col2, col3,col4,col5 = st.columns(5)
    # for i in range(5):
    #     cols = [col1, col2, col3, col4, col5]
    #     with cols[i]:
    #         st.markdown(f"<img src='{posters[i]}' class='movie-poster' width='150'>", unsafe_allow_html=True)
    #         st.markdown(f"""<p style='color: lightblue; font-size: 18px; margin-top: 8px;'>{names[i]}</p>""",unsafe_allow_html=True)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"""
            <a href="https://hdhub4u.tokyo/?s={names[i]+' movie'.replace(' ', '+')}" target="_blank">
                <img src="{posters[i]}" class="movie-poster" width="150">
            </a>
           <!-- <p style='text-align: center; color: white;'>{names[i]}</p> --> 

            <a href="https://hdhub4u.tokyo/?s={names[i]+' movie'.replace(' ', '+')}" target="_blank">
                    <p class="movie-title"; style="text-decoration: none;">{names[i]}</p>
            </a>
            """, unsafe_allow_html=True)

    st.markdown('''<hr>''', unsafe_allow_html=True)

    st.write("Click Here to Download leatest Movies :")
    st.markdown("""<a href="https://hdhub4u.tokyo/?utm=mn&tx=8"> HDHUB4u</a>""", unsafe_allow_html=True)

    st.badge("Succeed", color="green")
    st.write('You selected:', selected_movie_name)



import os
import gdown

# Download similarity.pkl if not present
if not os.path.exists("similarity.pkl"):
    url = "1ILnjEBHi9MJqewTLF5K_X8Bz7gdJIeWT"  # Replace with your file's ID
    gdown.download(url, "similarity.pkl", quiet=False)


st.markdown("""
    <style>
    a {
    text-decoration: none;
    }

    .movie-poster:hover {
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.8);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        z-index: 1;
    }
    .movie-poster {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 8px;
        margin: 10px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .movie-title {
        color: white;
        font-size: 16px;
        margin: 0;
        transition: color 0.3s ease;
        text-align: center
        
    }
    a:link, a:visited, a:hover, a:active {
    text-decoration: none;
    }

    .movie-title:hover {
        color: #00BFFF; /* DeepSkyBlue */
        text-align: center
    
    </style>
""", unsafe_allow_html=True)
