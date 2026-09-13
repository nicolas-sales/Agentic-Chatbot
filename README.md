# Agentic AI Chatbot with LangGraph

## Description

Ce projet est une application d'IA agentique construite avec **LangGraph**, **LangChain**, **Groq**, **Tavily** et **Streamlit**.

L'objectif est d'apprendre progressivement à construire une application basée sur des LLM capable :

* de gérer un état avec LangGraph ;
* d'utiliser différents modèles LLM via Groq ;
* de construire des workflows sous forme de graphes ;
* d'utiliser des outils externes ;
* d'effectuer des recherches sur le Web avec Tavily ;
* de laisser le LLM décider quand utiliser un outil ;
* de récupérer et résumer des actualités sur l'intelligence artificielle ;
* d'afficher les résultats dans une interface Streamlit.

Le projet contient actuellement trois principaux use cases :

1. **Basic Chatbot**
2. **Chatbot with Web**
3. **AI News Explorer**

---

## Technologies utilisées

* Python
* LangGraph
* LangChain
* Groq
* Streamlit
* Tavily
* LangSmith
* FAISS
* python-dotenv

---

# Architecture générale

L'application suit globalement l'architecture suivante :

```text
Utilisateur
    ↓
Streamlit
    ↓
Configuration du use case
    ↓
GroqLLM
    ↓
GraphBuilder
    ↓
LangGraph
    ↓
Nodes / Tools
    ↓
Groq + Tavily
    ↓
Résultat
    ↓
Streamlit
```

`GraphBuilder` construit un graphe différent en fonction du use case sélectionné dans l'interface.

---

# Structure du projet

La structure évolue au fur et à mesure de l'ajout des fonctionnalités.

```text
AgenticChatbot/
│
├── app.py
├── requirements.txt
│
├── AINews/
│   ├── daily_summary.md
│   ├── weekly_summary.md
│   └── monthly_summary.md
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
│       │   ├── basic_chatbot_node.py
│       │   ├── chatbot_with_tool_node.py
│       │   └── ai_news_node.py
│       │
│       ├── tools/
│       │   └── search_tool.py
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

> La structure peut légèrement évoluer au cours du développement du projet.

---

# Installation

## 1. Créer un environnement virtuel

```bash
python -m venv venvac
```

## 2. Activer l'environnement virtuel

Sous Windows PowerShell :

```powershell
.\venvac\Scripts\Activate.ps1
```

## 3. Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

---

# Dépendances principales

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

Le projet utilise également le client Python Tavily pour certaines fonctionnalités de recherche.

---

# Configuration

## Groq

L'application utilise **Groq** pour exécuter les modèles LLM.

Une clé API Groq est nécessaire.

Elle peut être saisie directement dans l'interface Streamlit.

La clé est ensuite accessible à l'application afin d'initialiser le modèle sélectionné.

---

## Tavily

Le use case **Chatbot with Web** et le système **AI News Explorer** utilisent Tavily pour effectuer des recherches sur Internet.

Une clé API Tavily est donc nécessaire pour ces fonctionnalités.

Elle peut être saisie dans la sidebar Streamlit lorsque le use case concerné est sélectionné.

La clé est ensuite ajoutée aux variables d'environnement :

```python
os.environ["TAVILY_API_KEY"] = tavily_api_key
```

---

# Configuration des use cases

Les différentes options de l'application sont configurées dans :

```text
src/langgraphagenticai/ui/uiconfigfile.ini
```

Par exemple :

```ini
[DEFAULT]

PAGE_TITLE = LangGraph: Build stateful Agentic AI LangGraph

LLM_OPTIONS = Groq

USECASE_OPTIONS = Basic Chatbot, Chatbot with Web, AI News

GROQ_MODEL_OPTIONS = openai/gpt-oss-20b, openai/gpt-oss-120b
```

Il est important que les noms des use cases soient exactement identiques dans le fichier `.ini` et dans le code Python.

Par exemple :

```text
Chatbot with Web
```

doit conserver exactement la même casse partout.

---

# Lancer l'application

Depuis la racine du projet :

```bash
python -m streamlit run app.py
```

L'application Streamlit est ensuite disponible localement, généralement sur :

```text
http://localhost:8501
```

---

# 1. Basic Chatbot

Le premier use case est un chatbot simple utilisant Groq et LangGraph.

Son graphe est :

```text
START
  ↓
