from tkinter import *
from tkinter import ttk,font,messagebox
from math import inf
from os import path
import numpy as np
import pulp

# Pio - TempledUX
# Last edit: 07/11/2020
# Contact: edux98g@gmail.com
# Public license: MIT

class Grafo():
    def __init__(self, nodos:set, aristas:set, costes:dict):
        self.nodos = nodos
        self.aristas = aristas
        self.costes = costes
    
    def getNodos(self):
        return self.nodos

    def getAristas(self):
        return self.aristas

    def coste(self,arista):
        return self.costes[arista]

    def distancia(self,nodo1,nodo2):
        """
        Devuelve el coste entre dos nodos (no la distancia)
        """
        return self.costes.get((nodo1,nodo2),inf)

    def buildMatrizAdyacencia(self):
        """
        Construye la matriz de adyacencia en base a la información del grafo como un ndarray de NumPy y lo devuelve
        """
        numNodos = len(self.nodos)
        matriz = np.empty((numNodos,numNodos))
        for nodo in sorted(self.nodos):
            nodolista = []
            for nodo2 in sorted(self.nodos):
                if (nodo,nodo2) in self.aristas:
                    nodolista.append(1)
                else:
                    nodolista.append(0)
            matriz[nodo] = nodolista
        return matriz

            ################
            # LOCALIZATION #
            ################

