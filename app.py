import json
from mcp_tools.memory_tool import MemoryTool
from mcp_tools.profile_tool import ProfileTool

memory = MemoryTool()
profiles = ProfileTool()

templates = json.load(open("personality/templates.json"))

def llm(prompt):
    return "LLM OUTPUT: " + prompt[:100]

def extract_memory(message):
    items = []
    if "like" in message or "love" in message:
        items.append({"type": "preference","value": message,"confidence": 0.9})
    if "sad" in message or "angry" in message:
        items.append({"type": "emotion","value": message,"confidence": 0.8})
    if "I am" in message or "my name" in message:
        items.append({"type": "fact","value": message,"confidence": 0.85})
    return items

def transform(reply, style):
    template = templates[style]
    prompt = f"{template}\nOriginal: {reply}"
    return llm(prompt)

def run_pipeline():
    lines = open("data/messages.txt").read().splitlines()
    for msg in lines:
        mem_items = extract_memory(msg)
        for item in mem_items:
            memory.save(item)
    baseline = "This is the neutral reply."
    output = {}
    for style in templates.keys():
        transformed = transform(baseline, style)
        output[style] = transformed
    print("=== STORED MEMORY ===")
    print(memory.query())
    print("\n=== PERSONALITY OUTPUTS ===")
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    run_pipeline()
