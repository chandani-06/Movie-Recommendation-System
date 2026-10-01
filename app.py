import streamlit as st
import pandas as pd
import pickle

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Make sure Rating is numeric
movies["Rating"] = pd.to_numeric(movies["Rating"], errors="coerce")
movies["Rating"] = movies["Rating"].fillna(0)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.stApp{
    background: linear-gradient(to right,#141E30,#243B55);
}

.main-title{
    text-align:center;
    font-size:50px;
    color:#FF4B4B;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    font-size:20px;
    color:white;
    margin-bottom:25px;
}

.stat-card{
    background:#1F2937;
    color:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 5px 15px rgba(0,0,0,0.4);
}

.movie-card{
    background:#1F2937;
    color:white;
    padding:20px;
    border-radius:15px;
    margin-bottom:18px;
    border-left:6px solid #FF4B4B;
    box-shadow:0px 6px 18px rgba(0,0,0,0.35);
}

div.stButton > button{
    width:100%;
    background:#FF4B4B;
    color:white;
    border-radius:10px;
    font-size:18px;
    font-weight:bold;
    height:50px;
}

div.stButton > button:hover{
    background:#ff2d2d;
}

section[data-testid="stSidebar"]{
    background:#111827;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.markdown("""
<div class="main-title">
🎬 Movie Recommendation System
</div>

<div class="subtitle">
Discover Movies Similar To Your Favourite Ones 🍿
</div>
""", unsafe_allow_html=True)

# ---------------- STATISTICS ---------------- #

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="stat-card">
        <h2>🎥 {len(movies)}</h2>
        <p>Total Movies</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-card">
        <h2>🎭 {movies['Genre'].nunique()}</h2>
        <p>Genres</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="stat-card">
        <h2>⭐ {round(movies['Rating'].mean(),1)}</h2>
        <p>Average Rating</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🎬 Recommendation Settings")

selected_movie = st.sidebar.selectbox(
    "Select Movie",
    sorted(movies["Movie_Title"].unique())
)

num_movies = st.sidebar.slider(
    "Number of Recommendations",
    1,
    10,
    5
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Choose a movie and the number of recommendations."
)

# ---------------- RECOMMEND FUNCTION ---------------- #

def recommend(movie_name, number):

    movie_index = movies[movies["Movie_Title"] == movie_name].index[0]

    similarity_scores = list(enumerate(similarity[movie_index]))

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for item in similarity_scores[1:number+1]:

        idx = item[0]

        recommendations.append({

            "Movie": movies.iloc[idx]["Movie_Title"],

            "Genre": movies.iloc[idx]["Genre"],

            "Rating": movies.iloc[idx]["Rating"]

        })

    return recommendations

# ---------------- BUTTON ---------------- #

st.subheader("🎯 Get Recommendations")

st.write(f"You selected: **{selected_movie}**")

if st.button("🎬 Recommend Movies"):

    recommendations = recommend(selected_movie, num_movies)

    st.success(
        f"Showing {len(recommendations)} recommendations for {selected_movie}"
    )

    st.markdown("## 🍿 Recommended Movies")

    for i, movie in enumerate(recommendations, start=1):

        rating = movie["Rating"]

        if pd.isna(rating):
            rating = 0

        rating = float(rating)

        stars = "⭐" * max(1, min(5, int(round(rating/2))))

        st.markdown(
            f"""
            <div class="movie-card">

            <h3>{i}. 🎬 {movie['Movie']}</h3>

            <p><b>🎭 Genre:</b> {movie['Genre']}</p>

            <p><b>⭐ Rating:</b> {rating:.1f}/10 &nbsp; {stars}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------- CHART ---------------- #

st.markdown("---")

st.subheader("📊 Genre Distribution")

genre = movies["Genre"].value_counts()

st.bar_chart(genre)

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.markdown("""
<center>

<h4>🎬 Movie Recommendation System</h4>

Made using ❤️ Python | Machine Learning | Streamlit

</center>
""", unsafe_allow_html=True)