def getLocalization(language):
    if language == "spanish":
        return {
            "language_spanish": "Español",
            "language_english": "Inglés",
            "language_menu": "Lenguaje",
            "title": "Pio - Teoría de grafos",
            "labelframe1_title": "Configuración del problema",
            "labelframe1_nodenumber_label": "Número de nodos:",
            "labelframe1_algorithm_label": "Algoritmo de operación:",
            "labelframe1_opmode_label": "Modo de operación:",
            "labelframe1_button_setupmatrix": "Preparar matriz",
            "labelframe1_button_updatedata": "Actualizar datos",
            "dijkstrasubframe_origin_node": "Nodo de origen:",
            "dijkstrasubframe_destination_node": "Nodo de destino:",
            "bellmankalabasubframe_last_node": "Nodo final:",
            "labelframe2_title": "Matriz de costes del grafo",
            "labelframe2_solve_button": "Resolver",
            "labelframe2_symmetrize_button": "Simetrizar",
            "labelframe2_drop_matrix_button": "Reconfigurar matriz",
            "labelframe2_clear_ties_checkbox": "Sin lazos",
            "labelframe3_title": "Resolución del problema e información de estado",
            "labelframe3_msg_waiting_data": "Esperando datos del problema...",
            "labelframe3_msg_waiting_solve": "OK \nEsperando orden para ejecutar resolución...\n",
            "labelframe3_msg_waiting_problem": "Actualiza la información del problema antes de continuar...",
            "error_invalidentry_title": "Entrada vacía o inválida",
            "error_invalidentry_desc": "Especifica un número de nodos correcto antes de continuar.",
            "error_outofrange_title": "Valor fuera de rango",
            "error_outofrange_desc": "El número de nodos es demasiado grande. El máximo de nodos disponible es 25",
            "error_invalidentryalg_title": "Entrada vacía o inválida",
            "error_invalidentryalg_desc": "Especifica un algoritmo de resolución antes de continuar.",
            "error_invalidentrystartendnodes_title": "Entrada vacía o inválida",
            "error_invalidentrystartendnodes_desc": "Configura adecuadamente el nodo inicial y final para el algoritmo de Dijkstra y después actualiza los datos.",
            "error_outofrangestartnode_title": "Valor fuera de rango",
            "error_outofrangestartnode_desc": "El valor introducido para el nodo inicial no se corresponde con ningún nodo existente. Observación: los nodos se numeran empezando desde el 0.",
            "error_outofrangeendnode_title": "Valor fuera de rango",
            "error_outofrangeendnode_desc": "El valor introducido para el nodo final no se corresponde con ningún nodo existente. Observación: los nodos se numeran empezando desde el 0.",
            "error_invalidentrybellmanend_title": "Entrada vacía o inválida",
            "error_invalidentrybellmanend_desc": "Configura adecuadamente el nodo final para el algoritmo de Bellman-Kalaba antes de continuar.",
            "error_outofrangebellmanend_title": "Valor fuera de rango",
            "error_outofrangebellmanend_desc": "El valor introducido para el nodo final no se corresponde con ningún nodo existente.",
            "error_invalidentrysolin_title": "Entrada vacía o inválida",
            "error_invalidentrysolin_desc": "Configura adecuadamente el modo de operación del algoritmo de Solin antes de continuar.",
            "error_solve_noconfig_title": "Configuración sin finalizar",
            "error_solve_noconfig_desc": "Configura los datos del problema (si es necesario) y pulsa 'Actualizar datos' antes de continuar.",
            "error_solve_connectivity_title": "Conectividad del grafo",
            "error_solve_connectivity_desc": "El grafo introducido no parece ser conexo. Puedes utilizar un algoritmo sobre cada componente conexa o revisar la matriz de costes.",
            "alg_dijkstra_desc": "Algoritmo elegido: Dijkstra\nPermite encontrar el camino mínimo desde el nodo de origen hasta el nodo de destino.\n\n",
            "alg_bellmankalaba_desc": "Algoritmo elegido: Bellman-Kalaba\nPermite encontrar todos los caminos mínimos del grafo hasta un nodo final.\n\n",
            "alg_floyd_desc": "Algoritmo elegido: Floyd\nPermite calcular los caminos mínimos entre dos pares cualesquiera de nodos.\n\n",
            "alg_solin_desc": "Algoritmo elegido: Solin\nPermite calcular el árbol recubridor mínimo o máximo de un grafo.\n",
            "alg_solin_desc2": "\nObservación: dado que trabajamos con un árbol, asigna los valores a la mitad de la matriz y simetrizala.\n\n",
            "alg_transportation_desc": "Algoritmo elegido: Transporte\nPermite resolver un problema formulado mediante el modelo de transporte (nodos de producción, intermedios y de destino).",
            "alg_transportation_desc2": "\nElige la cabecera de cada nodo para determinar como se comportará bajo el modelo de transporte y para ajustar sus valores de producción/demanda.\n",
            "dijkstra_pipeline_title": "Resolución del problema mediante el algoritmo de Dijkstra: \n \n",
            "dijkstra_pipeline_1": "Nodo óptimo: {} \nM=[{}] \n",
            "dijkstra_pipeline_2": "Nodo óptimo: {} \nM={} \n",
            "dijkstra_pipeline_3": "\nEl algoritmo ha finalizado. La distancia mínima del nodo origen al nodo destino es {}. \n",
            "bellman_pipeline_title": "Resolución del problema mediante el algoritmo de Bellman-Kalaba: \n \n",
            "bellman_pipeline_1": "\nEl algoritmo ha finalizado. Las distancias mínimas de cada uno de los nodos al nodo final son los valores de V de la última iteracción. \n",
            "floyd_pipeline_title": "Resolución del problema mediante el algoritmo de Floyd: \n \n",
            "floyd_pipeline_1": "Matriz costes: \n",
            "floyd_pipeline_2": "Matriz penúltimos nodos: \n",
            "floyd_pipeline_3": "\nFinal:\n",
            "floyd_pipeline_4": "\nEl algoritmo ha finalizado. La matriz de costes del final contiene los caminos mínimos para ir de un nodo a otro y la matriz de penúltimos nodos del final contiene los penúltimos nodos de los caminos mínimos que unen dos nodos. \n",
            "solin_pipeline_title": "Resolución del problema mediante el algoritmo de Solin: \n \n",
            "solin_pipeline_1": "\nEl algoritmo ha finalizado. La matriz que se presenta a continuación es la que queda tras aplicar el algoritmo de Solin: \n",
            "transportation_pipeline_title": "\nInformación del problema\n",
            "transportation_pipeline_1": "Estado del problema: {}",
            "transportation_pipeline_2": "\nValor de la función objetivo: {}",
            "transportation_pipeline_3": "\nVariables:\n",
            "gui2_title": "Ajustar nodo {}",
            "gui2_radio1": "Origen",
            "gui2_label1": "Producción:",
            "gui2_radio2": "Destino",
            "gui2_label2": "Demanda:",
            "gui2_radio3": "Nodo intermedio",
            "gui2_save_button": "Guardar"
        }
    elif language == "english":
        return {
            "language_spanish": "Spanish",
            "language_english": "English",
            "language_menu": "Language",
            "title": "Pio - Graph theory solver",
            "labelframe1_title": "Problem configuration",
            "labelframe1_nodenumber_label": "Number of nodes:",
            "labelframe1_algorithm_label": "Algorithm:",
            "labelframe1_opmode_label": "Operation mode:",
            "labelframe1_button_setupmatrix": "Setup matrix",
            "labelframe1_button_updatedata": "Update problem data",
            "dijkstrasubframe_origin_node": "Origin node:",
            "dijkstrasubframe_destination_node": "Destination node:",
            "bellmankalabasubframe_last_node": "End node:",
            "labelframe2_title": "Cost matrix of the graph",
            "labelframe2_solve_button": "Solve",
            "labelframe2_symmetrize_button": "Symmetrize",
            "labelframe2_drop_matrix_button": "Rebuild matrix",
            "labelframe2_clear_ties_checkbox": "Clear ties",
            "labelframe3_title": "Problem solving information and log",
            "labelframe3_msg_waiting_data": "Waiting for problem data...",
            "labelframe3_msg_waiting_solve": "OK \nWaiting for request to solve problem...\n",
            "labelframe3_msg_waiting_problem": "Update the problem before continuing...",
            "error_invalidentry_title": "Empty or invalid entry",
            "error_invalidentry_desc": "Input a correct number of nodes before continuing.",
            "error_outofrange_title": "Out of range value",
            "error_outofrange_desc": "The number of nodes is too large. You can input a number of 25 nodes max.",
            "error_invalidentryalg_title": "Empty or invalid entry",
            "error_invalidentryalg_desc": "Input a solving algorithm before continuing",
            "error_invalidentrystartendnodes_title": "Empty or invalid entry",
            "error_invalidentrystartendnodes_desc": "Setup properly the origin and destination node for the Dijkstra algorithm and then update the problem data.",
            "error_outofrangestartnode_title": "Out of range value",
            "error_outofrangestartnode_desc": "The value entered for the origin node doesn't correspond to any existing node. Tip: nodes are numbered starting from 0.",
            "error_outofrangeendnode_title": "Out of range value",
            "error_outofrangeendnode_desc": "The value entered for the destination node doesn't correspond to any existing node. Tip: nodes are numbered starting from 0.",
            "error_invalidentrybellmanend_title": "Empty or invalid entry",
            "error_invalidentrybellmanend_desc": "Setup properly the destination node for the Bellman-Kalaba algorithm before continuing.",
            "error_outofrangebellmanend_title": "Out of range value",
            "error_outofrangebellmanend_desc": "The value entered for the destination node doesn't correspond to any existing node.",
            "error_invalidentrysolin_title": "Empty or invalid entry",
            "error_invalidentrysolin_desc": "Setup properly the Solin algorithm's operation mode before continuing",
            "error_solve_noconfig_title": "Empty configuration",
            "error_solve_noconfig_desc": "Setup the problem data (if necessary) and click 'Update problem data' before continuing.",
            "error_solve_connectivity_title": "Graph connectivity",
            "error_solve_connectivity_desc": "The entered graph doesn't seem to be connected. You can use one algorithm for every connected component or check the cost matrix.",
            "alg_dijkstra_desc": "Selected algorithm: Dijkstra\nFinds the shortest path from the origin node to the destination node.\n\n",
            "alg_bellmankalaba_desc": "Selected algorithm: Bellman-Kalaba\nFinds the shortest paths from every node of the graph to a destination node.\n\n",
            "alg_floyd_desc": "Selected algorithm: Floyd\nFinds the shortest paths between every pair of nodes of the graph.\n\n",
            "alg_solin_desc": "Selected algorithm: Solin\nFinds the minimum or maximum spanning tree of a graph.\n",
            "alg_solin_desc2": "\nTip: since we work with a tree, input values for half of the matrix and symmetrize it.\n\n",
            "alg_transportation_desc": "Selected algorithm: Transportation\nSolves a problem formulated under the transportation model (production nodes, intermediate nodes and destination nodes).",
            "alg_transportation_desc2": "\nSelect the header of a node for setting how it will behave under the transportation model and for setting up its production/demand values.\n",
            "dijkstra_pipeline_title": "Resolution of the problem using Dijkstra's algorithm: \n \n",
            "dijkstra_pipeline_1": "Optimal node: {} \nM=[{}] \n",
            "dijkstra_pipeline_2": "Optimal node: {} \nM={} \n",
            "dijkstra_pipeline_3": "\nAlgorithm has finished. The minimum distance from origin node to destination node is {}. \n",
            "bellman_pipeline_title": "Resolution of the problem using Bellman-Kalaba's algorithm: \n \n",
            "bellman_pipeline_1": "\nAlgorithm has finished. The minimum distances from each node to the destination node are the values V of the last iteration. \n",
            "floyd_pipeline_title": "Resolution of the problem using Floyd's algorithm: \n \n",
            "floyd_pipeline_1": "Cost matrix: \n",
            "floyd_pipeline_2": "Penultimate nodes matrix: \n",
            "floyd_pipeline_3": "\nEnd:\n",
            "floyd_pipeline_4": "\nAlgorithm has finished. The last cost matrix contains the shortest paths between every pair of nodes and the last penultimate nodes matrix contains the penultimate nodes of the shortest paths between two nodes. \n",
            "solin_pipeline_title": "Resolution of the problem using Solin's algorithm: \n \n",
            "solin_pipeline_1": "\nAlgorithm has finished. The next matrix is the one that remains after applying Solin's algorithm: \n",
            "transportation_pipeline_title": "\nProblem info\n",
            "transportation_pipeline_1": "Problem status: {}",
            "transportation_pipeline_2": "\nValue of the target function: {}",
            "transportation_pipeline_3": "\nVariables:\n",
            "gui2_title": "Node {} conf.",
            "gui2_radio1": "Origin",
            "gui2_label1": "Production:",
            "gui2_radio2": "Destination",
            "gui2_label2": "Demand:",
            "gui2_radio3": "Intermediate node",
            "gui2_save_button": "Save"
        }

