import db
import bcrypt

class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

    @classmethod
    def from_dict(cls, user_dict):
        return cls(user_dict['user_id'], user_dict['user_name'], user_dict['user_password'])
    
    @classmethod
    def getUserById(cls, user_id):
        user = db.getUserFromDbById(user_id)
        if user == None:
            return None
        return cls(user[0], user[1], user[2])

    @classmethod
    def getUserByName(cls, username):
        user = db.getUserFromDbByName(username)
        if user == None:
            return None
        return cls(user[0], user[1], user[2])

    @classmethod
    def userExists(cls, username):
        user = db.getUserFromDbByName(username)
        return cls(user[0], user[1], user[2])
    
    def validate(self, username, password):
        if self.name == username and bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')):
            return True
        return False

    def addTask(self, task):
        if task != "":
            return db.addTaskDb(self.id, task)

    def getTasks(self):
        return db.getTasksDb(self.id)

    def getTask(self, user_task_id):
        return db.getTaskDb(user_task_id)

    def updateTask(self, id, updated_task):
        db.updateTaskDb(id, updated_task)
    
    def deleteTask(self, user_task_id):
        db.deleteTaskDb(user_task_id)
