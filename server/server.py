from flask import Flask, jsonify, request, Response, stream_with_context
from flask_cors import CORS
import chromadb
from chromadb.utils import embedding_functions
import os
import requests
import json
import base64
from dotenv import load_dotenv
from pathlib import Path
from supabase import create_client, Client

# Load environment variables from root .env file
root_dir = Path(__file__).parent.parent
load_dotenv(dotenv_path=root_dir / ".env")

app = Flask(__name__)
CORS(app)

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
embedding = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Get or create collection
try:
    collection = chroma_client.get_collection(
        name="static_knowledge_base", embedding_function=embedding
    )
except Exception:
    collection = chroma_client.create_collection(
        name="static_knowledge_base",
        embedding_function=embedding,
        metadata={"description": "Static knowledge base for RAG"},
    )

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# Initialize Lava Payments token
def get_lava_token():
    return base64.b64encode(
        json.dumps(
            {
                "secret_key": os.getenv("LAVA_API_KEY"),
                "connection_secret": os.getenv("LAVA_SELF_CONNECTION_SECRET"),
                "product_secret": os.getenv("LAVA_SELF_PRODUCT_SECRET"),
            }
        ).encode()
    ).decode()


def split_query_into_search_terms(user_query: str):
    """
    Use LLM to split a complex user query into simpler search terms for RAG.

    Args:
        user_query: The original user question

    Returns:
        List of simplified search queries
    """
    token = get_lava_token()

    # Load query splitter prompt from file
    splitter_prompt_path = Path(__file__).parent / "query_splitter_prompt.md"
    with open(splitter_prompt_path, "r") as f:
        system_prompt = f.read()

    try:
        response = requests.post(
            "https://api.lavapayments.com/v1/forward?u=https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query},
                ],
                "temperature": 0.3,
            },
        )

        response_data = response.json()
        split_queries = (
            response_data["choices"][0]["message"]["content"].strip().split("\n")
        )
        # Clean up any empty lines
        split_queries = [q.strip() for q in split_queries if q.strip()]

        print(f"Split query into: {split_queries}")
        return split_queries

    except Exception as e:
        print(f"Error splitting query: {e}")
        # Fallback to original query if splitting fails
        return [user_query]


def get_rag_context(query: str, n_results: int = 3):
    """
    Retrieve relevant documents from the vector database.

    Args:
        query: The search query
        n_results: Number of results to return

    Returns:
        List of dictionaries containing document text, distance, and metadata
    """
    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "distances", "metadatas"],
    )

    context_items = []
    for doc, distance, metadata in zip(
        results["documents"][0], results["distances"][0], results["metadatas"][0]
    ):
        context_items.append({"text": doc, "distance": distance, "metadata": metadata})

    return context_items


def get_realtime_farm_data(crop_list=None):
    """
    Fetch real-time data from Supabase tables.

    Args:
        crop_list: Optional list of crop names to filter market data

    Returns:
        Dictionary containing weather, market, and other farm data
    """
    try:
        # Fetch weather data (most recent 7 days)
        weather_response = (
            supabase.table("weather_data")
            .select("*")
            .order("date", desc=False)
            .limit(7)
            .execute()
        )

        # Fetch market prices with optional crop filter
        market_query = supabase.table("market_prices").select("*")

        if crop_list:
            # Filter by crop names (case-insensitive)
            market_query = market_query.in_("crop_name", crop_list)

        market_response = market_query.order("date", desc=False).execute()

        return {
            "weather": weather_response.data if weather_response.data else [],
            "market": market_response.data if market_response.data else [],
        }
    except Exception as e:
        print(f"Error fetching real-time data: {e}")
        return {"weather": [], "market": []}


