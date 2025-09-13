from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.callbacks.manager import get_openai_callback


from app.core.config import settings
from app.db.session import db_instance


class AgentService:
    def __init__(self):
        # Initialize the database connection
        # self.db = SQLDatabase.from_uri(settings.DATABASE_URL)
        self.db = db_instance

        # Initialize the LLM
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0,
        )

        # Create the toolkit
        toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)

        # Create the agent executor
        self.agent_executor = create_sql_agent(
            llm=self.llm,
            toolkit=toolkit,
            verbose=True,
            handle_parsing_errors=True,
        )

    def process_query(self, question: str) -> str:
        """Processes a natural language query and returns the answer."""
        try:
            with get_openai_callback() as cb:
                response = self.agent_executor.invoke({"input": question})

                print("--- Token Usage ---")
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost (USD): ${cb.total_cost:.6f}")
                print("-------------------")

                return response.get(
                    "output", "Sorry, I couldn't process that question."
                )
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred while processing your request."


agent_service = AgentService()
