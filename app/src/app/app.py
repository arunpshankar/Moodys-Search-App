from src.search.search import perform_search
from src.db.create import authenticate_user
from src.db.create import insert_feedback
from src.utils.db import encrypt_password
from src.db.create import username_exists
from src.db.create import insert_user
from src.config.logging import logger 
from datetime import datetime
from typing import Optional
from typing import Dict
from typing import Any
import streamlit as st
from PIL import Image


def load_css(file_path: str) -> None:
    """Load and apply CSS styles from a given file."""
    try:
        with open(file_path) as css_file:
            st.markdown(f'<style>{css_file.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        logger.exception(f"Failed to load CSS from {file_path}: {e}")


def create_account_form() -> None:
    """Displays a form to create a new user account and handles the creation logic."""
    with st.form("create_account", border=False):
        # st.write("### Create a new account")
        first_name: str = st.text_input("First Name", key="first_name_create")
        last_name: str = st.text_input("Last Name", key="last_name_create")
        username: str = st.text_input("Username", key="username_create")
        password: str = st.text_input("Password", type="password", key="password_create")
        team: str = st.text_input("Team", key="team_create")
        submit_button: bool = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit_button:
            try:
                if username_exists(username):
                    st.error("This username is already taken. Please choose a different one.")
                else:
                    user_data: Dict[str, Any] = {
                        "username": username,
                        "password_hash": encrypt_password(password),  # Hash the password
                        "first_name": first_name,
                        "last_name": last_name,
                        "team": team
                    }
                    insert_user(user_data)
                    st.success(f"Account created successfully for {username}!")
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.rerun()
            except Exception as e:
                logger.exception("Failed to create account: %s", e)
                st.error("Failed to create account.")


def login_form() -> Optional[bool]:
    """Displays a login form and handles user authentication."""
    with st.form("login", border=False):
        # st.write("### Login")
        # st.markdown("<h2 style='text-align: center'>Document Sourcing</h2>", unsafe_allow_html=True)
        st.divider()

        username: str = st.text_input("Username", key="login_username")
        password: str = st.text_input("Password", type="password", key="login_password")
        submit_button: bool = st.form_submit_button("Login", use_container_width=True)

        st.divider()
        if submit_button:
            if authenticate_user(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.success(f"Welcome back, {username}!")
                return True
            else:
                st.error("Invalid username or password.")
                return False
    return None


def logout_button() -> None:
    """Displays a logout button and handles the logout process."""
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state.pop('username', None)
        st.rerun()


def display_banner(banner_path: str) -> None:
    """Displays a banner image from the specified path."""
    try:
        from PIL import Image
        banner_image = Image.open(banner_path)
        st.image(banner_image, width=700)  # Adjust the width as needed
    except FileNotFoundError:
        logger.error("Banner image not found at %s", banner_path)
        st.error(f"Banner image not found at {banner_path}")


def display_search_results(query, search_results, tab_name, entity_details):
    if search_results:
        rank = 1
        for result in search_results[tab_name.lower()]:
            with st.container():
                st.markdown(f"### {rank}.) {result['title']} </br>",unsafe_allow_html=True)
                st.markdown(f"{result['snippet']}")
                st.markdown(f"{result['link']}", unsafe_allow_html=True)

                feedback_form_id = f"{tab_name.lower()}_{rank}"
                with st.form(key=f"feedback_{feedback_form_id}",  border=False):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        feedback_type: str = st.radio("Relevant?", ["Yes", "No"], key=f'feedback_type_{feedback_form_id}', horizontal=True)
                    with col2:
                        feedback_text: str = st.text_input("Comments [Optional]", key=f'feedback_text_{feedback_form_id}', help="Please provide your comments here.")
                        submitted: bool = st.form_submit_button("Submit", use_container_width=True)
                    
                    if submitted:
                        logger.info("Feedback submitted for: %s - %s", feedback_type, feedback_text)
                        st.success("Feedback received. Thank you!")
                        feedback_data = {
                            'timestamp': datetime.now(),
                            'username': st.session_state['username'],
                            'query': query,
                            'title': result['title'],
                            'snippet': result['snippet'],
                            'url': result['link'],
                            'feedback': feedback_text,
                            'is_relevant': feedback_type,
                            'feedback_given_timestamp': datetime.now(),
                            'match_rank': rank,
                            **entity_details  # Unpack entity details into the feedback data
                        }
                        # Replace with your actual function to handle feedback data
                        insert_feedback(feedback_data)

                st.divider()     

                rank += 1


def search_and_feedback_ui():

    if 'search_results' not in st.session_state:
        st.session_state['search_results'] = None
    if 'entities' not in st.session_state:
        st.session_state['entities'] = None


    with st.form(key='search_form', border=False):
        
        st.markdown("<h2 style='text-align: center'>Document Sourcing</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center'>Type your query below: </p>", unsafe_allow_html=True)
        query = st.text_input("", "")
        query_mode = st.radio("Query type: ", ['Raw', 'Targeted'], index=0, horizontal=True)
        submit_button = st.form_submit_button(label='Search', use_container_width=True)
        
    # Simulate search results for the purpose of this example
    if submit_button:
        with st.spinner('Searching...'):
            search_results, entities = perform_search(query_mode, query)  # Replace with your actual function
            st.session_state.search_results = search_results
            st.session_state.entities = entities

    entity_details = st.session_state.entities if st.session_state['entities'] else {}

    tab1, tab2 = st.tabs(["Company Websites", "CDNs"])

    with tab1:
        display_search_results(query, st.session_state.search_results, "Site", entity_details)

    with tab2:
        display_search_results(query, st.session_state.search_results, "CDN", entity_details)


def display_logo(image_path: str) -> None:
    try:
        image: Image.Image = Image.open(image_path)
        st.sidebar.image(image)
    except FileNotFoundError:
        logger.error("Image not found at %s", image_path)
        st.sidebar.error(f"Image not found at {image_path}")


def app() -> None:
    """Main application function to initialize and manage the search and feedback system."""
    # st.subheader(':blue[Document Sourcing - Search and Feedback System]', divider='rainbow')
    load_css("./src/app/style.css")

    # Display logo in the sidebar
    # display_logo('./img/moodys.png')
    display_banner('./img/moodys-banner.png')
    
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if st.session_state['authenticated']:
        search_and_feedback_ui()
    else:
        # login_expander = st.expander("Login")
        # with login_expander:
        if login_form() is True:
            st.rerun()
                
        create_acc_expander = st.expander("Create Account")
        with create_acc_expander:
            create_account_form()


if __name__ == '__main__':
    app()