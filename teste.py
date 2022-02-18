import time
import random
import math
from copy import deepcopy
import heapq

#CLASSE DE APOIO
class adjacencyMatrix:
    def __init__(self, vertices, w = False):
        if w == False:
            self.vertices = vertices
            self.graph = [[0]*self.vertices for i in range(self.vertices)]
        else:
            self.vertices = vertices
            self.graph = [[math.inf ]*self.vertices for i in range(self.vertices)]

    def add_edge(self, u, v):
        self.graph[u - 1][v - 1] = 1
        self.graph[v - 1][u - 1] = 1

    def add_w_edge(self, u, v, peso):
        self.graph[u-1][v-1] = peso
        self.graph[v-1][u-1] = peso

    def show_matrix(self):
        matrix = []
        for i in range(self.vertices):
            matrix.append(self.graph[i])
        return matrix



#IMPORTANTE: VER MANUAL DE USO DA CLASSE NO FINAL DO ARQUIVO
class Grafo:

    def __init__(self, grafo_txt, escolha):
        
        self.arestas = []
        self.vetor = []
        self.matrix = []
        self.nArestas = 0
        self.representacao = escolha
        self.nomeGrafo = grafo_txt[len(grafo_txt)-15:len(grafo_txt)-4]

        while(True):
            self.temPesos = input("O grafo possui pesos (sim/nao)? ")
            if self.temPesos == "sim" or self.temPesos == "nao":
                break

        if self.temPesos == "sim":
            self.temPesosNeg = False
        
        #USUÁRIO ESCOLHE ENTRE MATRIZ (1) E VETOR (2)
        #while(True):
        #    escolha = input("Digite 1 para representar o grafo com um Matriz de adjacências ou 2 para representar com um Vetor de adjacências: ")
        #    if (escolha == "1" or escolha == "2"):
        #        self.representacao = escolha
        #        break
        #    else:
        #        print("Resposta inválida. Favor digitar somente 1 ou somente 2")

        #LEITURA DO ARQUIVO
        with open(grafo_txt, 'r') as file:
            #LEITURA DA QUANTIDADE DE VÉRTICES
            self.nVertices = int((file.readline().rstrip('\n')))

            self.grau = [0] * (self.nVertices + 1)

            #AQUI A LEITURA SE DIVIDE EM DOIS CASOS DEPENDENDO DA ESCOLHA DO USUÁRIO DE ESTRUTURA

            #CASO O USUÁRIO ESCOLHA A MATRIZ E O GRAFO SEJA SEM PESOS
            if (self.representacao == '1' and self.temPesos == "nao"):

                while(True):
                    arestaPrimitiva = file.readline().rstrip('\n')
                    if arestaPrimitiva:
                        self.nArestas += 1
                        ap = []
                        for v in arestaPrimitiva.split():
                            ap.append(int(v))
                        aresta = (ap[0], ap[1])
                        self.grau[ap[0]] += 1
                        self.grau[ap[1]] += 1
                        self.arestas.append(aresta)
                    else:
                        break

                g = adjacencyMatrix(self.nVertices)
                for i in range(len(self.arestas)):
                    arestas = self.arestas[i]
                    g.add_edge(arestas[0], arestas[1])
                self.matrix = g.show_matrix()

            #CASO O USUÁRIO ESCOLHA O VETOR E O GRAFO SEJA SEM PESOS
            elif (self.representacao == '2' and self.temPesos == "nao"):           
                self.vetor = [[]] * (self.nVertices+1)
                while(True): 
                    arestaPrimitiva = file.readline().rstrip('\n')
                    if arestaPrimitiva:
                        self.nArestas += 1
                        ap = []
                        for v in arestaPrimitiva.split():
                            ap.append(int(v))
                        self.grau[ap[0]] += 1
                        self.grau[ap[1]] += 1

                        self.vetor[ap[0]] = sorted(self.vetor[ap[0]] + [ap[1]])
                        self.vetor[ap[1]] = sorted(self.vetor[ap[1]] + [ap[0]])
                    else:
                        break

            #CASO O USUÁRIO ESCOLHA A MATRIZ E O GRAFO TENHA PESOS
            elif (self.representacao == '1' and self.temPesos == "sim"):

                while(True):
                    arestaPrimitiva = file.readline().rstrip('\n')
                    if arestaPrimitiva:
                        self.nArestas += 1
                        ap = arestaPrimitiva.split()
                        aresta = (int(ap[0]), int(ap[1]))
                        self.grau[int(ap[0])] += 1
                        self.grau[int(ap[1])] += 1
                        self.arestas.append((aresta, float(ap[2])))
                        
                        if float(ap[2]) < 0:
                            self.temPesosNeg = True
                    else:
                        break

                g = adjacencyMatrix(self.nVertices, True)
                for i in range(len(self.arestas)):
                    arestas = self.arestas[i][0]
                    g.add_w_edge(arestas[0], arestas[1], self.arestas[i][1])
                self.matrix = g.show_matrix()
        

            #CASO O USUÁRIO ESCOLHA O VETOR E O GRAFO TENHA PESOS
            elif (self.representacao == '2' and self.temPesos == "sim"):           
                self.vetor = [[]] * (self.nVertices+1)
                while(True): 
                    arestaPrimitiva = file.readline().rstrip('\n')
                    if arestaPrimitiva:
                        self.nArestas += 1
                        ap = arestaPrimitiva.split()
                        self.grau[int(ap[0])] += 1
                        self.grau[int(ap[1])] += 1

                        self.vetor[int(ap[0])] = sorted(self.vetor[int(ap[0])] + [(int(ap[1]), float(ap[2]))])
                        self.vetor[int(ap[1])] = sorted(self.vetor[int(ap[1])] + [(int(ap[0]), float(ap[2]))])

                        if float(ap[2]) < 0:
                            self.temPesosNeg = True

                    else:
                        break
            
            #CASO PELO MENOS UMA DAS ENTRADAS SEJA INVÁLIDA
            else:
                raise Exception("ENTRADAS INVÁLIDAS")

        self.grau = sorted(self.grau)
        if self.nVertices % 2 == 0:
            self.grauMediano = (self.grau[int(self.nVertices/2)] + self.grau[int(self.nVertices/2) + 1]) / 2
        else:
            self.grauMediano = (self.grau[int(self.nVertices/2 + 0.5)])
        self.grauMedio = 0
        for g in self.grau:
            self.grauMedio += g
        self.grauMedio = self.grauMedio / self.nVertices

        with open("arquivoSaida.txt", "w") as file:
            file.write("Numero de vertices: " + str(self.nVertices) + "\n")
            file.write("Numero de arestas: " + str(self.nArestas) + "\n")
            file.write("Grau minimo: " + str(self.grau[1]) + "\n")
            file.write("Grau maximo: " + str(self.grau[self.nVertices]) + "\n")
            file.write("Grau medio: " + str(self.grauMedio) + "\n")
            file.write("Grau mediano: " + str(self.grauMediano) + "\n")


    def bfs(self, raiz):

        fila = []
        vertices = [-1] * (self.nVertices + 1)
        nivel = [-1] * (self.nVertices + 1)
        pai = [-1] * (self.nVertices + 1)

        vertices[raiz] = 0
        pai[raiz] = 0
        nivel[raiz] = 0
        fila.append(raiz)

        if (self.representacao == "1"):
            while(len(fila) != 0):
                x = fila[0] - 1
                w = self.matrix[x]
                fila.pop(0)
                for j in range(self.nVertices):
                    if (w[j] == 1 and vertices[j+1] == -1):
                        vertices[j+1] = 0
                        fila.append(j+1)
                        pai[j+1] = x+1
                        nivel[j+1] = nivel[x+1] + 1

        else:
            while(len(fila) != 0):
                x = fila[0]
                w = self.vetor[x]
                fila.pop(0)
                for j in w:
                    if(vertices[j] == -1):
                        vertices[j] = 0
                        fila.append(j)
                        pai[j] = x
                        nivel[j] = nivel[x] + 1

        return (nivel, pai)



    def bfsFile(self, raiz):
        x = self.bfs(raiz)
        with open("bfs.txt", "w") as file:
            file.write("VERTICE / PAI / NIVEL \n")
            for i in range(1, self.nVertices+1):
                file.write(str(i) + " / " + str(x[1][i]) + " / " + str(x[0][i]) + "\n")
            file.write("OS VERTICES COM NIVEL E PAI -1 NAO PERTENCEM A ESSA COMPONENTE CONEXA \n")
            file.write("O VERTICE COM NIVEL 0 E PAI 0 = RAIZ")



    def dfs(self, raiz):

        pilha = []
        vertices = [-1] * (self.nVertices + 1)
        nivel = [-1] * (self.nVertices + 1)
        pai = [-1] * (self.nVertices + 1)

        pai[raiz] = 0
        nivel[raiz] = 0
        pilha.append(raiz)

        vpuv = [-1] * (self.nVertices + 1)

        if (self.representacao == "1"):
            while(len(pilha) != 0):
                x = pilha[0] - 1
                if(pai[x+1]) == -1:
                    pai[x+1] = vpuv[x+1]
                    nivel[x+1] = nivel[vpuv[x+1]] + 1
                pilha.pop(0)
                if (vertices[x+1] != 0):
                    vertices[x+1] = 0
                    temp = []
                    for j in range(self.nVertices):
                        if self.matrix[x][j] == 1:
                            temp.append(j+1)
                            vpuv[j+1] = x+1
                    pilha = temp + pilha           

        else:
            while(len(pilha) != 0):
                x = pilha[0]
                if(pai[x]) == -1:
                    pai[x] = vpuv[x]
                    nivel[x] = nivel[vpuv[x]] + 1
                pilha.pop(0)
                if (vertices[x] != 0):
                    vertices[x] = 0
                    w = self.vetor[x]
                    temp = []
                    for j in w:
                        temp.append(j)
                        vpuv[j] = x
                    pilha = temp + pilha
        
        return (nivel, pai)

    
    
    def dfsFile(self, raiz):
        x = self.dfs(raiz)
        with open("dfs.txt", "w") as file:
            file.write("VERTICE / PAI / NIVEL \n")
            for i in range(1, self.nVertices+1):
                file.write(str(i) + " / " + str(x[1][i]) + " / " + str(x[0][i]) + "\n")
            file.write("OS VERTICES COM NIVEL E PAI -1 NAO PERTENCEM A ESSA COMPONENTE CONEXA \n")
            file.write("O VERTICE COM NIVEL 0 E PAI 0 = RAIZ")



    def dijkstra(self, s):
        dist = [math.inf] * (self.nVertices + 1)
        explorados = [0] * (self.nVertices + 1) 
        dist[s] = 0
        caminho = [[]] * (self.nVertices + 1)
        caminho[s] = caminho[s] + [s]
        tamExplorados = 0
        while(tamExplorados != self.nVertices):
            u = 0
            dist_u = dist[0]
            for i in range(self.nVertices + 1):
                if dist[i] < dist_u and explorados[i] != 1:
                    u = i
                    dist_u = dist[u]
            explorados[u] = 1
            tamExplorados += 1
            
            if (self.representacao == "1"):
                for vizinho in range(self.nVertices):
                    aresta_uv = self.matrix[u-1][vizinho]
                    if aresta_uv != math.inf:
                        if dist[vizinho+1] > dist_u + aresta_uv:
                            dist[vizinho+1] = dist_u + aresta_uv
                            caminho[vizinho+1] = caminho[u] + [vizinho+1]

            else:
                for vizinho in self.vetor[u]:
                    if dist[vizinho[0]] > dist_u + vizinho[1]:
                        dist[vizinho[0]] = dist_u + vizinho[1]
                        caminho[vizinho[0]] = caminho[u] + [vizinho[0]]

        #    print(u, explorados[1:], dist[1:]) 
        #print()
        #print(caminho)
        return (dist, caminho)

 

    #def floyd_warshall(self):
    #    d = deepcopy(self.matrix)
    #    for i in range(self.nVertices):
    #        d[i][i] = 0
    #    pred = deepcopy(d)
    #
    #    for k in range(self.nVertices):
    #        for i in range(self.nVertices):
    #            for j in range(self.nVertices):
    #                if(d[i][j] > d[i][k] + d[k][j]):
    #                    d[i][j] = d[i][k] + d[k][j]
    #                    pred[i][j] = pred[k][j]
        
        #for linha in d:
        #    print(linha)
        #print()
        #for linha in self.matrix:
        #    print(linha)
    #    return d



    def prim(self):
        s = 1
        peso_total = [0] * (self.nVertices+1)  
        arestas_mst = [None] * (self.nVertices + 1)
        dist = [math.inf] * (self.nVertices + 1)
        explorados = [0] * (self.nVertices + 1) 
        dist[s] = 0
        caminho = [[]] * (self.nVertices + 1)
        caminho[s] = caminho[s] + [s]
        tamExplorados = 0
        while(tamExplorados != self.nVertices):
            u = 0
            dist_u = dist[0]
            for i in range(self.nVertices + 1):
                if dist[i] < dist_u and explorados[i] != 1:
                    u = i
                    dist_u = dist[u]
            explorados[u] = 1
            tamExplorados += 1
            
            if (self.representacao == "1"):
                for vizinho in range(self.nVertices):
                    aresta_uv = self.matrix[u-1][vizinho]
                    if aresta_uv != math.inf:
                        if dist[vizinho+1] > dist_u + aresta_uv:
                            dist[vizinho+1] = dist_u + aresta_uv
                            caminho[vizinho+1] = caminho[u] + [vizinho+1]
                            arestas_mst[vizinho+1] = (vizinho+1, u, aresta_uv)
                            peso_total[vizinho+1] = aresta_uv
                            

            else:
                for vizinho in self.vetor[u]:
                    if dist[vizinho[0]] > dist_u + vizinho[1]:
                        dist[vizinho[0]] = dist_u + vizinho[1]
                        caminho[vizinho[0]] = caminho[u] + [vizinho[0]]
                        arestas_mst[vizinho[0]] = (vizinho[0], u, vizinho[1])
                        peso_total[vizinho[0]] = vizinho[1]

        arestas_mst = arestas_mst[2:]
        peso = sum(peso_total) 

        with open("mst_" + self.nomeGrafo + ".txt", 'w') as arq:
            for e in arestas_mst:
                if e != None:
                    arq.write(str(e[0]) + " " + str(e[1]) + "\n")


        return peso



    def dist_caminho_entre_uv(self, u, v):
        if self.temPesos == "não":
            nivel = self.bfs(u)[0]
            return nivel[v]
        else:
            if self.temPesosNeg == False:
                x = self.dijkstra(u)
                distancia = x[0][v]
                caminho = x[1][v]
                return (distancia, caminho)



    def dist_caminho_de_u_a_todos(self, u):
        if self.temPesos == "não":
            nivel = self.bfs(u)[0]
            return nivel
        else:
            if self.temPesosNeg == False:
                x = self.dijkstra(u)
                distancia = x[0]
                caminho = x[1]
                return (distancia, caminho)
    

    def diametro(self):
        dia = [0, [0,0]]
        for i in range(1, self.nVertices+1):
            for j in range(i, self.nVertices+1):
                if (i != j):
                    d = self.distancia(i, j)
                    if d > dia[0]:
                        dia[0] = d
                        dia[1][0] = i
                        dia[1][1] = j
        print(dia[0])

    

    def diametroAprox(self):
        dia = [0, [0,0]]
        for i in range(1, int(math.log(self.nVertices, 2))):
            k = random.randint(1, self.nVertices)
            j = random.randint(1, self.nVertices)
            if (k != j):
                d = self.distancia(k, j)
                if d > dia[0]:
                    dia[0] = d
                    dia[1][0] = k
                    dia[1][1] = j
        print(dia[0])



    def componentesConexas(self):

        nComponentesConexas = 0
        componentes = []
        vertices = [-1] * (self.nVertices + 1)

        for v in range(1, self.nVertices + 1):
            if (vertices[v] == -1):
                nivel = self.bfs(v)[0]
                nComponentesConexas += 1
                nVerticesCC = 0
                cc = []
                for n in range(1, self.nVertices + 1):
                    if (nivel[n] != -1):
                        vertices[n] = 0
                        cc.append(n)
                        nVerticesCC += 1
                componentes.append((cc, nVerticesCC))
        
        return (nComponentesConexas, componentes)


