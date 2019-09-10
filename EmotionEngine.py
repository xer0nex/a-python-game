


class Emotion:
    def __init__(self, name, description=''):
        self.name = name
        self.description = description
        self.links = []
        self.weights = []


class EmotiveRange:
    def __init__(self, name, positive, neutral, negative):
        self.name = name
        self.positive = positive
        self.neutral = neutral
        self.negative = negative
        self.value = 0.0


class EmotiveRelation:
    def __init__(self, name, relations=[], weights=[]):
        self.name = name
        self.relations = relations
        self.weights = weights

# class Emotive


emotions = ["admiration","adoration","aesthetic appriciation",
            "amusement","calmness","excitement","joy","romance","sexual desire",
            "awe","awkwardness","craving","surprise",
            "interest","nostalgia","relief","satisfaction","entrancement",
            "anger","anxiety","boredom","confusion","disgust","pain","fear",
            "horror","sadness"]

POSITIVE = 0
NEUTRAL = 9
NEGATIVE = 17


class MindMod:
    def __init__(self):
        pass

def main():
    m = MindMod()


if __name__ == "__main__":
    main()
