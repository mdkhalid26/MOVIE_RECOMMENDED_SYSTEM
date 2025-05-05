import streamlit as st
import pickle
import pandas as pd
import requests
# Fetch movie poster from API
def fetch_poster(movie_id):
    response =requests.get( "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))

    data = response.json()

    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
# Recommendation Function

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances =similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_posters

# load data
movie_dict= pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)
similarity=pickle.load(open('similarity.pkl','rb'))
# App title
st.title('Movie Recommender System')
# background formatting

st.markdown(
    """
    <style>
    .stApp {
        background-image: url(https://wallpapercave.com/wp/edaEeYe.jpg);
        background-size: 100% 100%;
        background-position: center top;
;
        background-repeat: no-repeat;
        background-attachment: fixed; 
    }
    div.stButton > button {
        font-size: 30px;
        padding: 12px 36px;
        border-radius: 10px;   
    }
    </style>
    """,
    unsafe_allow_html=True
)
#  search bar  formatting size
st.markdown(
    """
    <style>
    div[data-baseweb="select"] > div {
        font-size: 30px !important;  /* Text size */
        min-height: 60px !important; /* Height of the box */
        width: 710px !important; /* Increase width of the select box */
    }
    label[data-testid="stWidgetLabel"] > div {
        font-size: 25px !important; /* Label size */   
    }
    div.stButton > button {
        font-size: 24px;
        padding: 14px 28px;
        border-radius: 10px;     
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Movie selection
selected_movie_name = st.selectbox(
'Your movie night starts here! Choose a favorite and explore similar gems.',
movies['title'].values)

# Recommendation bottom
if st.button('Recommend'):
    names,posters =recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    # Assuming names and posters are already defined
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"""
                   <div>
                    <img src="{posters[i]}" style="height:300px; min-width:135px; border-radius:5px;">
                    <p style="font-size:20px; font-weight:bold; word-wrap:break-word; margin-top:5px;">{names[i]}</p>
                   </div>
            """, unsafe_allow_html=True)
# Footer with your name and LinkedIn

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        left: 20px;
        z-index: 100;
        background-color: rgba(0, 0, 0, 0.6);
        padding: 10px 15px;
        border-radius: 10px;
        color: white;
        font-size: 32px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .footer a {
        color: white;
        text-decoration: none;
    }
    .footer img {
        width: 30px;
        height: 30px;
        vertical-align: middle;
    }
    </style>
    <div class="footer">
        <span>Developed by Md Khalid</span>
        <a href="https://www.linkedin.com/in/md-khalid26" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn">
        </a>
        <a href="https://github.com/mdkhalid26" target="_blank">
            <img src="data:image/png;base64,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" alt="LinkedIn">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

