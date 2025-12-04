import json
from mcp_tools.memory_tool import MemoryTool
from mcp_tools.profile_tool import ProfileTool

# Initialize tools
memory = MemoryTool()
profiles = ProfileTool()

# Load templates
templates = json.load(open("personality/templates.json"))

# Fake LLM function (safe, no API required)
def llm(prompt):
    return "LLM OUTPUT: " + prompt[:100]

# Extract memory
def extract_memory(message):
    items = []

    if "like" in message or "love" in message:
        items.append({"type": "preference", "value": message, "confidence": 0.9})
    if "sad" in message or "angry" in message or "tired" in message:
        items.append({"type": "emotion", "value": message, "confidence": 0.8})
    if "I am" in message or "my name" in message:
        items.append({"type": "fact", "value": message, "confidence": 0.85})

    return items

# Personality rewrite
def transform(reply, style):
    template = templates[style]
    prompt = f"{template}\n\nOriginal: {reply}\nRewrite it:"
    return llm(prompt)

def run_pipeline():
    lines = open("data/messages.txt").read().splitlines()

    for msg in lines:
        for item in extract_memory(msg):
            memory.save(item)

    baseline = "This is the neutral reply."

    print("=== BEFORE (Neutral Reply) ===")
    print(baseline)

    output = {}
    for style in templates.keys():
        output[style] = transform(baseline, style)

    print("\n=== STORED MEMORY ===")
    print(memory.query())

    print("\n=== AFTER (Personality Outputs) ===")
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    run_pipeline()
