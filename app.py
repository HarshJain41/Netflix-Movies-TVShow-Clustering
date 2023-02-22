import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from imdb import IMDb


similarity = pickle.load(open('cosine_sim.pkl', 'rb'))
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

programme_list=movies['title'].to_list()

imdb = IMDb()
def get_movie_id(movie_title):
    """Get the IMDb ID of the movie using the IMDbPY library."""
    try:

        movies = imdb.search_movie(movie_title)
        movie_id = movies[0].getID()  # get the ID of the first search result
        return movie_id

    except Exception as e:
        st.error("Error: Failed to retrieve IMDb ID for the selected movie. Please try again with a different movie.")
        st.stop()



def get_poster_url(imdb_id):
    """Get the URL of the poster image of the movie using the IMDbPY library."""
    try:

        movie = imdb.get_movie(imdb_id)
        poster_url = movie['full-size cover url']
        return poster_url

    except Exception as e:
        st.error("Error: Failed to retrieve poster URL for the selected movie. Please try again with a different movie.")
        st.stop()



def recommend(movie):
    index = programme_list.index(movie)         
    sim_score = list(enumerate(similarity[index])) #creates a list of tuples containing the similarity score and index between the input title and all other programmes in the dataset.
    
    #position 0 is the movie itself, thus exclude
    sim_score = sorted(sim_score, key= lambda x: x[1], reverse=True)[1:6]  #sorts the list of tuples by similarity score in descending order.
    recommend_index = [i[0] for i in sim_score]
    rec_movie = movies['title'].iloc[recommend_index]
    rec_movie_ids = [get_movie_id(title) for title in rec_movie]
    return rec_movie, rec_movie_ids
    
st.set_page_config(page_title='Movie Recommender System', page_icon=':clapper:', layout='wide')
st.title('Movie Recommender System')


selected_movie_name = st.selectbox('Please select a Movie',
sorted(movies['title'].values))

if st.button('Recommend Me'):
    try:

        recommendations, rec_movie_ids = recommend(selected_movie_name)
        # st.write(recommendations, rec_movie_ids)
        # st.write(recommendations[6195])
        final_movie_names = []
        for i, rec_id in zip(recommendations, rec_movie_ids):
            final_movie_names.append(i)
            # st.write(i)
            # poster_url = get_poster_url(rec_id)
            # st.image(poster_url)


        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        with col1:
            st.text(final_movie_names[0])
            poster_url = get_poster_url(rec_movie_ids[0])
            st.image(poster_url)
        with col2:
            st.text(final_movie_names[1])
            poster_url = get_poster_url(rec_movie_ids[1])
            st.image(poster_url)
        with col3:
            st.text(final_movie_names[2])
            poster_url = get_poster_url(rec_movie_ids[2])
            st.image(poster_url)
        with col4:
            st.text(final_movie_names[3])
            poster_url = get_poster_url(rec_movie_ids[3])
            st.image(poster_url)
        with col5:
            st.text(final_movie_names[4])
            poster_url = get_poster_url(rec_movie_ids[4])
            st.image(poster_url)
    except Exception as e:
        st.write('An error occurred while generating recommendations:', e)

