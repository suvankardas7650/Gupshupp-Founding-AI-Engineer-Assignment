class MemoryTool:
    def __init__(self):
        self.storage = []

    def save(self, item):
        self.storage.append(item)
        return {"status": "saved", "item": item}

    def query(self):
        return self.storage
