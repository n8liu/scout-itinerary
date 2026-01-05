"""Vector memory tools for storing and recalling user preferences."""
from langchain_core.tools import tool
import os


@tool
def store_preference(user_id: str, preference_type: str, value: str) -> dict:
    """Store user travel preference in vector memory.

    Args:
        user_id: Unique user identifier
        preference_type: Category (e.g., "airline", "hotel_chain", "seat_class")
        value: Preference value

    Returns:
        Confirmation of stored preference
    """
    try:
        from langchain_pinecone import PineconeVectorStore
        from langchain_openai import OpenAIEmbeddings
        from pinecone import Pinecone

        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            return {"error": "PINECONE_API_KEY not configured"}

        pc = Pinecone(api_key=api_key)
        index_name = "scout-preferences"

        # Check if index exists, if not provide instructions
        if index_name not in pc.list_indexes().names():
            return {
                "error": f"Pinecone index '{index_name}' not found",
                "instructions": "Create index with: pc.create_index(name='scout-preferences', dimension=1536, metric='cosine')",
            }

        vectorstore = PineconeVectorStore(
            index_name=index_name, embedding=OpenAIEmbeddings()
        )

        vectorstore.add_texts(
            texts=[f"{preference_type}: {value}"],
            metadatas=[{"user_id": user_id, "type": preference_type}],
        )

        return {"stored": True, "preference": f"{preference_type}={value}"}

    except ImportError:
        return {
            "error": "Pinecone libraries not installed",
            "instructions": "Install with: pip install langchain-pinecone pinecone-client",
        }
    except Exception as e:
        return {"error": f"Failed to store preference: {str(e)}"}


@tool
def recall_preferences(user_id: str, query: str) -> dict:
    """Retrieve relevant user preferences.

    Args:
        user_id: Unique user identifier
        query: Context for preference lookup (e.g., "booking flights to Japan")

    Returns:
        List of relevant stored preferences
    """
    try:
        from langchain_pinecone import PineconeVectorStore
        from langchain_openai import OpenAIEmbeddings

        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            return {"preferences": [], "note": "PINECONE_API_KEY not configured"}

        vectorstore = PineconeVectorStore(
            index_name="scout-preferences", embedding=OpenAIEmbeddings()
        )

        results = vectorstore.similarity_search(query, k=5, filter={"user_id": user_id})

        return {"preferences": [doc.page_content for doc in results]}

    except ImportError:
        return {
            "error": "Pinecone libraries not installed",
            "preferences": [],
        }
    except Exception as e:
        return {"error": f"Failed to recall preferences: {str(e)}", "preferences": []}
