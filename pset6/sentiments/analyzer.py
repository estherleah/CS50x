import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        # add positive words
        self.positives = set()
        file = open("positive-words.txt", "r")
        for line in file:
            if not line.startswith(';'):
                self.positives.add(line.strip())
        file.close()
        # add negative words
        self.negatives = set()
        file = open("negative-words.txt", "r")
        for line in file:
            if not line.startswith(';'):
                self.negatives.add(line.strip())
        file.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        # initialize token and tokenizer
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        sum = 0
        # analyze each word
        for word in tokens:
            if word.lower() in self.positives:
                sum += 1
            elif word.lower() in self.negatives:
                sum -= 1
            else:
                sum += 0
        return sum
