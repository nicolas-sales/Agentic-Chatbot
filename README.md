# Agentic AI Chatbot with LangGraph

## Description

Ce projet est un chatbot d'IA construit avec **LangGraph**, **LangChain**, **Groq** et **Streamlit**.

L'objectif du projet est d'apprendre à construire progressivement une application d'IA agentique capable de gérer un état, d'utiliser différents modèles LLM et, à terme, d'intégrer des outils externes et de la mémoire.

## Technologies utilisées

* Python
* LangGraph
* LangChain
* Groq
* Streamlit
* LangSmith
* FAISS
* Tavily

## Structure du projet

```text
AgenticChatbot/
│
├── app.py
├── requirements.txt
│
├── src/
│   └── langgraphagenticai/
│       │
│       ├── main.py
│       │
│       ├── LLMS/
│       │   └── groqllm.py
│       │
│       ├── graph/
│       │   └── graph_builder.py
│       │
│       ├── nodes/
│       │   └── basic_chatbot_node.py
│       │
│       ├── state/
│       │   └── state.py
│       │
│       └── ui/
│           ├── uiconfigfile.py
│           ├── uiconfigfile.ini
│           │
│           └── streamlitui/
│               ├── loadui.py
│               └── display_result.py
│
└── venvac/
```

## Fonctionnement général

Le projet suit actuellement ce flux :

```text
Utilisateur
    ↓
Streamlit
    ↓
GroqLLM
    ↓
GraphBuilder
    ↓
LangGraph
    ↓
START → chatbot → END
    ↓
Groq API
    ↓
Réponse du LLM
    ↓
Streamlit
```

## Installation

### 1. Créer un environnement virtuel

```bash
python -m venv venvac
```

### 2. Activer l'environnement virtuel

Sous Windows PowerShell :

```powershell
.\venvac\Scripts\Activate.ps1
```

### 3. Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

## Dépendances principales

Le fichier `requirements.txt` contient notamment :

```text
langchain
langgraph
langchain-core
langchain-community
langchain-openai
langchain-groq

ipykernel
python-dotenv

arxiv
wikipedia
feedparser

langgraph-cli==0.4.28
langgraph-api==0.10.0
langgraph-runtime-inmem==0.30.0

faiss-cpu

langchain-tavily

streamlit
```

## Configuration de Groq

L'application utilise Groq pour exécuter les modèles LLM.

Une clé API Groq est nécessaire.

La clé peut être saisie directement dans l'interface Streamlit.

## Modèles Groq

Les modèles actuellement utilisés dans le projet peuvent être configurés dans :

```text
src/langgraphagenticai/ui/uiconfigfile.ini
```

Exemple :

```ini
[DEFAULT]

PAGE_TITLE = LangGraph: Build stateful Agentic AI LangGraph

LLM_OPTIONS = Groq

USECASE_OPTIONS = Basic Chatbot

GROQ_MODEL_OPTIONS = openai/gpt-oss-20b, openai/gpt-oss-120b
```

Pour le développement et les tests, `openai/gpt-oss-20b` est un bon choix afin de conserver un coût faible.

## Lancer l'application

Depuis la racine du projet :

```bash
python -m streamlit run app.py
```

L'application Streamlit est ensuite accessible localement dans le navigateur.

Par défaut :

```text
http://localhost:8501
```

## Graph LangGraph actuel

Le chatbot utilise actuellement un graphe très simple :

```text
START
  ↓
chatbot
  ↓
END
```

Le nœud `chatbot` reçoit le message utilisateur et appelle le modèle Groq.

## GraphBuilder

La classe `GraphBuilder` est responsable de la construction du graphe LangGraph.

Elle utilise :

```python
StateGraph(State)
```

puis ajoute le nœud :

```python
self.graph_builder.add_node(
    "chatbot",
    self.basic_chatbot_node.process
)
```

et les connexions :

```python
self.graph_builder.add_edge(START, "chatbot")
self.graph_builder.add_edge("chatbot", END)
```

Le graphe est ensuite compilé avec :

```python
self.graph_builder.compile()
```

## Interface Streamlit

Streamlit permet :

* de sélectionner le fournisseur LLM ;
* de sélectionner le modèle Groq ;
* de saisir la clé API Groq ;
* de sélectionner le use case ;
* d'envoyer un message ;
* d'afficher la réponse du chatbot.

## État actuel du projet

Le **Basic Chatbot** est fonctionnel.

Exemple :

```text
Utilisateur : Salut

Assistant : Bonjour ! Comment puis-je vous aider aujourd'hui ?
```

Le flux complet entre Streamlit, LangGraph et Groq fonctionne.

## Prochaines étapes

Les prochaines améliorations prévues peuvent inclure :

* ajout de la mémoire conversationnelle ;
* conservation de l'historique des messages ;
* utilisation du state LangGraph ;
* ajout de plusieurs nodes ;
* ajout de tools ;
* recherche web avec Tavily ;
* recherche Wikipedia ;
* recherche Arxiv ;
* intégration d'une base vectorielle FAISS ;
* création d'agents ;
* ajout du routing entre différents nodes ;
* observabilité et debugging avec LangSmith.

## Objectif pédagogique

Ce projet sert principalement à comprendre progressivement :

* comment fonctionne un LLM ;
* comment intégrer Groq avec LangChain ;
* comment construire un graphe avec LangGraph ;
* comment gérer le state ;
* comment créer des nodes ;
* comment connecter des tools ;
* comment construire un agent ;
* comment créer une interface utilisateur avec Streamlit.

## Auteur

Projet personnel d'apprentissage autour de **LangGraph et des systèmes Agentic AI**.
