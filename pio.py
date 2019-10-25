from tkinter import *
from tkinter import ttk,font
from math import inf

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
        return self.costes.get((nodo1,nodo2),inf)

class Aplicacion():
    def __init__(self):
        self.principal = Tk()
        self.principal.title("Teoría de grafos - Caminos/Árboles")
        self.principal.geometry("900x800")

        self.botoneraDibujada = False

        self.matriz = {}
        self.referenciasnodoslazo = []
        self.celdasTitulo = {}
        self.grafo = 0

        #Panel de información y subpaneles
        self.panelmodo = ttk.LabelFrame(self.principal, text="Configuración del problema")
        self.panelinfo = ttk.Frame(self.panelmodo)
        self.panelinfosolin = ttk.Frame(self.panelmodo)
        self.panelbotones = ttk.Frame(self.panelmodo)
        self.textnumnodos = ttk.Label(self.panelinfo, text="Número de nodos:")
        self.entrynumnodos = ttk.Entry(self.panelinfo, width=7)
        self.textalgoritmo = ttk.Label(self.panelinfo, text="Algoritmo de operación:")
        self.textmodesolin = ttk.Label(self.panelinfosolin,text="Modo de operación:")
        self.selalgoritmo = ttk.Combobox(self.panelinfo, state="readonly")
        self.selalgoritmo["values"] = ["Dijkstra","Bellman-Kalaba","Floyd","Solin","Transporte","Asignación"]
        self.selalgoritmo.bind("<<ComboboxSelected>>",self.algorithmSelected)
        self.selmodosolin = ttk.Combobox(self.panelinfosolin, state="readonly")
        self.selmodosolin["values"] = ["Maximizar","Minimizar"]
        self.buttoncontinue = ttk.Button(self.panelbotones, text="Preparar matriz", command=self.generateMatrix)

        self.panelinfodijkstra = ttk.Frame(self.panelmodo)
        self.textfirstnodedijkstra = ttk.Label(self.panelinfodijkstra,text="Nodo de origen:")
        self.textlastnodedijkstra = ttk.Label(self.panelinfodijkstra, text="Nodo de destino:")
        self.firstnodedijkstra = ttk.Entry(self.panelinfodijkstra,width=5)
        self.lastnodedijkstra = ttk.Entry(self.panelinfodijkstra,width=5)

        self.panelintermedio = ttk.Frame(self.principal)

        #Panel de matriz y subpaneles
        self.panelmatriz = ttk.LabelFrame(self.panelintermedio, text="Matriz de costes del grafo")
        self.panelmatrizmain = ttk.Frame(self.panelmatriz)
        self.panelmatrizbotonera = ttk.Frame(self.panelmatriz)

        self.selalgoritmomatriz = ttk.Label(self.panelmatrizbotonera, font=font.Font(size=10))
        self.buttonresolver = ttk.Button(self.panelmatrizbotonera,text="Resolver",command=self.solve)
        self.buttonsim = ttk.Button(self.panelmatrizbotonera,text="Simetrizar")
        self.loops = IntVar(self.principal)
        self.noloopscheck = ttk.Checkbutton(self.panelmatrizbotonera, text="Sin lazos", variable=self.loops, command=self.lazosCallback)
        self.reconfiguratebutton = ttk.Button(self.panelmatrizbotonera, text="Reconfigurar matriz", command=self.reconfigurate)

        #Panel de resolución y subpaneles
        self.panelresolucion = ttk.LabelFrame(self.panelintermedio, text="Resolución del problema")
        self.solveroutput = Text(self.panelresolucion, width=71)
        self.outputscroll = ttk.Scrollbar(self.panelresolucion, command=self.solveroutput.yview)
        self.solveroutput.configure(yscrollcommand=self.outputscroll.set)
        self.solveroutput.insert(END,'Esperando datos del problema...')

        #==GEOMETRIA==
        #Geometría de paneles
        self.panelmodo.pack(side=TOP,fill=NONE,expand=False,padx=5,pady=(20,5))
        self.panelintermedio.pack(side=TOP,fill=NONE,expand=False,padx=5,pady=(20,5))
        self.panelmatriz.pack(side=LEFT,fill=X,expand=True,padx=(0,20),pady=0)
        self.panelmatrizmain.pack(side=TOP,fill=X,expand=True,padx=0,pady=0)
        self.panelmatrizbotonera.pack(side=TOP,fill=X,expand=True,padx=0,pady=5)
        self.panelresolucion.pack(side=RIGHT,fill=Y,expand=False,padx=0,pady=0)

        #Geometría panel de modo
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

        #Geometría panel de resolución
        self.solveroutput.pack(side=LEFT,fill=BOTH,expand=True,padx=(5,0),pady=5)
        self.outputscroll.pack(side=RIGHT,fill=Y,expand=True)

        self.principal.mainloop()

    def generateMatrix(self):
        self.dropMatrix()
        self.switchMatrixButtons('enabled')
        self.buttoncontinue.configure(text="Actualizar datos", command=self.updateMatrix)
        self.selalgoritmomatriz.configure(text="Algoritmo elegido: " + self.selalgoritmo.get())
        self.loops.set(0)
        self.solveroutput.delete('1.0',END)
        self.solveroutput.insert(END,'Esperando orden para ejecutar resolución...')
        self.switchConfiguration('disabled')
        numNodos = int(self.entrynumnodos.get())
        #Titulos
        for i in range(numNodos):
            caja = ttk.Entry(self.panelmatrizmain,width=5)
            if self.selalgoritmo.get() == "Dijkstra":
                if i == int(self.firstnodedijkstra.get()):
                    caja.insert(0,str(i)+'*O')
                elif i == int(self.lastnodedijkstra.get()):
                    caja.insert(0,str(i)+'*D')
                else:
                    caja.insert(0,str(i))
            else:
                caja.insert(0,str(i))
            caja.configure(state="disabled")
            self.celdasTitulo['c'+str(i)] = caja
            caja.grid(column=i+1,row=0,padx=3,pady=3,sticky=(N,S,E,W))
        for i in range(numNodos):
            caja = ttk.Entry(self.panelmatrizmain,width=5)
            if self.selalgoritmo.get() == "Dijkstra":
                if i == int(self.firstnodedijkstra.get()):
                    caja.insert(0,str(i)+'*O')
                elif i == int(self.lastnodedijkstra.get()):
                    caja.insert(0,str(i)+'*D')
                else:
                    caja.insert(0,str(i))
            else:
                caja.insert(0,str(i))
            caja.configure(state="disabled")
            self.celdasTitulo['r'+str(i)] = caja
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

    def updateMatrix(self):
        if self.selalgoritmo.get() == "Dijkstra":
            fn = self.firstnodedijkstra.get()
            ln = self.lastnodedijkstra.get()
            #Limpiar celdas
            self.dijkstraClearTitles()
            #Asignar datos
            for celda in [self.celdasTitulo['c'+fn],self.celdasTitulo['r'+fn]]:
                celda.configure(state="enabled")
                celda.insert(END,'*O')
                celda.configure(state="disabled")
            for celda in [self.celdasTitulo['c'+ln],self.celdasTitulo['r'+ln]]:
                celda.configure(state="enabled")
                celda.insert(END,'*D')
                celda.configure(state="disabled")
        self.switchMatrixButtons('enabled')
    
    def dijkstraClearTitles(self):
        for celda in self.celdasTitulo.values():
            celda.configure(state="enabled")
            index = celda.get().find('*')
            if index != -1: celda.delete(index,END)
            celda.configure(state="disabled")

    def dropMatrix(self):
        for widget in self.panelmatrizmain.grid_slaves():
            widget.grid_forget()
        self.matriz = {}
        self.celdasTitulo = {}

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
            self.selalgoritmomatriz.pack(side=RIGHT,fill=Y,expand=True,padx=5,pady=5)
            self.botoneraDibujada = True

    def algorithmSelected(self,event):
        self.modosubpanelupdate()
        self.selalgoritmomatriz.configure(text="Algoritmo elegido: " + self.selalgoritmo.get())
        if self.selalgoritmo.get() != 'Dijkstra': self.dijkstraClearTitles()

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
        self.buildGraph()
        if self.selalgoritmo.get() == "Dijkstra":
            self.solveDijkstra()

    def lazosCallback(self):
        if self.loops.get() == 1:
            for caja in self.referenciasnodoslazo:
                caja.configure(state="disabled")
        else:
            for caja in self.referenciasnodoslazo:
                caja.configure(state="enabled")

    def switchConfiguration(self,switch):
        self.entrynumnodos.configure(state=switch)

    def reconfigurate(self):
        self.dropMatrix()
        self.buttoncontinue.configure(text="Preparar matriz", command=self.generateMatrix)
        self.switchMatrixButtons('disabled')
        self.switchConfiguration('enabled')

    def buildGraph(self):
        #Encontrar nodos y aristas
        tamaño = int(self.entrynumnodos.get())
        nodos = set()
        aristas = set()
        costes = {}
        for i in range(tamaño):
            for j in range(tamaño):
                coste = self.matriz[(i,j)].get()
                if coste == '' or int(coste) == 0:
                    continue
                else:
                    nodos.add(i)
                    nodos.add(j)
                    aristas.add((i,j))
                    costes[(i,j)] = int(coste)
        self.grafo = Grafo(nodos,aristas,costes)

    def solveDijkstra(self):
        self.solveroutput.delete('1.0',END)
        self.solveroutput.insert(END, "Resolución del problema mediante el algoritmo de Dijkstra: \n \n")
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
        self.solveroutput.insert(END, "Nodo óptimo: {} \nM=[{}] \n".format(nodoOrigen,nodoOrigen))
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
            self.solveroutput.insert(END, "Nodo óptimo: {} \nM={} \n".format(nodoOptimo,str(M)))
            V0 = V1.copy()
            if M[-1] == nodoDestino: break
        self.solveroutput.insert(END, "\nEl algoritmo ha finalizado. La distancia mínima del nodo origen al nodo destino es {}. \n".format(V0[nodoDestino]))
    
Aplicacion()