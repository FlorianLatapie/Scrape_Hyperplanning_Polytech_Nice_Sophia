class Discipline:
    def __init__(self, name, average):
        self.name = name
        self.average = average


    def __eq__(self, obj):
        return isinstance(obj, Discipline) and obj.name == self.name and obj.average == self.average

    def __repr__(self):
        return self.name + ": " + str(self.average)

    def __str__(self):
        return self.name + ": " + self.average

    def __serialize__(self):
        return {
            'name': self.name,
            'average': self.average
        }