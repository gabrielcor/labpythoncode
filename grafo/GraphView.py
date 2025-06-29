import networkx as nx #pip install networkx
import matplotlib.pyplot as plt #pip install matplotlib
import mysql.connector  # Requires pip install mysql-connector-python
from matplotlib.colors import ListedColormap
import pygraphviz #ver post para instalar

# MariaDB connection configuration
conn = mysql.connector.connect(
    host="192.168.20.55",
    user="hassio",
    password="a1234567*",
    database="ravenlockslab",
    port=3306  # Default MariaDB port
)

# Crear cursor de MySQL Connector
cursor = conn.cursor()

# Buscar datos de puzzles y sus dependencias
cursor.execute('SELECT idPuzzle, PuzzleName, idStage FROM Puzzles')
puzzles = cursor.fetchall()
puzzle_names = {puzzle[0]: puzzle[1] for puzzle in puzzles}
stages = {puzzle[0]: puzzle[2] for puzzle in puzzles}

# Crear grafo dirigido
G = nx.DiGraph()

# Agregar nodos (puzzles)
G.add_nodes_from(puzzle_names.keys())

# agregar aristas (dependencias)
cursor.execute('SELECT idPuzzleDependsOn, idPuzzle FROM PuzzlePrecedences')
precedences = cursor.fetchall()
G.add_edges_from(precedences)

# colores dependiendo del stage
unique_stages = list(set(stages.values()))
cmap = plt.cm.tab10  # Using matplotlib's tab10 colormap
stage_colors = {stage: cmap(i % 10) for i, stage in enumerate(unique_stages)} # Asigno colores a cada stage
node_colors = [stage_colors[stages[node]] for node in G.nodes()]  # asigno el color a los nodos segun su stage

try:
    # graphviz layout modo dot para que se vea mas prolijo
    pos = nx.nx_agraph.graphviz_layout(
        G, 
        prog='dot',
        args="-Gnewrank='True' " # argumentos para organizar mejor el layour (ARREGLAR algunos no funcionan bien) -Gnodesep=1.0 -Granksep=1.5 -Gminlen=2 -Goverlap=prism 
    )
except ImportError:
    print("Warning: pygraphviz not found, using spring layout instead")
    # si no funciona la biblioteca pygraphviz uso spring layout los valores los robe de un ejemplo
    pos = nx.spring_layout(
        G, 
        k=1.0,          # Default: 0.1, Increased to 1.0 for more spacing
        iterations=100,  # Default: 50, Increased for better layout
        seed=42          # Consistent layouts between runs
    )
# Draw the graph
plt.figure(figsize=(20, 20)) # tamaño del grafico (ancho, alto)
nx.draw(G, pos,
        labels=puzzle_names,
        with_labels=True,
        node_color=node_colors, # colores de los nodos son los que asignamos
        node_size=500,
        font_size=9,
        arrowsize=18,
        edge_color='gray',
        width=1.2)

# no me funciona el legend ARREGLAR
legend_patches = [plt.Line2D([0], [0], 
                  marker='o', 
                  color='w', 
                  label=f'Stage {stage}',
                  markersize=15,
                  markerfacecolor=color) 
                 for stage, color in stage_colors.items()]

plt.legend(handles=legend_patches, 
           title="Stages",
           loc='upper right',
           bbox_to_anchor=(1.15, 1),  # Position legend outside axes
           fontsize=10,
           title_fontsize=12)

# Adjust layout manually
plt.subplots_adjust(
    left=0.1,    # Left margin
    right=0.85,  # Right margin (space for legend)
    top=0.9,     # Top margin
    bottom=0.1   # Bottom margin
)

plt.title("Grafo de dependencias - coloreado", fontsize=14, pad=20)
plt.show()

cursor.close()
conn.close()