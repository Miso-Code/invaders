class CMetadata:
    def __init__(self, metadata):
        for key, value in metadata.items():
            setattr(self, key, value)
