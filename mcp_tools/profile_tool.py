class ProfileTool:
    def __init__(self):
        self.profiles = {}

    def save(self, style, profile):
        self.profiles[style] = profile
        return {"status": "saved", "style": style}

    def load(self, style):
        return self.profiles.get(style, {})
