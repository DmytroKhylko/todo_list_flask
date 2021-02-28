class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
    @classmethod
    def from_dict(cls, user_dict):
        return cls(user_dict['user_id'], user_dict['user_name'], user_dict['user_password'])
    
    def validate(self, username, password):
        if self.name == username and self.password == password:
            return True
        return False