import heapq          # Para usar una cola de prioridad 
import random          # Para generar conexiones aleatorias entre palabras
import networkx as nx  # Para crear y manejar grafos con nodos y aristas
import matplotlib.pyplot as plt  # Para graficar el grafo

#Función: para cargar diccionario
def datos_diccionario(ruta):
    diccionario = {}  # Diccionario vacío donde se guardan las claves y valores
    with open(ruta, 'r', encoding='utf-8') as f:  # Abre el archivo en modo lectura en utf-8
        for linea in f:  # Recorre cada línea del archivo
            if ':' in linea:  # Si la línea contiene ":" se considera válida
                palabra, significado = linea.strip().split(':', 1)  # Separa solo en el primer ":"
                diccionario[palabra.strip()] = significado.strip()  # Guarda en el diccionario
    return diccionario  # Devuelve el diccionario ya cargado






#Función: valor_ascii
def valor_ascii(palabra):
    return sum(ord(c) for c in palabra) 







#Función: armar_grafo
def armar_grafo(diccionario, conexiones_por_nodo=(1, 2)):
    palabras = list(diccionario.keys())#Se convierte las claves en una sola lista para ser procesadas
    random.shuffle(palabras)#se mezcla el orden de las palabras para que las conexiones sean randomicamente asignadas
    grafo = {palabra: [] for palabra in palabras}# Inicializamos cada palabra con una lista vacía de vecinos
    
    for palabra in palabras:#1. Para cada palabra en la lista de palabras
        posibles_vecinos = [p for p in palabras if p != palabra]#2. Excluimos la palabra actual de sus posibles vecinos
        num_conexiones = random.randint(conexiones_por_nodo[0], conexiones_por_nodo[1])# 3. Número de conexiones aleatorias
        vecinos = random.sample(posibles_vecinos, num_conexiones)#4. Seleccionamos aleatoriamente los vecinos
        
        for v in vecinos:# Recorremos cada vecino seleccionado
            if v not in grafo[palabra]:# Añadimos la conexión al grafo
                grafo[palabra].append(v)
            if palabra not in grafo[v]:# Aseguramos que la conexión es bidireccional con la palabra actual
                grafo[v].append(palabra)
    return grafo# Devuelve el grafo construido







#Función: busqueda_uniforme (Uniform Cost Search)
def busqueda_uniforme(diccionario, grafo, inicio, objetivo):
    visitados = set()  # Conjunto para guardar los nodos ya visitados
    cola = [(0, inicio)]  # Cola de prioridad con tuplas (costo_acumulado, nodo)
    caminos = {inicio: None}  # Para reconstruir el camino (de hijo → padre)
    costos = {inicio: 0}  # Guarda el costo total mínimo conocido hasta cada nodo
    recorrido = []  # Guarda el orden en que se visitan los nodos

    # Mientras haya nodos en la cola (aún hay caminos posibles)
    while cola:
        costo, actual = heapq.heappop(cola)  # Saca el nodo con menor costo acumulado
        if actual in visitados:  # Si ya fue visitado, lo saltamos
            continue

        visitados.add(actual)  # Marcamos este nodo como visitado
        recorrido.append(actual)  # Guardamos el orden de visita
        print(f"Visitando: {actual} (costo acumulado={costo})")  # Imprime progreso

        # Si llegamos al objetivo, reconstruimos la ruta y la devolvemos
        if actual == objetivo:
            ruta = []  # Lista vacía para reconstruir el camino
            while actual:  # Retrocede desde el objetivo hasta el inicio
                ruta.append(actual)
                actual = caminos[actual]  # Retrocede un paso
            ruta.reverse()  # Invierte la lista para que empiece desde el inicio
            return ruta, costos, recorrido  # Devuelve la ruta encontrada, los costos y el recorrido

        # Si no llegamos aún, expandimos los vecinos
        for vecino in grafo.get(actual, []):  # Recorre los vecinos del nodo actual
            if vecino not in visitados:  # Si aún no fue visitado
                nuevo_costo = costo + valor_ascii(vecino)  # Calcula el costo total hasta el vecino
                # Si el vecino no tiene costo o este nuevo es más bajo, lo actualizamos
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    caminos[vecino] = actual  # Guardamos el "padre" para reconstruir la ruta
                    heapq.heappush(cola, (nuevo_costo, vecino))  # Lo añadimos a la cola con su costo

    # Si salimos del bucle sin encontrar el objetivo, no hay ruta posible
    return None, costos, recorrido








# Se dibuja el grafo con NetworkX y se resalta la ruta en rojo
def graficar_grafo(grafo, ruta=None):
    G = nx.Graph()  # se crea un grafo no dirigido
    # se añaden las aristas al grafo
    for nodo, vecinos in grafo.items():
        for v in vecinos:
            # arista con peso igual a la diferencia absoluta de valores ASCII
            G.add_edge(nodo, v, weight=abs(valor_ascii(nodo) - valor_ascii(v)))

    # se calculan posiciones en 2D para dibujar los nodos
    pos = nx.spring_layout(G, seed=42, k=1.2)

    #colores de los nodos
    node_colors = []
    for n in G.nodes():
        if ruta and n in ruta:
            node_colors.append("red")  # rojo para la ruta
        else:
            node_colors.append("lightgray")  # gris para los demas nodos

    # se crea una figura de tamaño 12x7
    plt.figure(figsize=(12, 7))
    
    # se dibujan los nodos del grafo
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=900, edgecolors="black")

    # se dibujan las aristas
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7)

    # se añaden etiquetas nombre y valor ASCII
    etiquetas = {n: f"{n}\n({valor_ascii(n)})" for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=etiquetas, font_size=9)

    # si hay una ruta, dibuja sus aristas en rojo
    if ruta:
        edges_path = list(zip(ruta, ruta[1:]))  # crea pares de nodos consecutivos en la ruta
        nx.draw_networkx_edges(G, pos, edgelist=edges_path, edge_color="red", width=2)


    plt.title(" Grafo de Búsqueda Uniforme (Ruta resaltada en rojo)", fontsize=13)
    
    plt.axis("off")  # Quita los ejes
    plt.tight_layout()  # Ajusta los margenes
    plt.show()  # Muestra la ventana del grafico











if __name__ == "__main__":
    # se cargan las palabras
    diccionario = datos_diccionario("datos.txt")

    # se construye el grafo aleatorio de palabras
    grafo = armar_grafo(diccionario)

    # Nodo inicial y el nodo objetivo
    inicio = "casa"
    objetivo = "perro"
    
    print(f" Buscando desde '{inicio}' hasta '{objetivo}'...\n")

    # se ejecuta la busqueda de costo uniforme
    ruta, costos, recorrido = busqueda_uniforme(diccionario, grafo, inicio, objetivo)

    # Si hay ruta se muestra y se grafica
    if ruta:
        print("\n Ruta encontrada:")
        print(" → ".join(ruta))  # se imprime la secuencia de palabras
        print("\nSignificado:", diccionario.get(objetivo, "No encontrado"))  # se muestra el significado
        graficar_grafo(grafo, ruta)  # se dibuja el grafo con la ruta resaltada
    else:
        # Si no se encontró ningún camino hacia el objetivo
        print(f"\n!!!!!!! No se encontró una ruta hacia '{objetivo}'.")
        graficar_grafo(grafo)  # se dibuja el grafo normal
