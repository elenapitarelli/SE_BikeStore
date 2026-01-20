from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self._id_map = {}
        self.G = nx.DiGraph()

        self._lista_products = []
        self._lista_categories = []
        self.lista_connessioni = []


    def get_products(self):
        return DAO.get_all_products_by_category()

    def get_categories(self, year):
        return DAO.get_all_categories()

    def load_products(self, year):
        self._lista_products = DAO.get_all_products_by_category()
        return self._lista_products

    def load_categories(self):
        self._lista_categories = DAO.get_all_categories()
        return self._lista_categories
    def load_connessioni(self):
        self._lista_connessioni = DAO.get_all_connessioni()
        return self._lista_connessioni

    def costrusci_grafo(self):
        self._nodes = None
        self._edges = None
        self._id_map = {}
        self.load_products()
        self.load_categories()
        self.load_connessioni()
        self.G.clear()


        self._nodes = DAO.get_all_products_by_category()
        self._edges = DAO.get_all_connessioni()
        self.G.clear()
        self.G.add_nodes_from(self._nodes.values())

        for a1, a2 in self._edges:
            self.G.add_edge(a1, a2)
            if prodotto1 in self._id_map and prodotto2 in self._id_map:
                t1 = self._id_map[prodotto1]
                t2 = self._id_map[prodotto2]


    def get_date_range(self):
        return DAO.get_date_range()

    def get_num_edges(self):

        num_edges = self.G.number_of_edges()
        return num_edges

    def get_num_nodes(self):

        num_nodi = self.G.number_of_nodes()
        return num_nodi
