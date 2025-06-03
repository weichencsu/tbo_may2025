import streamlit as st

class MultiPage:
    """Framework for combining multiple streamlit applications
    """
    def __init__(self) -> None:
        self.pages = []
    
    def add_page(self, title, func):
        self.pages.append(
            {
            'title': title,
            'function': func
            }
        )
    
    def run(self):
        #st.sidebar.title("Grind Master")
        page = st.logo("bisalloy.png")
        page = st.sidebar.image("amman.png", width=120)
        page = st.sidebar.header("Northern Star Thunderbox Mine")
        page = st.sidebar.header(":rainbow[Bisalloy Digital Wear Fusion App]")
        page = st.sidebar.image("mill.png", width=240)
        page = st.sidebar.header("***Next Gen Wear Intelligence***", divider='gray')
        page = st.sidebar.markdown("###")
        page = st.sidebar.radio(
            'Asset Navigation', 
            self.pages,
            format_func=lambda page: page['title']  # Function to modify the display of the labels.

        )
        
        page['function']()
        page = st.sidebar.markdown("###")
        page = st.sidebar.markdown("###")
        page = st.sidebar.markdown("###")
        page = st.sidebar.markdown("###")
        page = st.sidebar.markdown("###")
        page = st.sidebar.caption("Developed by Bisalloy Digital Solutions 2025 | Contact us@ www.bisalloydigital.com.au")
        #page = st.sidebar.markdown("Email us@ charles.curry@bisalloy.com.au")