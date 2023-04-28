import csv
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

# Define la clase Pelicula
class Pelicula:
    def __init__(self, id, nombre, año, genero, director):
        self.id = id
        self.nombre = nombre
        self.año = año
        self.genero = genero
        self.director = director

def leer_peliculas():
    # Abre el archivo CSV con la codificación UTF-8
    with open('database.csv', 'r', encoding='UTF-8') as csvfile:
        # Crea un objeto reader
        reader = csv.reader(csvfile)
        # Crea un grafo vacío
        G = nx.Graph()

        # Evita leer la primera linea (cabecera con los parámetros)
        next(reader)

        # Crea un diccionario de géneros para cada película
        generos = {}
        peliculas = []
        for i, row in enumerate(reader):
            # Crea un objeto Pelicula con los datos de la fila
            pelicula = Pelicula(id=i, nombre=row[1], año=row[2], genero=row[5].split(','), director=row[9])
            peliculas.append(pelicula)
            # Agrega la película al grafo
            G.add_node(i, data=pelicula)
            # Agrega los géneros de la película al diccionario
            generos[i] = set(pelicula.genero)

        # Crea las aristas del grafo
        for i in range(len(peliculas)):
            for j in range(i+1, len(peliculas)):
                # Calcula el peso de la arista
                peso = 0
                # Aumenta el peso si las películas tienen el mismo director
                if peliculas[i].director == peliculas[j].director:
                    peso += 1
                # Aumenta el peso por cada género idéntico entre las películas
                for genero in peliculas[i].genero:
                    if genero in peliculas[j].genero:
                        peso += 1
                # Crea la arista con el peso calculado
                if peso > 0:
                    G.add_edge(i, j, weight=peso)

        return G

# Prueba 1
def dibujar_grafo(G):
    # Selecciona los primeros 10 nodos del grafo
    nodes = list(G.nodes())[:10]
    # Crea un subgrafo con los nodos seleccionados
    G_sub = G.subgraph(nodes)

    # Selecciona todas las aristas del subgrafo
    edges = G_sub.edges()

    # Verifica si la lista de aristas es vacía
    if len(edges) == 0:
        print("No hay conexiones entre los primeros 10 nodos.")
        return

    # Define los tamaños y colores de los nodos y aristas
    node_size = 500
    node_color = '#FFC300'
    edge_width = [d['weight'] for (u, v, d) in G_sub.edges(data=True)]
    edge_color = '#C4C4C4'
    edge_cmap = plt.cm.Blues

    # Ajusta la posición de los nodos
    pos = nx.kamada_kawai_layout(G_sub)

    # Dibuja la gráfica del subgrafo
    nx.draw_networkx_nodes(G_sub, pos, nodelist=nodes, node_color=node_color, node_size=node_size)
    nx.draw_networkx_edges(G_sub, pos, edgelist=edges, edge_color=edge_color, width=edge_width, edge_cmap=edge_cmap)
    nx.draw_networkx_edge_labels(G_sub, pos, font_size=10, edge_labels={(u, v): d['weight'] for u, v, d in G_sub.edges(data=True)})
    nx.draw_networkx_labels(G_sub, pos, font_size=12)

    # Agrega un título al gráfico
    plt.title("Primeras 10 películas con todas sus conexiones")

    for node in G_sub.nodes():
        pelicula = G_sub.nodes[node]['data']
        print("ID: {} - Película: {} - Año: {} - Género: {} - Director: {}".format(pelicula.id, pelicula.nombre, pelicula.año, pelicula.genero, pelicula.director))

    # Desactiva los ejes y muestra la gráfica
    plt.axis('off')
    plt.show()

