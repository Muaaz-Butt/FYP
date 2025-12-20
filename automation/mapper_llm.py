import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

def map_fields_llm(fields):
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-computer-use-preview-10-2025",
        google_api_key="AIzaSyAgopFWn8NEe7XjNRl-eZvEB7feIJxRGBg",  # consider using environment variable for safety
        temperature=0
    )

    # System message
    system_msg = SystemMessage(content="""
You are an AI that maps university HTML form field names to student profile fields.
Return STRICT JSON only in this exact format:

[
  { "html_field": "<field name>", "mapped_to": "<student field name or null>" }
]

If unsure, use: "mapped_to": null.
""")

    # User message
    user_msg = HumanMessage(content=f"Extracted fields: {json.dumps(fields)}")

    # Corrected: pass a list of conversations (each conversation is a list of messages)
    response = llm.generate([[system_msg, user_msg]])

    try:
        # Extract the generated text and parse JSON
        return json.loads(response.generations[0][0].text)
    except Exception as e:
        print("Error parsing LLM response:", e)
        return []
