class User:
    def __init__(self, _id, username, password):
        self.id = _id # id is python keyword. must add prefix '_'
        self.username = username
        self.password = password