#ABAIXO, DEVE-SE POR O CAMINHO PARA O ARQUIVO TXT QUE CONTEM OS GRAFOS ENTRE AS ASPAS COMO PRIMEIRO PARAMETRO. NÂO SE DEVE RETIRAR O r ANTES DAS ASPAS
#O SEGUNDO PARAMETRO DEVE SER SOMENTE "1" PARA USAR A REPRESENTAÇÂO DE MATRIZ OU "2" PARA USAR O VETOR. AMBOS DEVEM ESTAR ENTRE ASPAS!!!

g = Grafo(r"C:\Users\Bernardo\Documents\ufrj_2021_2\Trab1_TeoGraf\rede_colaboracao.txt", "2")
x = g.dijkstra(2722)
dist = x[0]
print(dist[11365])
print(dist[471365])
print(dist[5709])
print(dist[11386])
print(dist[343930])


#t_medio_djk = 0
#t_medio_djk_otm = 0
#v_iniciais = []
#for i in range(100):
#    v_iniciais.append(random.randint(1, g.nVertices + 1))
#
#for i in range(100):
#   end_djk = time.time()
#    t_medio_djk += end_djk - start_djk
#
#t_medio_djk = t_medio_djk / 100
#p = g.prim()
#
#print("Tempo médio Dijkstra grafo 1: " + str(t_medio_djk))
#print("Peso total da mst deste grafo: " + str(p))
#print()



#print(g.matrix)
#g.dijkstra(1)
#print()
#print()
#for i in range(tam):
#    print(x[i].valor, y[i])
#y = g.floyd_warshall()[0]
#for i in range(len(y)):
#    print(y[i])
#print()
#print()
#g.prim()
#print(g.dist_caminho_entre_uv(1,10))
#print(g.dist_caminho_entre_uv(1,20))
#print(g.dist_caminho_entre_uv(1,30))
#print(g.dist_caminho_entre_uv(1,40))
#print(g.dist_caminho_entre_uv(1,50))
#g.dist_caminho_de_u_a_todos(1)
