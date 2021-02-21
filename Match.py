# A simple class for holding artist names and their similarity score to a search query.
class Match:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        
    def __repr__(self):
        return repr((self.name, self.score))