def initLocalization() -> str:
    try:
        if not (path.exists('pio_settings.txt')):
            infile = open('pio_settings.txt','w')
            infile.write('localization=english')
            infile.close()
            raise Exception
        infile = open('pio_settings.txt','r')
        data = infile.read()
        idx = data.find('=')
        locsetting = data[idx+1:]
    except Exception:
        return 'english'
    return locsetting

def saveLocalization(locsetting: str, app):
    try:
        outfile = open('pio_settings.txt','w')
        outfile.write(f"localization={locsetting}")
        outfile.close()
    except Exception:
        return 'error'
    app.destroy()
    Aplicacion()

                #######
                # GUI #
                #######

class Aplicacion():
    def __init__(self):
        self.loc = getLocalization(initLocalization())

        self.principal = Tk()
        self.principal.title(self.loc['title'])
        self.principal.geometry("900x800")

        menubar = Menu(self.principal)
        languagemenu = Menu(menubar, tearoff=0)
        languagemenu.add_command(label=self.loc['language_spanish'], command=lambda s="spanish", app=self.principal:saveLocalization(s,app))
        languagemenu.add_command(label=self.loc['language_english'], command=lambda s="english", app=self.principal:saveLocalization(s,app))
        menubar.add_cascade(label=self.loc['language_menu'], menu=languagemenu)
        self.principal.config(menu=menubar)

        self.botoneraDibujada = False

        """
        -------------------------------------------------------------------------------
        Documentación de las variables
        -------------------------------------------------------------------------------
        matriz: diccionario con los valores de la matriz
        referenciasnodoslazo: lista que guarda las entradas que representan lazos
        celdasTitulo: diccionario con las entradas que representan nodos de la matriz (Acceder con ri (fila i) o cj (columna j))
        grafo: variable auxiliar para guardar un objeto de tipo Grafo asociado a la matriz del problema
        demandasProducciones: diccionario con la demanda o producción de cierto nodo. Leyenda: las claves son [nodo (int)] = (k,valor) con
            k = 0 -> Producción
            k = 1 -> Demanda
            k = 2 -> Nodo intermedio
        operationStatus: estado del programa. Hay 3 opciones:
            0: matriz sin configurar
            1: datos sin actualizar (semiconfigurado)
            2: preparado para resolución
        """
        self.matriz = {}
        self.referenciasnodoslazo = []
        self.celdasTitulo = {}
        self.grafo = 0
        self.demandasProducciones = {}
        self.operationStatus = 0

        #Panel de información y subpaneles
        self.panelmodo = ttk.LabelFrame(self.principal, text=self.loc['labelframe1_title'])
        self.panelinfo = ttk.Frame(self.panelmodo)
        self.panelinfosolin = ttk.Frame(self.panelmodo)
        self.panelbotones = ttk.Frame(self.panelmodo)
        self.textnumnodos = ttk.Label(self.panelinfo, text=self.loc['labelframe1_nodenumber_label'])
        self.entrynumnodos = ttk.Entry(self.panelinfo, width=7)
        self.textalgoritmo = ttk.Label(self.panelinfo, text=self.loc['labelframe1_algorithm_label'])
        self.textmodesolin = ttk.Label(self.panelinfosolin,text=self.loc['labelframe1_opmode_label'])
        self.selalgoritmo = ttk.Combobox(self.panelinfo, state="readonly")
        # Asignación deleted (06/11/20), framework required
        self.selalgoritmo["values"] = ["Dijkstra","Bellman-Kalaba","Floyd","Solin","Transporte"]
        self.selalgoritmo.bind("<<ComboboxSelected>>",self.algorithmSelected)
        self.selmodosolin = ttk.Combobox(self.panelinfosolin, state="readonly")
        self.selmodosolin["values"] = ["Maximizar","Minimizar"]
        self.buttoncontinue = ttk.Button(self.panelbotones, text=self.loc['labelframe1_button_setupmatrix'], command=self.generateMatrix)

        #Subpanel Dijkstra
        self.panelinfodijkstra = ttk.Frame(self.panelmodo)
        self.textfirstnodedijkstra = ttk.Label(self.panelinfodijkstra,text=self.loc['dijkstrasubframe_origin_node'])
        self.textlastnodedijkstra = ttk.Label(self.panelinfodijkstra, text=self.loc['dijkstrasubframe_destination_node'])
        self.firstnodedijkstra = ttk.Entry(self.panelinfodijkstra,width=5)
        self.lastnodedijkstra = ttk.Entry(self.panelinfodijkstra,width=5)

        #Subpanel Bellman-Kalaba
        self.panelinfokalaba = ttk.Frame(self.panelmodo)
        self.textlastnodebellman = ttk.Label(self.panelinfokalaba, text=self.loc['bellmankalabasubframe_last_node'])
        self.lastnodebellman = ttk.Entry(self.panelinfokalaba,width=5)

        self.panelintermedio = ttk.Frame(self.principal)

        #Panel de matriz y subpaneles
        self.panelmatriz = ttk.LabelFrame(self.panelintermedio, text=self.loc['labelframe2_title'])
        self.panelmatrizmain = ttk.Frame(self.panelmatriz)
        self.panelmatrizbotonera = ttk.Frame(self.panelmatriz)

        #self.selalgoritmomatriz = ttk.Label(self.panelmatrizbotonera, font=font.Font(size=10))
        self.buttonresolver = ttk.Button(self.panelmatrizbotonera,text=self.loc['labelframe2_solve_button'],command=self.solve)
        self.buttonsim = ttk.Button(self.panelmatrizbotonera,text=self.loc['labelframe2_symmetrize_button'],command=self.simetrizeMatrix)
        self.loops = IntVar(self.principal)
        self.noloopscheck = ttk.Checkbutton(self.panelmatrizbotonera, text=self.loc['labelframe2_clear_ties_checkbox'], variable=self.loops, command=self.lazosCallback)
        self.reconfiguratebutton = ttk.Button(self.panelmatrizbotonera, text=self.loc['labelframe2_drop_matrix_button'], command=self.reconfigurate)

        #Panel de resolución y subpaneles
        self.panelresolucion = ttk.LabelFrame(self.panelintermedio, text=self.loc['labelframe3_title'])
        self.solveroutput = Text(self.panelresolucion, width=71)
        self.outputscroll = ttk.Scrollbar(self.panelresolucion, command=self.solveroutput.yview)
        self.solveroutput.configure(yscrollcommand=self.outputscroll.set)
        self.solveroutput.insert(END,self.loc['labelframe3_msg_waiting_data'])

        #==GEOMETRIA==
        #Geometría de paneles
        self.panelmodo.pack(side=TOP,fill=NONE,expand=False,padx=5,pady=(20,5))
        self.panelintermedio.pack(side=TOP,fill=NONE,expand=False,padx=5,pady=(20,5))
        self.panelmatriz.pack(side=LEFT,fill=X,expand=True,padx=(0,20),pady=0)
        self.panelmatrizmain.pack(side=TOP,fill=X,expand=True,padx=0,pady=0)
        self.panelmatrizbotonera.pack(side=TOP,fill=X,expand=True,padx=0,pady=5)
        self.panelresolucion.pack(side=RIGHT,fill=Y,expand=False,padx=0,pady=0)

        #Geometría panel de modo y subpaneles
        self.panelinfo.pack(side=TOP,fill=BOTH,expand=True,padx=5,pady=5)
        self.textnumnodos.pack(side=LEFT,fill=BOTH,expand=True,padx=5,pady=5)
        self.entrynumnodos.pack(side=LEFT,fill=BOTH,expand=True,padx=5,pady=5)
        self.textalgoritmo.pack(side=LEFT,fill=BOTH,expand=True,padx=5,pady=5)
        self.selalgoritmo.pack(side=LEFT,fill=BOTH,expand=True,padx=5,pady=5)
        self.panelbotones.pack(side=TOP,fill=BOTH,expand=True,padx=5,pady=5)
        self.buttoncontinue.pack(side=RIGHT,fill=Y,expand=True,padx=5,pady=5)
        self.selmodosolin.pack(side=RIGHT,fill=None,expand=False,padx=5,pady=0)
        self.textmodesolin.pack(side=RIGHT,fill=None,expand=False,padx=5,pady=0)
        self.textfirstnodedijkstra.pack(side=LEFT,fill=None,expand=False,padx=5,pady=0)
        self.firstnodedijkstra.pack(side=LEFT,fill=None,expand=False,padx=5,pady=0)
        self.textlastnodedijkstra.pack(side=LEFT,fill=None,expand=False,padx=5,pady=0)
        self.lastnodedijkstra.pack(side=LEFT,fill=None,expand=False,padx=5,pady=0)
        self.textlastnodebellman.pack(side=LEFT,fill=None,expand=False,padx=5,pady=0)
        self.lastnodebellman.pack(side=LEFT,fill=None,expand=False,padx=5,pady=0)

        #Geometría panel de resolución
        self.solveroutput.pack(side=LEFT,fill=BOTH,expand=True,padx=(5,0),pady=5)
        self.outputscroll.pack(side=RIGHT,fill=Y,expand=True)

        self.principal.mainloop()

    def checkErrors(self):
        """
        Comprueba errores. Si todo está correcto devuelve True, en caso contrario devuelve False.
        """
        #Numero de nodos de la matriz
        try:
            numNodos = int(self.entrynumnodos.get())
        except ValueError:
            messagebox.showerror(self.loc['error_invalidentry_title'], self.loc['error_invalidentry_desc'])
            return False
        algoritmo = self.selalgoritmo.get()
        if numNodos > 25:
            messagebox.showerror(self.loc['error_outofrange_title'], self.loc['error_outofrange_desc'])
            return False
        #Algoritmo elegido
        if algoritmo == '':
            messagebox.showerror(self.loc['error_invalidentryalg_title'],self.loc['error_invalidentryalg_desc'])
            return False
        if algoritmo == "Dijkstra":
            #Sintaxis
            try:
                fn = int(self.firstnodedijkstra.get())
                ln = int(self.lastnodedijkstra.get())
            except ValueError:
                messagebox.showerror(self.loc['error_invalidentrystartendnodes_title'],self.loc['error_invalidentrystartendnodes_desc'])
                return False
            #Rango
            fn = int(self.firstnodedijkstra.get())
            ln = int(self.lastnodedijkstra.get())
            limite = numNodos
            if fn < 0 or fn > limite-1:
                messagebox.showerror(self.loc['error_outofrangestartnode_title'], self.loc['error_outofrangestartnode_desc'])
                return False
            if ln < 0 or ln > limite-1:
                messagebox.showerror(self.loc['error_outofrangeendnode_title'], self.loc['error_outofrangeendnode_desc'])
                return False
        if algoritmo == "Bellman-Kalaba":
            #Sintaxis
            try:
                fn = int(self.lastnodebellman.get())
            except ValueError:
                messagebox.showerror(self.loc['error_invalidentrybellmanend_title'],self.loc['error_invalidentrybellmanend_desc'])
                return False
            #Rango
            if fn < 0 or fn > numNodos-1:
                messagebox.showerror(self.loc['error_outofrangebellmanend_title'],self.loc['error_outofrangebellmanend_desc'])
                return False
        if algoritmo == "Solin":
            if self.selmodosolin.get() == '':
                messagebox.showerror(self.loc['error_invalidentrysolin_title'],self.loc['error_invalidentrysolin_desc'])
                return False
        return True

    def generateMatrix(self):
        """
        Función llamada al pulsar el botón preparar matriz
        """
        #Comprobación de errores general antes de continuar
        if not self.checkErrors(): return
        self.dropMatrix()
        self.switchMatrixButtons('enabled')
        self.buttoncontinue.configure(text=self.loc['labelframe1_button_updatedata'], command=self.updateMatrix)
        #self.selalgoritmomatriz.configure(text="Algoritmo elegido: " + self.selalgoritmo.get())
        self.loops.set(0)
        self.switchConfiguration('disabled')
        numNodos = int(self.entrynumnodos.get())
        #Titulos
        for i in range(numNodos):
            caja = ttk.Entry(self.panelmatrizmain,width=5)
            self.ajustarTitulo(caja,i)
            caja.configure(state="disabled")
            self.celdasTitulo['c'+str(i)] = caja
            if self.selalgoritmo.get() == 'Transporte':
                caja.bind("<Button-1>", lambda event, node=i, yo=self : ElementViewTransporte(self.principal, node,yo,self.loc))
            caja.grid(column=i+1,row=0,padx=3,pady=3,sticky=(N,S,E,W))
        for i in range(numNodos):
            caja = ttk.Entry(self.panelmatrizmain,width=5)
            self.ajustarTitulo(caja,i)
            caja.configure(state="disabled")
            self.celdasTitulo['r'+str(i)] = caja
            if self.selalgoritmo.get() == 'Transporte':
                caja.bind("<Button-1>", lambda event, node=i, yo=self : ElementViewTransporte(self.principal, node,yo,self.loc))
            caja.grid(column=0,row=i+1,padx=3,pady=3,sticky=(N,S,E,W))
        #Matriz de datos
        for row in range(numNodos):
            for col in range(numNodos):
                textvar = StringVar(self.principal)
                caja = ttk.Entry(self.panelmatrizmain,width=5,textvariable=textvar)
                if col == row:
                    self.referenciasnodoslazo.append(caja)
                caja.grid(column=col+1,row=row+1,padx=3,pady=3,sticky=(N,S,E,W))
                key = (row,col)
                self.matriz[key] = textvar
        self.dibujarBotonera()
        self.solveroutput.delete('1.0',END)
        self.writeprobleminfo()
        self.solveroutput.insert(END, self.loc['labelframe3_msg_waiting_solve'])
        self.operationStatus = 2

    def ajustarTitulo(self,caja,i):
        """
        Ajusta el título de la caja proporcionada. i es el número que se muestra en la misma
        """
        if self.selalgoritmo.get() == "Dijkstra":
            if i == int(self.firstnodedijkstra.get()):
                caja.insert(0,str(i)+'*O')
            elif i == int(self.lastnodedijkstra.get()):
                caja.insert(0,str(i)+'*D')
            else:
                caja.insert(0,str(i))
        elif self.selalgoritmo.get() == "Bellman-Kalaba":
            if i == int(self.lastnodebellman.get()):
                caja.insert(0,str(i)+'*D')
            else:
                caja.insert(0,str(i))
        #Puede que sobre
        else:
            caja.insert(0,str(i))

    def updateMatrix(self):
        """
        Función llamada al pulsar el botón de actualizar datos
        """
        if not self.checkErrors(): return
        if self.selalgoritmo.get() == "Dijkstra":
            fn = self.firstnodedijkstra.get()
            ln = self.lastnodedijkstra.get()
            #Limpiar
            self.dijkstraClearTitles()
            self.unbindTitles()
            #Asignar datos
            for celda in [self.celdasTitulo['c'+fn],self.celdasTitulo['r'+fn]]:
                celda.configure(state="enabled")
                celda.insert(END,'*O')
                celda.configure(state="disabled")
            for celda in [self.celdasTitulo['c'+ln],self.celdasTitulo['r'+ln]]:
                celda.configure(state="enabled")
                celda.insert(END,'*D')
                celda.configure(state="disabled")
        elif self.selalgoritmo.get() == "Bellman-Kalaba":
            ln = self.lastnodebellman.get()
            #Limpiar
            self.dijkstraClearTitles()
            self.unbindTitles()
            for celda in [self.celdasTitulo['c'+ln],self.celdasTitulo['r'+ln]]:
                celda.configure(state="enabled")
                celda.insert(END,'*D')
                celda.configure(state="disabled")
        elif self.selalgoritmo.get() == 'Transporte':
            self.dijkstraClearTitles()
            for celda in self.celdasTitulo.values():
                celda.bind("<Button-1>", lambda event, node=int(celda.get()), yo=self : ElementViewTransporte(self.principal, node,yo,self.loc))
        self.switchMatrixButtons('enabled')
        self.solveroutput.delete('1.0',END)
        self.writeprobleminfo()
        self.solveroutput.insert(END, self.loc['labelframe3_msg_waiting_solve'])
        self.operationStatus = 2
    
    def dijkstraClearTitles(self):
        """
        Limpia todos los títulos especiales de las cajas (los precedidos por *)
        """
        for celda in self.celdasTitulo.values():
            celda.configure(state="enabled")
            index = celda.get().find('*')
            if index != -1: celda.delete(index,END)
            celda.configure(state="disabled")
    
    def unbindTitles(self):
        """
        Desacopla los menus secundarios del modo de trasporte de las cajas y limpia la memoria de datos
        """
        for celda in self.celdasTitulo.values():
            celda.unbind("<Button-1>")
        self.demandasProducciones = {}

    def dropMatrix(self):
        """
        Limpia la matriz entera
        """
        for widget in self.panelmatrizmain.grid_slaves():
            widget.grid_forget()
        self.matriz = {}
        self.celdasTitulo = {}

    def simetrizeMatrix(self):
        """
        Simetriza la matriz de costes
        """
        def parseToInt(string):
            if string == '': return 0
            else: return int(string)

        numNodos = int(self.entrynumnodos.get())
        for i in range(numNodos):
            for j in range(numNodos):
                actual = self.matriz[(i,j)].get()
                objetivo = self.matriz[(j,i)].get()
                if actual == '':
                    self.matriz[(i,j)].set(objetivo)
                    continue
                else:
                    preferido = max(int(actual),parseToInt(objetivo))
                    self.matriz[(i,j)].set(str(preferido))

    def switchMatrixButtons(self,switch):
        self.reconfiguratebutton.configure(state=switch)
        self.buttonsim.configure(state=switch)
        self.buttonresolver.configure(state=switch)
        self.noloopscheck.configure(state=switch)

    def dibujarBotonera(self):
        if not self.botoneraDibujada:
            self.reconfiguratebutton.pack(side=LEFT,fill=NONE,expand=False,padx=3,pady=5)
            self.buttonresolver.pack(side=RIGHT,fill=NONE,expand=False,padx=(5,3),pady=5)
            self.buttonsim.pack(side=RIGHT,fill=NONE,expand=False,padx=5,pady=5)
            self.noloopscheck.pack(side=RIGHT,fill=Y,expand=False,padx=(5,15),pady=5)
            #self.selalgoritmomatriz.pack(side=RIGHT,fill=Y,expand=True,padx=5,pady=5)
            self.botoneraDibujada = True

    def algorithmSelected(self,event):
        """
        Función llamada al elegir un algoritmo en el desplegable
        """
        self.modosubpanelupdate()
        self.solveroutput.delete('1.0',END)
        #self.selalgoritmomatriz.configure(text="Algoritmo elegido: " + self.selalgoritmo.get())
        self.dijkstraClearTitles()
        self.writeprobleminfo()
        self.operationStatus = 1

    def writeprobleminfo(self):
        if self.selalgoritmo.get() == 'Dijkstra':
            self.solveroutput.insert(END, self.loc['alg_dijkstra_desc'])
        elif self.selalgoritmo.get() == 'Bellman-Kalaba':
            self.solveroutput.insert(END, self.loc['alg_bellmankalaba_desc'])
        elif self.selalgoritmo.get() == 'Floyd':
            self.solveroutput.insert(END, self.loc['alg_floyd_desc'])
        elif self.selalgoritmo.get() == 'Solin':
            self.solveroutput.insert(END, self.loc['alg_solin_desc'])
            self.solveroutput.insert(END, self.loc['alg_solin_desc2'])
        elif self.selalgoritmo.get() == 'Transporte':
            self.solveroutput.insert(END, self.loc['alg_transportation_desc'])
            self.solveroutput.insert(END, self.loc['alg_transportation_desc2'])
        self.solveroutput.insert(END, self.loc['labelframe3_msg_waiting_problem'])

    def modosubpanelupdate(self):
        self.clearPanelModo()
        self.panelinfo.pack(side=TOP,fill=BOTH,expand=True,padx=5,pady=5)
        choice = self.selalgoritmo.get()
        if choice == "Dijkstra":
            self.panelinfodijkstra.pack(side=TOP,fill=BOTH,expand=True,padx=5,pady=5)
        else:
            self.panelinfodijkstra.pack_forget()
        if choice == "Solin":
            self.panelinfosolin.pack(side=TOP,fill=BOTH,expand=True,padx=5,pady=5)
        else:
            self.panelinfosolin.pack_forget()
        if choice == "Bellman-Kalaba":
            self.panelinfokalaba.pack(side=TOP,fill=BOTH,expand=True,padx=5,pady=5)
        else:
            self.panelinfokalaba.pack_forget()
        self.panelmodoupdate()

    def panelmodoupdate(self):
        self.textnumnodos.pack(side=LEFT,fill=BOTH,expand=True,padx=5,pady=5)
        self.entrynumnodos.pack(side=LEFT,fill=BOTH,expand=True,padx=5,pady=5)
        self.textalgoritmo.pack(side=LEFT,fill=BOTH,expand=True,padx=5,pady=5)
        self.selalgoritmo.pack(side=LEFT,fill=BOTH,expand=True,padx=5,pady=5)
        self.panelbotones.pack(side=TOP,fill=BOTH,expand=True,padx=5,pady=5)
        self.buttoncontinue.pack(side=RIGHT,fill=Y,expand=True,padx=5,pady=5)
        self.selmodosolin.pack(side=RIGHT,fill=None,expand=False,padx=5,pady=0)
        self.textmodesolin.pack(side=RIGHT,fill=None,expand=False,padx=5,pady=0)

    def clearPanelModo(self):
        for widget in self.panelmodo.pack_slaves():
            widget.pack_forget()

    def solve(self):
        """
        Comprueba todos los datos antes de continuar y redirige el flujo del programa al algoritmo  de resolución adecuado
        """
        self.buildGraph()
        if self.operationStatus != 2:
            messagebox.showwarning(self.loc['error_solve_noconfig_title'], self.loc['error_solve_noconfig_desc'])
            return
        if not self.checkConnectivity():
            messagebox.showwarning(self.loc['error_solve_connectivity_title'], self.loc['error_solve_connectivity_desc'])
            return
        if self.selalgoritmo.get() == "Dijkstra":
            self.solveDijkstra()
        elif self.selalgoritmo.get() == "Bellman-Kalaba":
            self.solveBellman()
        elif self.selalgoritmo.get() == "Floyd":
            self.solveFloyd()
        elif self.selalgoritmo.get() == "Solin":
            self.solveSolin(self.selmodosolin.get())
        elif self.selalgoritmo.get() == "Transporte":
            self.solveTransporte()

    def checkConnectivity(self):
        """
        Comprueba la conectividad del grafo del problema
        """
        numnodos = int(self.entrynumnodos.get())
        matrix = self.grafo.buildMatrizAdyacencia()
        #Simetrizar la matrix
        matrix = matrix + matrix.T - np.diag(matrix.diagonal())
        #Prop: el grafo es conexo <-> A + A^2 + ... + A^(n-1) tiene todos los coef. != 0
        for i in range(numnodos):
            if i == 0 or i==1: continue
            matrix = matrix + np.linalg.matrix_power(matrix,i)
        for elemento in np.nditer(matrix):
            if elemento == 0:
                return False
        return True

    def lazosCallback(self):
        if self.loops.get() == 1:
            for caja in self.referenciasnodoslazo:
                caja.delete(0,END)
                caja.configure(state="disabled")
        else:
            for caja in self.referenciasnodoslazo:
                caja.configure(state="enabled")

    def switchConfiguration(self,switch):
        self.entrynumnodos.configure(state=switch)

    def reconfigurate(self):
        self.dropMatrix()
        self.buttoncontinue.configure(text=self.loc['labelframe1_button_setupmatrix'], command=self.generateMatrix)
        self.switchMatrixButtons('disabled')
        self.switchConfiguration('enabled')
        #Update info panel
        self.solveroutput.delete('1.0',END)
        self.writeprobleminfo()
        
    def buildGraph(self):
        """
        Encontrar nodos y aristas y construir el grafo del problema
        """
        tamaño = int(self.entrynumnodos.get())
        nodos = set(range(tamaño))
        aristas = set()
        costes = {}
        for i in range(tamaño):
            for j in range(tamaño):
                coste = self.matriz[(i,j)].get()
                if coste == '' or int(coste) == 0:
                    continue
                else:
                    aristas.add((i,j))
                    costes[(i,j)] = int(coste)
        self.grafo = Grafo(nodos,aristas,costes)

    def outputText(self,text):
        self.solveroutput.insert(END,text)

    def getMatrix(self,casilla):
        r = self.matriz[casilla].get()
        if r == 0 or r == '':
            return 0
        else: return int(r)

    def getDemandasProducciones(self,nodo):
        return self.demandasProducciones.get(nodo, (2,0))

    def updateDemandasProducciones(self,nodo:int,value:tuple):
        """
        Actualiza los datos del modelo de transporte para el nodo 'nodo' con los datos 'value'
        """
        self.demandasProducciones[nodo] = value
        #Ajustar titulo de la celda
        for celda in [self.celdasTitulo['r'+str(nodo)], self.celdasTitulo['c'+str(nodo)]]:
            celda.configure(state="enabled")
            #Limpiar celda si no está vacia
            indx = celda.get().find('*')
            if indx != -1:
                celda.delete(indx,END)
            if value[0] == 2:
                celda.configure(state="disabled")
                continue
            #Actualizar datos
            if value[0] == 0:
                celda.configure(state="enabled")
                celda.insert(END,'*P')
            elif value[0] == 1:
                celda.configure(state="enabled")
                celda.insert(END,'*D')
            celda.configure(state="disabled")

                                    ################################
                                    ### ALGORITMOS DE RESOLUCIÓN ###
                                    ################################

    def solveDijkstra(self):
        self.solveroutput.delete('1.0',END)
        self.solveroutput.insert(END, self.loc['dijkstra_pipeline_title'])
        self.solveroutput.insert(END, "k=0 \n")
        nodoOrigen = int(self.firstnodedijkstra.get())
        nodoDestino = int(self.lastnodedijkstra.get())
        M = [nodoOrigen]
        V0 = {}
        V1 = {}
        k = 0
        for nodo in self.grafo.getNodos():
            if nodo == nodoOrigen: 
                self.solveroutput.insert(END, "V0({})=0 \n".format(nodo))
                V0[nodo] = 0
            else: 
                self.solveroutput.insert(END, "V0({})=inf \n".format(nodo))
                V0[nodo] = inf
        self.solveroutput.insert(END, self.loc['dijkstra_pipeline_1'].format(nodoOrigen,nodoOrigen))
        while True:
            k = k + 1
            V1 = {}
            self.solveroutput.insert(END, "\nk={} \n".format(k))
            for nodo in self.grafo.getNodos() - set(M):
                V1[nodo] = min(V0[nodo],V0[M[-1]]+self.grafo.distancia(M[-1],nodo))
                self.solveroutput.insert(END, "V{}({})={} \n".format(k,nodo,V1[nodo]))
            valorOptimo = min(V1.values())
            for key in V1.keys():
                if valorOptimo == V1[key]:
                    nodoOptimo = key
            M.append(nodoOptimo)
            self.solveroutput.insert(END, self.loc['dijkstra_pipeline_2'].format(nodoOptimo,str(M)))
            V0 = V1.copy()
            if M[-1] == nodoDestino: break
        self.solveroutput.insert(END, self.loc['dijkstra_pipeline_3'].format(V0[nodoDestino]))
    
    def solveBellman(self):
        self.solveroutput.delete('1.0',END)
        self.solveroutput.insert(END, self.loc['bellman_pipeline_title'])
        self.solveroutput.insert(END, "k=0 \n")
        nodoFinal = int(self.lastnodebellman.get())
        V0={}
        k = 0
        for nodo in self.grafo.getNodos():
            if nodo == nodoFinal:
                self.solveroutput.insert(END, "V0({})=0 \n".format(nodo))
                V0[nodo] = 0
            else:
                self.solveroutput.insert(END, "V0({})=inf\n".format(nodo))
                V0[nodo] = inf
        while True:
            k = k + 1
            V1 = {}
            self.solveroutput.insert(END, "\nk={} \n".format(k))
            for nodo in self.grafo.getNodos():
                valores = {self.grafo.distancia(nodo,y)+V0[y] for y in self.grafo.getNodos() - set([nodo])}
                V1[nodo] = min([min(valores),V0[nodo]])
                self.solveroutput.insert(END, "V{}({})={} \n".format(k,nodo,V1[nodo]))
            if V1 == V0: break
            V0 = V1.copy()
        self.solveroutput.insert(END, self.loc['bellman_pipeline_1'])

    def solveFloyd(self):
        self.solveroutput.delete('1.0',END)
        self.solveroutput.insert(END, self.loc['floyd_pipeline_title'])
        self.solveroutput.insert(END, "k=1 \n")
        numNodos = int(self.entrynumnodos.get())
        matrizCostes = {}
        for key in self.matriz.keys():
            if self.matriz[key].get() == '' or self.matriz[key].get() == '0': matrizCostes[key] = inf
            else: matrizCostes[key] = int(self.matriz[key].get())
        penultimosNodos = {(i,j):i for i in range(numNodos) for j in range(numNodos)}
        self.outputText(self.loc['floyd_pipeline_1'])
        for i in range(numNodos):
            self.outputText("{}\n".format(str([matrizCostes[(i,j)] for j in range(numNodos)])))
        self.outputText(self.loc['floyd_pipeline_2'])
        for i in range(numNodos):
            self.outputText("{}\n".format(str([penultimosNodos[(i,j)] for j in range(numNodos)])))
        k = 0
        while k<=numNodos-1:
            if k != numNodos-1:
                self.outputText("\nk={} \n".format(k+2))
            else:
                self.outputText(self.loc['floyd_pipeline_3'])
            for i in range(numNodos):
                for j in range(numNodos):
                    if i==k or j==k: continue
                    if matrizCostes[(i,k)]+matrizCostes[(k,j)] < matrizCostes[(i,j)]:
                        penultimosNodos[(i,j)] = penultimosNodos[(k,j)]
                        matrizCostes[(i,j)] = matrizCostes[(i,k)] + matrizCostes[(k,j)]
            self.outputText(self.loc['floyd_pipeline_1'])
            for i in range(numNodos):
                self.outputText("{}\n".format(str([matrizCostes[(i,j)] for j in range(numNodos)])))
            self.outputText(self.loc['floyd_pipeline_2'])
            for i in range(numNodos):
                self.outputText("{}\n".format(str([penultimosNodos[(i,j)] for j in range(numNodos)])))
            k = k + 1
        self.outputText(self.loc['floyd_pipeline_4'])
            
    def solveSolin(self,mode):
        self.solveroutput.delete('1.0',END)
        self.solveroutput.insert(END, self.loc['solin_pipeline_title'])
        numNodos = int(self.entrynumnodos.get())
        matrizCostes = {}

        def searchForKey(value, excluded=[],searchRows=range(numNodos)):
            for key in matrizCostes.keys() - set(excluded):
                if key[0] not in searchRows: continue
                if matrizCostes[key] == value:
                    return key

        def getMinFromMatrix(matriz):
            minimosPorFila = set()
            for i in range(numNodos):
                minimosPorFila.add(min({matriz[(i,j)] for j in range(numNodos)}))
            minimo = min(minimosPorFila)
            return searchForKey(minimo)

        keys = []

        if mode == 'Maximizar':
            for key in self.matriz.keys():
                if self.matriz[key].get() == '' or self.matriz[key].get() == '0': matrizCostes[key] = 0
                else: matrizCostes[key] = -int(self.matriz[key].get())
        else:
            for key in self.matriz.keys():
                if self.matriz[key].get() == '' or self.matriz[key].get() == '0': matrizCostes[key] = inf
                else: matrizCostes[key] = int(self.matriz[key].get())

        firstKey = getMinFromMatrix(matrizCostes)
        keys.append(firstKey)
        searchTarget = []
        searchTarget.append([matrizCostes[(firstKey[1],j)] for j in range(numNodos) if j != firstKey[1]])
        searchRows = {firstKey[1]}
        while True:
            flattenSearchTarget = [num for sublist in searchTarget for num in sublist]
            target = min(flattenSearchTarget)
            newKey = searchForKey(target,keys,searchRows)
            keys.append(newKey)
            if len(keys) == numNodos: break
            columnasExcluidas = [key[1] for key in keys]
            searchRows = searchRows.union({newKey[1]})
            searchTarget = []
            for key in keys:
                searchTarget.append([matrizCostes[(key[1],j)] for j in range(numNodos) if j not in columnasExcluidas])
        self.outputText(self.loc['solin_pipeline_1'])
        
        for key in matrizCostes:
            if key not in keys: matrizCostes[key] = '-'  

        if mode == 'Maximizar':
            for key in matrizCostes:
                if matrizCostes[key] != '-':
                    matrizCostes[key] = -matrizCostes[key]

        for i in range(numNodos):
            self.outputText("{}\n".format(str([matrizCostes[(i,j)] for j in range(numNodos)])))

    def solveTransporte(self):
        #Motor de programación lineal - PuLP
        #Recuperamos toda la información según el modelo de transporte
        nodosProductores = []
        nodosIntermedios = []
        nodosConsumidores = []
        numNodos = int(self.entrynumnodos.get())
        #Clasificamos todos los nodos
        for nodo in range(numNodos):
            nodoinfo = self.getDemandasProducciones(nodo)
            if nodoinfo[0] == 0:
                nodosProductores.append((nodo,nodoinfo[1]))
                continue
            elif nodoinfo[0] == 1:
                nodosConsumidores.append((nodo,nodoinfo[1]))
                continue
            else:
                nodosIntermedios.append(nodo)
        problema = pulp.LpProblem("Transporte",pulp.LpMinimize)
        variables = {}
        #Modo con nodos intermedios
        if len(nodosIntermedios) > 0:
            #Asignación de variables
            for nodo in nodosProductores:
                for nodoi in nodosIntermedios:
                    var = pulp.LpVariable("x{}{}".format(nodo[0],nodoi),upBound=nodo[1],lowBound=0)
                    variables[nodo[0],nodoi] = var
            for nodoi in nodosIntermedios:
                for nodo in nodosConsumidores:
                    var = pulp.LpVariable("x{}{}".format(nodoi,nodo[0]),upBound=nodo[1],lowBound=0)
                    variables[nodoi,nodo[0]] = var
            #Configuración de ecuaciones de equilibrio
            for nodo in nodosIntermedios:
                entradas = [variables[i,nodo] for i in [nod[0] for nod in nodosProductores]]
                salidas = [variables[nodo,i] for i in [nod[0] for nod in nodosConsumidores]]
                problema += pulp.lpSum(entradas) == pulp.lpSum(salidas)
            #Configuración de ecuaciones de productores
            for nodo in nodosProductores:
                nodovars = [variables[nodo[0],i] for i in nodosIntermedios]
                problema += pulp.lpSum(nodovars) <= nodo[1]
            #Configuración de ecuaciones de consumidores
            for nodo in nodosConsumidores:
                nodovars = [variables[i,nodo[0]] for i in nodosIntermedios]
                problema += pulp.lpSum(nodovars) >= nodo[1]
        else:
            #Optimización mediante expresión directa: (REVISAR)
            #variables = {(nod1[0],nod2[0]) : pulp.LpVariable("x{}{}".format(nod1[0],nod2[0]),upBound=nod1[0],lowBound=0) for nod1 in nodosConsumidores for nod2 in nodosProductores}
            for nod1 in nodosProductores:
                for nod2 in nodosConsumidores:
                    var = pulp.LpVariable("x{}{}".format(nod1[0],nod2[0]),upBound=nod1[1],lowBound=0)
                    variables[nod1[0],nod2[0]] = var
            #Configuración de ecuaciones de productores
            for nodo in nodosProductores:
                nodovars = [variables[nodo[0],i] for i in [nod[0] for nod in nodosConsumidores]]
                problema += pulp.lpSum(nodovars) <= nodo[1]
            #Configuración de ecuaciones de consumidores
            for nodo in nodosConsumidores:
                nodovars = [variables[i,nodo[0]] for i in [nod[0] for nod in nodosProductores]]
                problema += pulp.lpSum(nodovars) >= nodo[1]
        #Ecuacion general
        conf = [(variables[i,j],self.getMatrix((i,j))) for i in range(numNodos) for j in range(numNodos) if variables.get((i,j),0) != 0]
        exp = pulp.LpAffineExpression(conf)
        problema += exp
        #Resultado del problema
        self.solveroutput.insert(END, self.loc['transportation_pipeline_title'] + 35*'-' + '\n')
        self.solveroutput.insert(END, repr(problema) + "\n")
        problema.solve()
        self.solveroutput.insert(END, self.loc['transportation_pipeline_1'].format(pulp.LpStatus[problema.status]))
        self.solveroutput.insert(END, self.loc['transportation_pipeline_2'].format(pulp.value(problema.objective)))
        self.solveroutput.insert(END, self.loc['transportation_pipeline_3'])
        for v in problema.variables():
            self.solveroutput.insert(END, str(v.name) + '=' + str(v.varValue) + '\n')

