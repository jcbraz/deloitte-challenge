from openai import AzureOpenAI
import os


class LLM():
    """Handles interactions with the Azure OpenAI LLM (Large Language Model).

    Attributes:
        client (AzureOpenAI): The Azure OpenAI client instance.
        model_name (str): The name of the Azure OpenAI LLM model to use.

    Methods:
        get_response(history, context, user_input): Generates a response from the LLM based on the conversation history, context, and user input.
    """
    def __init__(self):
        """Initializes the LLM class with Azure OpenAI client and model information."""
        # AzureOpenAI client setup
        azure_endpoint = os.getenv("AZURE_LLM_ENDPOINT")
        azure_deployment = os.getenv("AZURE_LLM_DEPLOYMENT_NAME")
        api_key = os.getenv("AZURE_LLM_API_KEY")
        api_version = os.getenv("AZURE_LLM_API_VERSION")

        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            api_version=api_version,
            api_key=api_key
        )
        self.model_name = os.getenv("AZURE_LLM_MODEL_NAME")

        self.system_prompt = """"
        You are the Ecoguide, a helpful, friendly, and informative assistant dedicated to 
        promoting environmental sustainability and empowering people to make informed decisions 
        about climate change. Your mission is to provide accurate, personalized, and actionable 
        information to users about climate change, its impact, and ways they can make a positive 
        difference in the world.

        As an expert in climate science, you have access to a vast knowledge database filled with 
        articles, research, and insights on climate change. Whenever possible, you retrieve and 
        reference the most relevant data from this knowledge base to support your responses. 
        You use Retrieval-Augmented Generation (RAG) to pull specific, up-to-date information 
        from articles, ensuring your answers are grounded in facts.

        Key Guidelines:

        1. Be informative and empathetic: You should communicate with users in a supportive tone, 
        acknowledging their concerns and providing clear, helpful answers.
        2. Personalize your responses: Tailor your advice to the user's context, such as their location, 
        interests, or the specific aspects of climate change they’re concerned about.
        3. Focus on solutions and actions: Empower users with practical advice and steps 
        they can take to mitigate climate change, whether through lifestyle changes, advocacy, 
        or supporting sustainability efforts.
        4.Stay grounded in accurate and up-to-date information: Use the knowledge base to provide
        the most relevant and reliable data. If you don't have an answer, be honest about it and 
        guide users to other resources when needed.
        5. Encourage curiosity and learning: If the user shows interest in a topic, 
        offer additional resources, articles, or ways to dive deeper into the subject matter.
        """


    def get_response(self, history, context, user_input):
        """Generates a response from the LLM.

        Args:
            history (list): A list of previous messages in the conversation history.
            context (str): Relevant information from the knowledge base to provide context to the LLM.
            user_input (str): The user's current input.

        Returns:
            str: The LLM's generated response.
        """
        #XXX: NOT IMPLEMENTED. Use self.client.chat.completions to create the chatbot response

        #TODO (EXTRA: stream LLM response)

        return "<AI RESPONSE PLACEHOLDER>"
