from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self,llm):
        """
        Initialize the AINewsNode with API keys for Tavily and Groq.
        """
        self.tavily = TavilyClient()
        self.llm = llm
        # This is used to capture various steps in this file so thaht later can be use for steps shown
        self.state = {}

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch AI news based on the specified frequency.

        Args:
            state (dict): The state dictionary containing 'frequency'.

        Returns:
            dict: Updated state with 'news_data' key containing fetched news.
        """

        frequency = state["messages"][0].content.lower()
        self.state["frequency"] = frequency # sauvegardes cette fréquence dans la mémoire interne de l'objet
        time_range_amp = {"daily": "d", "weekly": "w", "monthly": "m", "year": "y"} # dictionnaire de correspondance pour que les valeurs soient utilisées par Tavily
        days_map = {"daily": 1, "weekly": 7, "monthly": 30, "year": 365} # dictionnaire de correspondance pour que les valeurs soient utilisées par Tavily

        response = self.tavily.search(
            query="Top Artificial Intelligence (AI) technology news France and globally",
            topic="news",
            time_range=time_range_amp[frequency], # avec conversion
            include_answer="advanced",
            max_result=20,
            days=days_map[frequency] # avec conversion
        )

        state["news_data"] = response.get("results", []) # récupère la clé "results". Si "results" n'existe pas, retourne []
        self.state["news_data"] = state["news_data"] # copies aussi les articles dans self.state
        return state

    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news using an LLM.

        Args:
            state (dict): The state dictionary containing 'news_data'.

        Returns:
        dict: Updated state with 'summary' key containing the summarized news.
        """

        news_items = self.state["news_data"]

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            -Sort news by date wise (latest first)
            - Source URL as link
            Use formats:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        # transformation de la liste d'articles en une grande chaîne de texte
        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state["summary"] = response.content
        self.state["summary"] = state["summary"] # sauvegarde également ce résumé dans l'état interne
        return self.state

    def save_result(self,state):
        frequency = self.state["frequency"]
        summary = self.state["summary"]
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w', encoding="utf-8") as f: # w : écriture, utf-8 permet d'écrire accents, symboles,tirets, caractères articles web, caractère générés par LLM
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n") # Titre du fichier markdown
            f.write(summary)
        self.state["filename"] = filename
        return self.state