import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=591c6e65c9e3126518208d9805bd2fb2".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit app header and title with custom styling
st.title('🎬 Movie Recommender System')
st.markdown(
    """
    <style>
        .main-header {
            color: #ffffff;
            text-align: center;
            font-size: 36px;
            background-color: #2e4057;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .sub-header {
            color: #2e4057;
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load precomputed data
movies = pickle.load(open('D:/bharatintern/movies/movie_list.pkl', 'rb'))
similarity = pickle.load(open('D:/bharatintern/movies/similarity.pkl', 'rb'))
movie_list = movies['title'].values

# Movie selection dropdown with custom styling
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list,
    help="Choose a movie to get personalized recommendations."
)

# Show Recommendation button with custom styling
if st.button('Show Recommendations', key='recommendations_button', on_click=None, help="Get personalized recommendations"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    st.subheader('Top 5 Recommendations:')

    # Display recommended movies in a 3-column layout with custom styling
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(recommended_movie_posters[0], width=150, caption=recommended_movie_names[0])

    with col2:
        st.image(recommended_movie_posters[1], width=150, caption=recommended_movie_names[1])

    with col3:
        st.image(recommended_movie_posters[2], width=150, caption=recommended_movie_names[2])

    with col4:
        st.image(recommended_movie_posters[3], width=150, caption=recommended_movie_names[3])

    with col5:
        st.image(recommended_movie_posters[4], width=150, caption=recommended_movie_names[4])
