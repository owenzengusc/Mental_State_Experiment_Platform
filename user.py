class Participant:
    def __init__(self, name="New_User", age=20, answers=[]):
        self.name = name
        self.age = age
        self.answers = answers
        
    def add_answer(self, answer):
        self.answers.append(answer)
        
    def print_answers(self):
        print(self.answers)
    
    
        
    