class Model(dict):
    """
    Represents basic information on a Graphwalker model
    """

    @property
    def name(self) -> str:
        """
        Get the name of the model.
        """
        return self["ModelName"]

    @property
    def id(self) -> str:
        """
        Get the ID of the model.
        """
        return self["ModelId"]

    @property
    def vertices(self) -> int:
        """
        Get the number of vertices.
        """
        return self["VerticesCount"]

    @property
    def edges(self) -> int:
        """
        Get the number of edges.
        """
        return self["EdgesCount"]

    @property
    def requirements(self) -> int:
        """
        Get the number of requirements.
        """
        return self["RequirementsCount"]

    @property
    def actions(self) -> int:
        """
        Get the number of actions.
        """
        return self["ActionsCount"]

    @property
    def properties(self) -> dict:
        """
        Get the properties.
        """
        return self["Properties"]

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    def __repr__(self) -> str:
        return f"Model({self.name}, {self.id})"