class ElementViewTransporte():
    def __init__(self,master,nodo,masterSelf,loc):
        self.loc = loc
        self.principal = master
        self.root = Toplevel(master)
        self.root.grab_set()
        self.root.title(self.loc['gui2_title'].format(nodo))
        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('250x120+%d+%d' % (x-50, y-50))
        self.root.resizable(0,0)

        self.nodo = nodo
        self.masterSelf = masterSelf

        self.panelorigen = ttk.Frame(self.root)
        self.paneldestino = ttk.Frame(self.root)
        self.botonera = ttk.Frame(self.root)

        self.origendestinoVar = IntVar(self.root)
        self.origenCheck = ttk.Radiobutton(self.panelorigen, text=self.loc['gui2_radio1'], variable=self.origendestinoVar, command=self.origenCallback, value=1)
        self.producionLabel = ttk.Label(self.panelorigen, text=self.loc['gui2_label1'])
        self.producionEntry = ttk.Entry(self.panelorigen, width=7)
        self.destinationCheck = ttk.Radiobutton(self.paneldestino, text=self.loc['gui2_radio2'], variable=self.origendestinoVar, command=self.destinationCallback, value=2)
        self.demandaLabel = ttk.Label(self.paneldestino, text=self.loc['gui2_label2'])
        self.demandaEntry = ttk.Entry(self.paneldestino, width=7)
        self.exitButton = ttk.Button(self.botonera, text=self.loc['gui2_save_button'], command=self.save)
        self.none = ttk.Radiobutton(self.botonera, text=self.loc['gui2_radio3'], variable=self.origendestinoVar, value=3, command=self.mediumNodeCallback)

        datosNodo = self.masterSelf.getDemandasProducciones(self.nodo)
        if datosNodo[0] == 0:
            self.demandaEntry.configure(state="disabled")
            self.origendestinoVar.set(1)
            self.producionEntry.insert(0, datosNodo[1])
        elif datosNodo[0] == 1:
            self.producionEntry.configure(state="disabled")
            self.origendestinoVar.set(2)
            self.demandaEntry.insert(0, datosNodo[1])
        elif datosNodo[0] == 2:
            self.producionEntry.configure(state="disabled")
            self.demandaEntry.configure(state="disabled")
            self.origendestinoVar.set(3)

        self.panelorigen.pack(side=TOP,fill=X,expand=True,padx=5,pady=5)
        self.paneldestino.pack(side=TOP,fill=X,expand=True,padx=5,pady=5)
        self.botonera.pack(side=TOP,fill=X,expand=True,padx=5,pady=5)

        self.origenCheck.pack(side=LEFT,fill=X,expand=True,padx=5,pady=0)
        self.producionLabel.pack(side=LEFT,fill=X,expand=True,padx=5,pady=0)
        self.producionEntry.pack(side=LEFT,fill=X,expand=True,padx=5,pady=0)
        self.destinationCheck.pack(side=LEFT,fill=X,expand=True,padx=5,pady=0)
        self.demandaLabel.pack(side=LEFT,fill=X,expand=True,padx=5,pady=0)
        self.demandaEntry.pack(side=LEFT,fill=X,expand=True,padx=5,pady=0)
        self.exitButton.pack(side=RIGHT,fill=NONE,expand=False,padx=5,pady=5)
        self.none.pack(side=LEFT,fill=NONE,expand=False,padx=5,pady=5)

    def origenCallback(self):
        self.demandaEntry.delete(0,END)
        self.demandaEntry.configure(state="disabled")
        self.producionEntry.configure(state="enabled")

    def destinationCallback(self):
        self.producionEntry.delete(0,END)
        self.producionEntry.configure(state="disabled")
        self.demandaEntry.configure(state="enabled")

    def mediumNodeCallback(self):
        self.demandaEntry.delete(0,END)
        self.producionEntry.delete(0,END)
        self.demandaEntry.configure(state="disabled")
        self.producionEntry.configure(state="disabled")

    def save(self):
        if self.origendestinoVar.get() == 1:
            valor = int(self.producionEntry.get())
            self.masterSelf.updateDemandasProducciones(self.nodo,(0,valor))
        elif self.origendestinoVar.get() == 2:
            valor = int(self.demandaEntry.get())
            self.masterSelf.updateDemandasProducciones(self.nodo,(1,valor))
        elif self.origendestinoVar.get() == 3:
            self.masterSelf.updateDemandasProducciones(self.nodo,(2,0))
        self.root.destroy()


Aplicacion()