def format_realtime_data(realtime_data):
    """
    Format real-time data into a readable text format for the LLM.

    Args:
        realtime_data: Dictionary containing weather and market data

    Returns:
        Formatted string with real-time data
    """
    formatted_text = "=== REAL-TIME PERSONALIZED FARM DATA ===\n\n"

    # Format weather data
    if realtime_data["weather"]:
        formatted_text += "** Weather Forecast (Next 7 Days) **\n"
        for day in realtime_data["weather"]:
            formatted_text += f"Date: {day.get('date', 'N/A')}\n"
            formatted_text += f"  - Temperature: {day.get('temperature_low', 'N/A')}°F to {day.get('temperature_high', 'N/A')}°F\n"
            formatted_text += (
                f"  - Mean Temperature: {day.get('temperature_mean', 'N/A')}°F\n"
            )
            formatted_text += (
                f"  - Precipitation Chance: {day.get('precipitation_chance', 'N/A')}%\n"
            )
            formatted_text += f"  - Precipitation Amount: {day.get('precipitation_sum', 'N/A')} inches\n"
            if day.get("humidity_mean"):
                formatted_text += f"  - Humidity: {day.get('humidity_mean')}%\n"
            if day.get("wind_speed_max"):
                formatted_text += f"  - Max Wind Speed: {day.get('wind_speed_max')} mph from {day.get('wind_direction', 'N/A')}\n"
            if day.get("wind_gusts_max"):
                formatted_text += f"  - Wind Gusts: {day.get('wind_gusts_max')} mph\n"
            if day.get("evapotranspiration"):
                formatted_text += (
                    f"  - Evapotranspiration: {day.get('evapotranspiration')} inches\n"
                )
            if day.get("sunshine_duration"):
                formatted_text += (
                    f"  - Sunshine Duration: {day.get('sunshine_duration')} seconds\n"
                )
            formatted_text += "\n"
    else:
        formatted_text += "** Weather Forecast **\nNo weather data available.\n\n"

    # Format market data
    if realtime_data["market"]:
        formatted_text += "** Market Prices **\n"
        # Group by crop
        crops = {}
        for price in realtime_data["market"]:
            crop_name = price.get("crop_name", "Unknown")
            if crop_name not in crops:
                crops[crop_name] = []
            crops[crop_name].append(price)

        for crop_name, prices in crops.items():
            formatted_text += (
                f"\n{crop_name.title()} ({prices[0].get('unit', 'N/A')}):\n"
            )
            for price in prices[:10]:  # Limit to 10 most recent prices per crop
                formatted_text += (
                    f"  - {price.get('date', 'N/A')}: ${price.get('price', 'N/A')}\n"
                )
    else:
        formatted_text += "** Market Prices **\nNo market data available.\n\n"

    formatted_text += "\n=== END REAL-TIME DATA ===\n"
    return formatted_text


@app.route("/api/farm-data", methods=["GET"])
def get_farm_data():
    """
    API endpoint to fetch real-time farm data (weather and market prices).
    Accepts optional 'crops' query parameter (comma-separated list).
    """
    try:
        # Get crops parameter from query string
        crops_param = request.args.get("crops")
        crop_list = None

        if crops_param:
            # Split comma-separated crops and clean up whitespace
            crop_list = [crop.strip() for crop in crops_param.split(",")]

        # Fetch real-time data
        realtime_data = get_realtime_farm_data(crop_list)

        return jsonify(realtime_data), 200

    except Exception as e:
        print(f"Error in /api/farm-data endpoint: {e}")
        return jsonify({"error": str(e), "weather": [], "market": []}), 500