# Prueba 2
def imprimir_nodos(G):
    # Selecciona los primeros 20 nodos del grafo
    nodes = list(G.nodes())[:20]
    
    # Imprime los datos de cada nodo
    for node in nodes:
        pelicula = G.nodes[node]['data']
        print("ID: {} - Película: {} - Año: {} - Género: {} - Director: {}".format(pelicula.id, pelicula.nombre, pelicula.año, pelicula.genero, pelicula.director))

    # Crea un subgrafo con los nodos seleccionados y las aristas con peso mayor a 1
    G_sub = G.subgraph(nodes)
    edges = [(u, v) for u, v, d in G_sub.edges(data=True) if d['weight'] > 1]
    
    # Verifica si la lista de aristas es vacía
    if len(edges) == 0:
        print("No hay conexiones entre los primeros 20 nodos con peso mayor a 1.")
        return

    # Define los tamaños y colores de los nodos y aristas
    node_size = 500
    node_color = '#FFC300'
    edge_width = 1
    edge_color = '#C4C4C4'
    edge_cmap = plt.cm.Blues

    # Ajusta la posición de los nodos
    pos = nx.kamada_kawai_layout(G_sub)

    # Dibuja la gráfica del subgrafo
    nx.draw_networkx_nodes(G_sub, pos, nodelist=nodes, node_color=node_color, node_size=node_size)
    nx.draw_networkx_edges(G_sub, pos, edgelist=edges, edge_color=edge_color, width=edge_width, edge_cmap=edge_cmap)
    nx.draw_networkx_edge_labels(G_sub, pos, font_size=10, edge_labels={(u, v): d['weight'] for u, v, d in G_sub.edges(data=True) if d['weight'] > 1})
    nx.draw_networkx_labels(G_sub, pos, font_size=12)

    # Agrega un título al gráfico
    plt.title("Primeras 20 películas con conexiones con peso mayor a 1")

    # Desactiva los ejes y muestra la gráfica
    plt.axis('off')
    plt.show()

# Prueba 3
def imprimir_peliculas(G):
# Crea una lista con los nodos que tienen al menos una arista con peso mayor o igual a 4
    nodos = [n for n in G.nodes() if any(G[u][v]['weight'] >= 4 for u, v in G.edges(n))]
    # Crea una subgrafo con los nodos seleccionados
    G_sub = G.subgraph(nodos)

    # Selecciona las aristas del subgrafo con peso mayor o igual a 4
    aristas = [(u, v) for u, v, d in G_sub.edges(data=True) if d['weight'] >= 4]

    # Verifica si la lista de aristas es vacía
    if len(aristas) == 0:
        print("No hay conexiones entre los nodos seleccionados.")
        return

    # Define los tamaños y colores de los nodos y aristas
    node_size = 500
    node_color = '#FFC300'
    edge_width = 1
    edge_color = '#C4C4C4'
    edge_cmap = plt.cm.Blues

    # Ajusta la posición de los nodos
    pos = nx.kamada_kawai_layout(G_sub)

    # Dibuja la gráfica del subgrafo
    nx.draw_networkx_nodes(G_sub, pos, nodelist=nodos, node_color=node_color, node_size=node_size)
    nx.draw_networkx_edges(G_sub, pos, edgelist=aristas, edge_color=edge_color, width=edge_width, edge_cmap=edge_cmap)
    nx.draw_networkx_edge_labels(G_sub, pos, font_size=10, edge_labels={(u, v): d['weight'] for u, v, d in G_sub.edges(data=True) if d['weight'] >= 4})
    nx.draw_networkx_labels(G_sub, pos, font_size=12)

    # Agrega un título al gráfico
    plt.title("Nodos con al menos una arista de peso mayor o igual a 4")

    for node in G_sub.nodes():
        pelicula = G_sub.nodes[node]['data']
        print("ID: {} - Película: {} - Año: {} - Género: {} - Director: {}".format(pelicula.id, pelicula.nombre, pelicula.año, pelicula.genero, pelicula.director))

    # Desactiva los ejes y muestra la gráfica
    plt.axis('off')
    plt.show()


# Lee las películas desde el archivo CSV
G = leer_peliculas()

# Prueba 1: Diez primero nodos
# dibujar_grafo(G)

# Prueba 2: Veinte primeros nodos y solo muestra las conexciones con un peso mayor que 1
# imprimir_nodos(G)

# Prueb 3: Todas las peliculas con conexciones con un peso mayor o igual a 4
imprimir_peliculas(G)