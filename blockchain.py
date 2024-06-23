class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_votes = []

    def add_vote(self, vote):
        self.pending_votes.append(vote)

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'votes': self.pending_votes,
            'previous_hash': previous_hash,
        }
        self.pending_votes = []
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1] if self.chain else None