@app.route("/api/satellite-data", methods=["GET"])
def get_satellite_data():
    """
    API endpoint to fetch satellite/crop monitor data from Supabase.
    Returns the most recent satellite data entry.
    """
    try:
        # Fetch the most recent satellite data (ordered by created_at)
        satellite_response = (
            supabase.table("satellite_data_table")
            .select("*")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        # Return the first (most recent) record, or null if none exists
        satellite_data = satellite_response.data[0] if satellite_response.data else None

        return jsonify(satellite_data), 200

    except Exception as e:
        print(f"Error in /api/satellite-data endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/environmental-data", methods=["GET"])
def get_environmental_data():
    """
    API endpoint to fetch environmental/soil data from Supabase.
    Returns the environmental data for the specified farm (defaults to FARM01).
    """
    try:
        # Get farm_id parameter from query string (default to FARM01)
        farm_id = request.args.get("farm_id", "FARM01")

        # Fetch environmental data for the specified farm
        environmental_response = (
            supabase.table("environmental_data")
            .select("*")
            .eq("farm_id", farm_id)
            .limit(1)
            .execute()
        )

        # Return the first record, or null if none exists
        environmental_data = (
            environmental_response.data[0] if environmental_response.data else None
        )

        return jsonify(environmental_data), 200

    except Exception as e:
        print(f"Error in /api/environmental-data endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/rag-query", methods=["POST"])
def rag_query():
    try:
        data = request.get_json()

        if not data or "messages" not in data:
            return jsonify({"error": 'Missing "messages" in request body'}), 400

        messages = data["messages"]
        n_results = data.get("n_results", 3)

        # Get the latest user message for RAG context retrieval
        user_messages = [m for m in messages if m["role"] == "user"]
        if not user_messages:
            return jsonify({"error": "No user messages found"}), 400

        # Extract text from the latest user message (handle both string and multimodal format)
        latest_message_content = user_messages[-1]["content"]
        if isinstance(latest_message_content, str):
            latest_user_prompt = latest_message_content
        elif isinstance(latest_message_content, list):
            # Multimodal format - extract text from the array
            text_parts = [
                item.get("text", "")
                for item in latest_message_content
                if item.get("type") == "text"
            ]
            latest_user_prompt = " ".join(text_parts)
        else:
            latest_user_prompt = str(latest_message_content)

        # Get relevant context from RAG
        context_items = get_rag_context(latest_user_prompt, n_results)
        print(context_items)

        # Format context for LLM
        context_text = "\n\n".join(
            [
                f"[Source: {item['metadata']['source']}]\n{item['text']}"
                for item in context_items
            ]
        )

        # Get real-time farm data from Supabase
        realtime_data = get_realtime_farm_data()
        realtime_text = format_realtime_data(realtime_data)
        print(realtime_text)

        # Load system prompt template from file
        system_prompt_path = Path(__file__).parent / "system_prompt.md"
        with open(system_prompt_path, "r") as f:
            system_prompt_template = f.read()

        # Create system message with both RAG context and real-time data
        system_message = system_prompt_template.format(
            realtime_data=realtime_text, rag_context=context_text
        )

        # Build the messages array for the LLM with conversation history
        llm_messages = [{"role": "system", "content": system_message}]

        # Add all conversation history (excluding any existing system messages from client)
        for msg in messages:
            if msg["role"] != "system":
                llm_messages.append({"role": msg["role"], "content": msg["content"]})

        # Call OpenAI via Lava Payments
        token = get_lava_token()

        lava_response = requests.post(
            "https://api.lavapayments.com/v1/forward?u=https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={"model": "gpt-4o-mini", "messages": llm_messages},
        )

        # Check if streaming is requested
        should_stream = data.get("stream", False)

        if should_stream:
            # Return streaming response with status updates
            def generate():
                try:
                    # Send single status with context sources if available
                    if context_items:
                        sources = [
                            item["metadata"]
                            .get("source", "Unknown")
                            .replace(".txt", "")
                            for item in context_items[:2]
                        ]
                        sources_text = ", ".join(sources)
                        yield f"data: {json.dumps({'status': f'Analyzing {sources_text}...', 'stage': 'rag'})}\n\n"

                    # Now stream the actual LLM response
                    lava_response = requests.post(
                        "https://api.lavapayments.com/v1/forward?u=https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {token}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "gpt-4o-mini",
                            "messages": llm_messages,
                            "stream": True,
                        },
                        stream=True,
                    )

                    # Stream the response
                    for line in lava_response.iter_lines():
                        if line:
                            decoded_line = line.decode("utf-8")
                            # Forward the SSE data directly to client
                            if decoded_line.startswith("data: "):
                                data_content = decoded_line[
                                    6:
                                ]  # Remove 'data: ' prefix

                                # Remove ** from content if present
                                if data_content != "[DONE]":
                                    try:
                                        parsed = json.loads(data_content)
                                        if (
                                            "choices" in parsed
                                            and len(parsed["choices"]) > 0
                                        ):
                                            if (
                                                "delta" in parsed["choices"][0]
                                                and "content"
                                                in parsed["choices"][0]["delta"]
                                            ):
                                                content = parsed["choices"][0]["delta"][
                                                    "content"
                                                ]
                                                content = content.replace("**", "")
                                                parsed["choices"][0]["delta"][
                                                    "content"
                                                ] = content
                                                data_content = json.dumps(parsed)
                                    except:
                                        pass

                                yield f"data: {data_content}\n\n"

                    # Send completion marker
                    yield "data: [DONE]\n\n"

                except Exception as e:
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"

            return Response(
                stream_with_context(generate()), mimetype="text/event-stream"
            )
        else:
            # Non-streaming response (legacy)
            lava_response = requests.post(
                "https://api.lavapayments.com/v1/forward?u=https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json={"model": "gpt-4o-mini", "messages": llm_messages},
            )

        lava_data = lava_response.json()
        response_text = lava_data["choices"][0]["message"]["content"]

        # Remove markdown formatting symbols
        response_text = response_text.replace("**", "")

        return (
            jsonify(
                {
                    "response": response_text,
                    "context": context_items,
                    "model": lava_data.get("model", "gpt-4o-mini"),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8080)
