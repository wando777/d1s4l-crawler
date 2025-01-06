from data.database import db

class BotState(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    state = db.Column(db.PickleType, nullable=False)

    def __init__(self, id, state):
        self.id = id
        self.state = state