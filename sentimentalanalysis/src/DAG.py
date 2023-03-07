class DAG:
    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, start, end, weight=0):
        if start not in self.adj_list:
            self.add_vertex(start)
        if end not in self.adj_list:
            self.add_vertex(end)
        self.adj_list[start].append((end, weight))







