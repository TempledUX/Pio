from tkinter import *
from tkinter import ttk,font,messagebox
from math import inf
import numpy as np
import pulp

# Pio - TempledUX
# Last edit: 25/01/2020
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


class Aplicacion():
    def __init__(self):
        self.principal = Tk()
        self.principal.title("Pio - Teoría de grafos")
        self.principal.geometry("900x800")

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

        #Subpanel Dijkstra
        self.panelinfodijkstra = ttk.Frame(self.panelmodo)
        self.textfirstnodedijkstra = ttk.Label(self.panelinfodijkstra,text="Nodo de origen:")
        self.textlastnodedijkstra = ttk.Label(self.panelinfodijkstra, text="Nodo de destino:")
        self.firstnodedijkstra = ttk.Entry(self.panelinfodijkstra,width=5)
        self.lastnodedijkstra = ttk.Entry(self.panelinfodijkstra,width=5)

        #Subpanel Bellman-Kalaba
        self.panelinfokalaba = ttk.Frame(self.panelmodo)
        self.textlastnodebellman = ttk.Label(self.panelinfokalaba, text="Nodo final:")
        self.lastnodebellman = ttk.Entry(self.panelinfokalaba,width=5)

        self.panelintermedio = ttk.Frame(self.principal)

        #Panel de matriz y subpaneles
        self.panelmatriz = ttk.LabelFrame(self.panelintermedio, text="Matriz de costes del grafo")
        self.panelmatrizmain = ttk.Frame(self.panelmatriz)
        self.panelmatrizbotonera = ttk.Frame(self.panelmatriz)

        #self.selalgoritmomatriz = ttk.Label(self.panelmatrizbotonera, font=font.Font(size=10))
        self.buttonresolver = ttk.Button(self.panelmatrizbotonera,text="Resolver",command=self.solve)
        self.buttonsim = ttk.Button(self.panelmatrizbotonera,text="Simetrizar",command=self.simetrizeMatrix)
        self.loops = IntVar(self.principal)
        self.noloopscheck = ttk.Checkbutton(self.panelmatrizbotonera, text="Sin lazos", variable=self.loops, command=self.lazosCallback)
        self.reconfiguratebutton = ttk.Button(self.panelmatrizbotonera, text="Reconfigurar matriz", command=self.reconfigurate)

        #Panel de resolución y subpaneles
        self.panelresolucion = ttk.LabelFrame(self.panelintermedio, text="Resolución del problema e información de estado")
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
            messagebox.showerror("Entrada vacía o inválida", "Especifica un número de nodos correcto antes de continuar.")
            return False
        algoritmo = self.selalgoritmo.get()
        if numNodos > 25:
            messagebox.showerror("Valor fuera de rango", "El número de nodos es demasiado grande. El máximo de nodos disponible es 25")
            return False
        #Algoritmo elegido
        if algoritmo == '':
            messagebox.showerror("Entrada vacía o invalida","Especifica un algoritmo de resolución antes de continuar.")
            return False
        if algoritmo == "Dijkstra":
            #Sintaxis
            try:
                fn = int(self.firstnodedijkstra.get())
                ln = int(self.lastnodedijkstra.get())
            except ValueError:
                messagebox.showerror("Entrada vacía o inválida","Configura adecuadamente el nodo inicial y final para el algoritmo de Dijkstra y después actualiza los datos.")
                return False
            #Rango
            fn = int(self.firstnodedijkstra.get())
            ln = int(self.lastnodedijkstra.get())
            limite = numNodos
            if fn < 0 or fn > limite-1:
                messagebox.showerror("Valor fuera de rango", "El valor introducido para el nodo inicial no se corresponde con ningún nodo existente. Observación: los nodos se numeran empezando desde el 0.")
                return False
            if ln < 0 or ln > limite-1:
                messagebox.showerror("Valor fuera de rango", "El valor introducido para el nodo final no se corresponde con ningún nodo existente. Observación: los nodos se numeran empezando desde el 0.")
                return False
        if algoritmo == "Bellman-Kalaba":
            #Sintaxis
            try:
                fn = int(self.lastnodebellman.get())
            except ValueError:
                messagebox.showerror("Entrada vacía o invalida","Configura adecuadamente el nodo final para el algoritmo de Bellman-Kalaba antes de continuar.")
                return False
            #Rango
            if fn < 0 or fn > numNodos-1:
                messagebox.showerror("Valor fuera de rango","El valor introducido para el nodo final no se corresponde con ningún nodo existente.")
                return False
        if algoritmo == "Solin":
            if self.selmodosolin.get() == '':
                messagebox.showerror("Entrada vacía o inválida","Configura adecuadamente el modo de operación del algoritmo de Solin antes de continuar.")
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
        self.buttoncontinue.configure(text="Actualizar datos", command=self.updateMatrix)
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
                caja.bind("<Button-1>", lambda event, node=i, yo=self : ElementViewTransporte(self.principal, node,yo))
            caja.grid(column=i+1,row=0,padx=3,pady=3,sticky=(N,S,E,W))
        for i in range(numNodos):
            caja = ttk.Entry(self.panelmatrizmain,width=5)
            self.ajustarTitulo(caja,i)
            caja.configure(state="disabled")
            self.celdasTitulo['r'+str(i)] = caja
            if self.selalgoritmo.get() == 'Transporte':
                caja.bind("<Button-1>", lambda event, node=i, yo=self : ElementViewTransporte(self.principal, node,yo))
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
        self.solveroutput.insert(END, "Esperando orden para ejecutar resolución...\n")
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
                celda.bind("<Button-1>", lambda event, node=int(celda.get()), yo=self : ElementViewTransporte(self.principal, node,yo))
        self.switchMatrixButtons('enabled')
        self.solveroutput.insert(END, "Esperando orden para ejecutar resolución...\n")
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
        if self.selalgoritmo.get() == 'Dijkstra':
            self.solveroutput.insert(END, "Algoritmo elegido: Dijkstra\nPermite encontrar el camino mínimo desde el nodo de origen hasta el nodo de destino.\n\n")
        elif self.selalgoritmo.get() == 'Bellman-Kalaba':
            self.solveroutput.insert(END, "Algoritmo elegido: Bellman-Kalaba\nPermite encontrar todos los caminos mínimos del grafo hasta un nodo final.\n\n")
        elif self.selalgoritmo.get() == 'Floyd':
            self.solveroutput.insert(END, "Algoritmo elegido: Floyd\nPermite calcular los caminos mínimos entre dos pares cualesquiera de nodos.\n\n")
        elif self.selalgoritmo.get() == 'Solin':
            self.solveroutput.insert(END, "Algoritmo elegido: Solin\nPermite calcular el árbol recubridor mínimo o máximo de un grafo.\n")
            self.solveroutput.insert(END, "\nObservación: dado que trabajamos con un árbol, asigna los valores a la mitad de la matriz y simetrizala.\n\n")
        elif self.selalgoritmo.get() == 'Transporte':
            self.solveroutput.insert(END, "Algoritmo elegido: Transporte\nPermite resolver un problema formulado mediante el modelo de transporte (nodos de producción, intermedios y de destino).")
            self.solveroutput.insert(END, "\nElige la cabecera de cada nodo para determinar como se comportará bajo el modelo de transporte y para ajustar sus valores de producción/demanda.\n")
        self.solveroutput.insert(END, "Actualiza la información del problema antes de continuar...\n")
        self.operationStatus = 1

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
            messagebox.showwarning("Configuración sin finalizar", "Configura los datos del problema (si es necesario) y pulsa 'Actualizar datos' antes de continuar.")
            return
        if not self.checkConnectivity():
            messagebox.showwarning("Conectividad del grafo", "El grafo introducido no parece ser conexo. Puedes utilizar un algoritmo sobre cada componente conexa o revisar la matriz de costes.")
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
        self.buttoncontinue.configure(text="Preparar matriz", command=self.generateMatrix)
        self.switchMatrixButtons('disabled')
        self.switchConfiguration('enabled')

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
    
    def solveBellman(self):
        self.solveroutput.delete('1.0',END)
        self.solveroutput.insert(END, "Resolución del problema mediante el algoritmo de Bellman-Kalaba: \n \n")
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
        self.solveroutput.insert(END, "\nEl algoritmo ha finalizado. Las distancias mínimas de cada uno de los nodos al nodo final son los valores de V de la última iteracción. \n")

    def solveFloyd(self):
        self.solveroutput.delete('1.0',END)
        self.solveroutput.insert(END, "Resolución del problema mediante el algoritmo de Floyd: \n \n")
        self.solveroutput.insert(END, "k=1 \n")
        numNodos = int(self.entrynumnodos.get())
        matrizCostes = {}
        for key in self.matriz.keys():
            if self.matriz[key].get() == '' or self.matriz[key].get() == '0': matrizCostes[key] = inf
            else: matrizCostes[key] = int(self.matriz[key].get())
        penultimosNodos = {(i,j):i for i in range(numNodos) for j in range(numNodos)}
        self.outputText("Matriz costes: \n")
        for i in range(numNodos):
            self.outputText("{}\n".format(str([matrizCostes[(i,j)] for j in range(numNodos)])))
        self.outputText("Matriz penúltimos nodos: \n")
        for i in range(numNodos):
            self.outputText("{}\n".format(str([penultimosNodos[(i,j)] for j in range(numNodos)])))
        k = 0
        while k<=numNodos-1:
            if k != numNodos-1:
                self.outputText("\nk={} \n".format(k+2))
            else:
                self.outputText("\nFinal:\n")
            for i in range(numNodos):
                for j in range(numNodos):
                    if i==k or j==k: continue
                    if matrizCostes[(i,k)]+matrizCostes[(k,j)] < matrizCostes[(i,j)]:
                        penultimosNodos[(i,j)] = penultimosNodos[(k,j)]
                        matrizCostes[(i,j)] = matrizCostes[(i,k)] + matrizCostes[(k,j)]
            self.outputText("Matriz costes: \n")
            for i in range(numNodos):
                self.outputText("{}\n".format(str([matrizCostes[(i,j)] for j in range(numNodos)])))
            self.outputText("Matriz penúltimos nodos: \n")
            for i in range(numNodos):
                self.outputText("{}\n".format(str([penultimosNodos[(i,j)] for j in range(numNodos)])))
            k = k + 1
        self.outputText("\nEl algoritmo ha finalizado. La matriz de costes del final contiene los caminos mínimos para ir de un nodo a otro y la matriz de penúltimos nodos del final contiene los penúltimos nodos de los caminos mínimos que unen dos nodos. \n")
            
    def solveSolin(self,mode):
        self.solveroutput.delete('1.0',END)
        self.solveroutput.insert(END, "Resolución del problema mediante el algoritmo de Solin: \n \n")
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
        self.outputText("\nEl algoritmo ha finalizado. La matriz que se presenta a continuación es la que queda tras aplicar el algoritmo de Solin: \n")
        
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
        self.solveroutput.insert(END, "\nInformación del problema\n" + 35*'-' + '\n')
        self.solveroutput.insert(END, repr(problema) + "\n")
        problema.solve()
        self.solveroutput.insert(END, "Estado del problema: {}".format(pulp.LpStatus[problema.status]))
        self.solveroutput.insert(END, "\nValor de la función objetivo: {}".format(pulp.value(problema.objective)))
        self.solveroutput.insert(END, "\nVariables:\n")
        for v in problema.variables():
            self.solveroutput.insert(END, str(v.name) + '=' + str(v.varValue) + '\n')

class ElementViewTransporte():
    def __init__(self,master,nodo,masterSelf):
        self.principal = master
        self.root = Toplevel(master)
        self.root.grab_set()
        self.root.title("Ajustar nodo {}".format(nodo))
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
        self.origenCheck = ttk.Radiobutton(self.panelorigen, text="Origen", variable=self.origendestinoVar, command=self.origenCallback, value=1)
        self.producionLabel = ttk.Label(self.panelorigen, text="Producción:")
        self.producionEntry = ttk.Entry(self.panelorigen, width=7)
        self.destinationCheck = ttk.Radiobutton(self.paneldestino, text="Destino", variable=self.origendestinoVar, command=self.destinationCallback, value=2)
        self.demandaLabel = ttk.Label(self.paneldestino, text="Demanda:")
        self.demandaEntry = ttk.Entry(self.paneldestino, width=7)
        self.exitButton = ttk.Button(self.botonera, text="Guardar", command=self.save)
        self.none = ttk.Radiobutton(self.botonera, text="Nodo intermedio", variable=self.origendestinoVar, value=3, command=self.mediumNodeCallback)

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