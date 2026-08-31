import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        print(user_message)
        if usecase =="Basic Chatbot":
                for event in graph.stream({'messages':("user",user_message)}): # .stream pour donner les résultats au fur et à mesure de l'exécution des noeuds
                    print(event.values())
                    for value in event.values():
                        print(value['messages'])
                        with st.chat_message("user"): # streamlit crée une bulle de chat pour l'utilisateur
                            st.write(user_message)
                        with st.chat_message("assistant"): # streamlit crée une bulle assistant et affiche le contenu de AIMessage
                            st.write(value["messages"].content)