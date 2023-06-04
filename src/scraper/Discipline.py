class Discipline:
    """
    Represents a discipline.
    """
    def __init__(self, name: str, average: float):
        """
        Initializes a new instance of the Discipline class.

        Parameters:
        - name (str): The name of the discipline.
        - average (float): The average of the discipline.
        """
        self.name = name
        self.average = average

    def __eq__(self, obj):
        """
        Checks if this Discipline object is equal to another object.

        Parameters:
        - obj: The object to compare with.

        Returns:
        - bool: True if the objects are equal, False otherwise.
        """
        return isinstance(obj, Discipline) and obj.name == self.name and obj.average == self.average

    def __repr__(self):
        """
        Returns a string representation of the Discipline object.

        Returns:
        - str: The string representation of the object.
        """
        return self.name + ": " + str(self.average)

    def __str__(self):
        """
        Returns a string representation of the Discipline object.

        Returns:
        - str: The string representation of the object.
        """
        return self.name + ": " + str(self.average)

    def __serialize__(self):
        """
        Serializes the Discipline object into a dictionary.

        Returns:
        - dict: The serialized representation of the object.
        """
        return {
            'name': self.name,
            'average': self.average
        }
