import json
import os
from openai import OpenAI
from mcp_tools.memory_tool import MemoryTool
from mcp_tools.profile_tool import ProfileTool

# -----------------------------
# Initialize tools and LLM
# -----------------------------
memory = MemoryTool()
profiles = ProfileTool()
templates = json.load(open("personality/templates.json"))

# OpenAI client (API key comes from Replit Secrets)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# LLM Function
# -----------------------------
def llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]


# -----------------------------
# Memory Extraction
# -----------------------------
def extract_memory(message):
    items = []

    if "like" in message or "love" in message:
        items.append({"type": "preference", "value": message, "confidence": 0.9})

    if "sad" in message or "tired" in message or "angry" in message:
        items.append({"type": "emotion", "value": message, "confidence": 0.8})

    if "I am" in message or "my name" in message:
        items.append({"type": "fact", "value": message, "confidence": 0.85})

    return items


# -----------------------------
# Personality Rewriting
# -----------------------------
def transform(reply, style):
    template = templates[style]
    prompt = f"{template}\n\nOriginal: {reply}\nRewrite this in the requested tone:"
    return llm(prompt)


# -----------------------------
# Main Pipeline
# -----------------------------
def run_pipeline():

    # Load sample user messages
    lines = open("data/messages.txt").read().splitlines()

    # Extract memory from messages
    for msg in lines:
        extracted = extract_memory(msg)
        for item in extracted:
            memory.save(item)

    # BEFORE RESPONSE
    baseline = "This is the neutral reply."

    print("=== BEFORE (Neutral Reply) ===")
    print(baseline)

    # AFTER — Personality Transformations
    output = {}
    for style in templates.keys():
        output[style] = transform(baseline, style)

    print("\n=== STORED MEMORY ===")
    print(memory.query())

    print("\n=== AFTER (Personality Outputs) ===")
    print(json.dumps(output, indent=2))


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    run_pipeline()

