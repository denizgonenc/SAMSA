class Graph:
    V = []
    E = []
    G = {}

    def add_vertex(self, vertex, edges):
        """
        :param vertex: string
        :param edges: list of tuples, 1st element of tuple is string, 2nd element of tuple is float
        :return: none
        """

        self.V.append(vertex)
        self.G[vertex] = edges

        for edge in edges:
            self.E.append((vertex, edge))


    def get_depth(self):
        visited = []
        d = 0






