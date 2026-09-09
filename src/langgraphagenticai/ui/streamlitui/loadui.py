import streamlit as st
import os

from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        # Titre onglet navigateur
        st.set_page_config(page_title = self.config.get_page_title(), layout="wide") # wide : pour que le titre occuope quasiement toute la lageur de l'écran

        # Titre haut de page
        st.header(self.config.get_page_title())

        with st.sidebar:
            # Options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == "Groq":
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("API key",type="password")

                # Validate API key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your Groq API Key to proceed")

            # Usecase selection
            self.user_controls["selected_usecase"] = st.selectbox("Select usecase",usecase_options)

            if self.user_controls["selected_usecase"] == "Chatbot with Web":

                tavily_api_key = st.text_input("Tavily API key", type="password")

                self.user_controls["TAVILY_API_KEY"] = tavily_api_key
                st.session_state["TAVILY_API_KEY"] = tavily_api_key

                if tavily_api_key:
                    os.environ["TAVILY_API_KEY"] = tavily_api_key
                else:
                    st.warning(
                        "Please enter your TAVILY API Key to proceed. "
                        "Don't have one? Refer: https://app.tavily.com"
                    )


                #os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"]=st.text_input("Tavily API key",type="password")

            # Validate API key
            #if not self.user_controls["TAVILY_API_KEY"]:
                #st.warning("Please enter your TAVILY API Key to proceed. Don't have? Refer : https://app.tavily.com")

        return self.user_controls