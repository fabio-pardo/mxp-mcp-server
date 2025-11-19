import os
import vertexai
from vertexai import rag
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class RagClient:
    """
    A client for interacting with a Google Cloud Vertex AI RAG Corpus.
    """

    def __init__(self):
        """
        Initializes the Vertex AI RAG client. It configures the connection
        using environment variables.
        """
        self.project_id = os.getenv("VERTEX_PROJECT_ID")
        self.rag_corpus_name = os.getenv("VERTEX_RAG_CORPUS_NAME")

        if not self.project_id or not self.rag_corpus_name:
            raise ValueError(
                "VERTEX_PROJECT_ID and VERTEX_RAG_CORPUS_NAME environment variables must be set."
            )

        # Initialize Vertex AI API once per session
        try:
            print("Initializing Vertex AI...")
            vertexai.init(project=self.project_id, location="us-east1")
            print("Vertex AI initialized successfully.")
        except Exception as e:
            print(f"Error initializing Vertex AI: {e}")
            raise

    def query(
        self,
        query_text: str,
        top_k: int = 5,
        vector_distance_threshold: float = 0.5,
    ) -> dict:
        """
        Performs a retrieval query against the configured RAG corpus.

        Args:
            query_text: The text to search for.
            top_k: The number of top results to return.
            vector_distance_threshold: The similarity threshold for results (0-1).
                                       Lower is more similar.

        Returns:
            A dictionary containing the retrieved contexts.
        """
        if not self.rag_corpus_name:
            raise ValueError("RAG corpus name is not configured.")

        print(f"Performing retrieval query for: '{query_text}'")
        response = rag.retrieval_query(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=self.rag_corpus_name,
                )
            ],
            text=query_text,
            rag_retrieval_config=rag.RagRetrievalConfig(
                top_k=top_k,
                filter=rag.Filter(vector_distance_threshold=vector_distance_threshold),
            ),
        )

        # Convert the response object to a dictionary for consistency
        return {
            "contexts": [
                {"source_uri": c.source_uri, "text": c.text}
                for c in response.contexts.contexts
            ]
        }


# Example usage for direct testing of the client
if __name__ == "__main__":
    try:
        rag_client = RagClient()
        test_query = "Tell me about the Person table?"
        print(f"Querying RAG corpus with: '{test_query}'")
        response = rag_client.query(test_query)
        print("\nResponse:")
        print(response)
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An error occurred during the query: {e}")