chatbot
  ↓
END
```

Le message de l'utilisateur est envoyé au graphe.

Le node `chatbot` appelle le LLM Groq puis retourne la réponse.

Exemple :

```text
Utilisateur
    ↓
"Salut"
    ↓
START
    ↓
chatbot
    ↓
Groq LLM
    ↓
AIMessage
    ↓
END
    ↓
Streamlit
```

Exemple de conversation :

```text
Utilisateur : Salut

Assistant : Bonjour ! Comment puis-je vous aider aujourd'hui ?
```

---

# 2. Chatbot with Web

Le deuxième use case ajoute la possibilité d'utiliser une recherche Web avec **Tavily**.

Le LLM ne se contente donc plus de répondre directement : il peut décider qu'il a besoin d'informations provenant d'Internet.

Le graphe devient :

```text
                    ┌─────────────┐
START ─────────────→│   chatbot   │
                    └──────┬──────┘
                           │
                    tools_condition
                           │
                    ┌──────┴───────┐
                    │              │
              pas de tool       tool call
                    │              │
                    ↓              ↓
                   END          tools
                                   │
                                   ↓
                                chatbot
```

---

# Fonctionnement du Chatbot with Web

Lorsqu'un utilisateur pose une question :

```text
Quelle est la météo aujourd'hui à Paris ?
```

le message est envoyé au graphe :

```python
initial_state = {
    "messages": [user_message]
}

res = graph.invoke(initial_state)
```

Le premier node exécuté est :

```text
chatbot
```

Le LLM analyse la question.

Il peut alors :

```text
                chatbot
                   │
         ┌─────────┴─────────┐
         │                   │
Réponse directe       Besoin du Web
         │                   │
         ↓                   ↓
        END              Tool Call
                             │
                             ↓
                           Tavily
```

Si une recherche Web est nécessaire, le LLM génère un appel d'outil.

---

# Tools et ToolNode

Les outils disponibles sont récupérés avec :

```python
tools = get_tools()
```

Par exemple, Tavily peut faire partie de cette liste.

Le `ToolNode` est ensuite créé :

```python
tool_node = create_tool_node(tools)
```

Il faut distinguer les deux concepts.

## Tool

Un **Tool** représente une capacité externe.

Par exemple :

```text
Tavily
    ↓
effectuer une recherche Web
```

## ToolNode

Le **ToolNode** est un node LangGraph capable d'exécuter les tools demandés par le LLM.

```text
LLM
 ↓
demande d'utiliser Tavily
 ↓
ToolNode
 ↓
Tavily
 ↓
résultat
```

---

# tools_condition

LangGraph utilise :

```python
self.graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)
```

`tools_condition` analyse la réponse du LLM.

Il vérifie essentiellement :

```text
Le dernier AIMessage contient-il un tool call ?
```

Si non :

```text
chatbot
   ↓
END
```

Si oui :

```text
chatbot
   ↓
tools
```

Après l'exécution de l'outil :

```python
self.graph_builder.add_edge(
    "tools",
    "chatbot"
)
```

le résultat retourne vers le LLM.

Le LLM peut alors analyser les informations récupérées et générer une réponse naturelle pour l'utilisateur.

---

# Messages LangChain

Le workflow utilise plusieurs types de messages.

## HumanMessage

Correspond au message envoyé par l'utilisateur.

```text
HumanMessage
"Quelle est la météo à Paris ?"
```

## AIMessage

Correspond à un message produit par le LLM.

Il peut s'agir :

* d'une réponse finale ;
* d'une demande d'utilisation d'un tool.

Un `AIMessage` contenant un tool call peut avoir un `content` vide.

## ToolMessage

Contient le résultat retourné par un outil.

Par exemple :

```text
ToolMessage
    ↓
Résultats Tavily
```

Après ce `ToolMessage`, le LLM est de nouveau appelé afin de produire la
