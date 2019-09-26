from random import randint
import os.path
import sys

matrizNos = []
listaNosVisitados = []
listaCaminhosCompletos = []
pathMelhorCaminhoSalvo = 'c:/tmp/melhorCaminho.csv'
pathDadosNos = 'c:/tmp/dados.csv'

#Inicio das Funções -----------------------------------------------
def SelecionaProximoNo(dado) :
    valores = []    
    tamanho = len(dado)
    for indice in range(tamanho) : #Loop para verifica qual posição tem valor
        noNaoVisitado = not indice in listaNosVisitados #Verifica se o nó já não foi visitado
        if dado[indice] > 0 and noNaoVisitado:  #Se valor maior que zero e não foi visitado
            valores.append(indice) #Pega a posição

    if len(valores) == 0 : #Se não tem mais nó para ir
        return -1 #Devolve -1 para terminar esse caminho
    
    #Senão terminou sorteia um nó e devolve
    posicaoNo = randint(0, len(valores) - 1)
    return valores[posicaoNo]

def CalculaCusto(nos) :
    soma = 0
    numNos = len(nos)
    for i in range(numNos - 1) :
        y = nos[i]
        x = nos[i+1]
        soma += matrizNos[y][x]

    return soma

def PreencheVetorComDados(tr) :
    ints = []
    for d in tr : #Percorre todos os valores do vetor passado como paramentro
        i = 0
        if d != "" : #Se conteudo da posição atual do vetor for diferente de vazio
            try :
                i = int(d) #Tenta converter para inteiro
            except :
                i = 0 #Caso ocorrer erro coloca zero
                print(f"Erro ao converter {d} foi setado o valor zero")
        ints.append(i) #Inclui o dado convertido na lista de inteiros

    return ints

def LerMenorCaminhoSalvo() :
    
    melhorCaminho = []

    if os.path.isfile(pathMelhorCaminhoSalvo) : #Se exisitir o arquivo

        arq = open(pathMelhorCaminhoSalvo, 'r') #Abre o arquivo no local indicado
        textoArq = arq.readlines()  #Lê o arquivo e joga para a variavel
        
        #Percorre o arquivo linha a linha, converte os custos para inteiro e joga os dados para dentro da matriz
        for linha in textoArq :

            linha = linha.replace("\n", "") #Tira as quebra de linha
            tr = linha.split(";") #Gera o vetor de string separando o arquivo pelo separador ponto e virgula
            melhorCaminho = PreencheVetorComDados(tr) #Pega os dados do arquivo

        arq.close() #Fecha o arquivo

    return melhorCaminho

def SalvaArquivoMelhorCusto(caminho) :
    arq = open(pathMelhorCaminhoSalvo, 'w')
    nosSalvar = ""
    qtdNos = len(caminho)
    for posicao in range(qtdNos) :
        nosSalvar += str(caminho[posicao])

        if posicao < qtdNos - 1 :
            nosSalvar += ";"

    arq.write(nosSalvar)
    arq.close()

#Fim das Funções -----------------------------------------------

if os.path.isfile(pathDadosNos) == False : #Se exisitir o arquivo
    print(f"O arquivo não foi encontrado, {pathDadosNos}")
    sys.exit(0)

arq = open(pathDadosNos, 'r') #Abre o arquivo no local indicado
textoArq = arq.readlines()  #Lê o arquivo e joga para a variavel

#Percorre o arquivo linha a linha, converte os custos para inteiro e joga os dados para dentro da matriz
for linha in textoArq :

    linha = linha.replace("\n", "") #Tira as quebra de linha
    tr = linha.split(";") #Gera o vetor de string separando o arquivo pelo separador ponto e virgula
    ints = PreencheVetorComDados(tr) #Pega os dados do arquivo
    matrizNos.append(ints) #Após percorrer a linha toda do arquivo inclui na matriz

arq.close() #Fecha o arquivo

numTentativas = 100 #Número de tentaivas para achar um caminho válido
qtdNos = len(matrizNos) #Pega a quantidade de nós da matriz com os dados
noInicial = 0 #Nó inicial 0, já que a matriz inicia em zero todos números 
                  #dos nós reais do problema será decrementado um
melhorCaminhoSalvo = LerMenorCaminhoSalvo()
melhorCustoSalvo = CalculaCusto(melhorCaminhoSalvo)

#Enquanto não terminar o número de tentativas, procura um caminho
while numTentativas > 0 :

    #Inicia as variaveis que será usada para percorrer o caminho
    
    noAtual = 0 #Guarda o valor do nó atual em que se encontra na interação
    listaNosVisitados.clear() #Lista para colocar os nós já visitados
    listaNosVisitados.append(noInicial) #Inclui a posição inicial na matriz
    
    for loop in range(qtdNos) : #Loop para se deslocar ente os nós e achar um caminho válido
        proximoNo = SelecionaProximoNo(matrizNos[noAtual]) #Pega o próximo nó que será visitado

        if proximoNo < 0 : # Verifica se acabou de percorrer o caminho
            if len(listaNosVisitados) == qtdNos : #Se percorreu todos os nós
                if matrizNos[noAtual][noInicial] > noInicial : #Se tem ligação com o nó inicial, o valor é maior que zero
                    listaNosVisitados.append(noInicial) #Então inclui o primeiro nó no final para fechar o ciclo percorrido

                    #Faz uma copia dos nós visitados e salva na lista de caminhos completos
                    auxNosVisitados = []
                    for n in range(len(listaNosVisitados)) :
                        auxNosVisitados.append(listaNosVisitados[n])
                    listaCaminhosCompletos.append(auxNosVisitados)
            break
        
        #Senão terminou de percorrer coloca o nó na lista de visitados
        listaNosVisitados.append(proximoNo)
        noAtual = proximoNo #Atualiza nó atual
    
    numTentativas -= 1 #Decrementa o número de tentativas

qtdCaminhos = len(listaCaminhosCompletos) #Pega a quantidade de caminhos encontrados
menorCusto = -1
menorCaminhoAtual = []

for caminho in range(qtdCaminhos) :    
    custoTotalAtual = CalculaCusto(listaCaminhosCompletos[caminho])
    if menorCusto == -1 : #Se não tem um menor custo ainda
        menorCusto = custoTotalAtual
        menorCaminhoAtual = listaCaminhosCompletos[caminho]
    elif custoTotalAtual < menorCusto : #Se o custo calculado atual for menor que o custo guardado
        menorCusto = custoTotalAtual
        menorCaminhoAtual = listaCaminhosCompletos[caminho]

if qtdCaminhos > 0 : #Se achou caminho

    if melhorCustoSalvo <= 0 :
        SalvaArquivoMelhorCusto(menorCaminhoAtual)
        for i in range(len(menorCaminhoAtual)) : #Incrementa 1 para ficar com a numeração dos nós reais
            menorCaminhoAtual[i] += 1
        print(f"{menorCaminhoAtual} = Custo: {menorCusto}")

    elif melhorCustoSalvo > menorCusto :
        SalvaArquivoMelhorCusto(menorCaminhoAtual)
        for i in range(len(menorCaminhoAtual)) : #Incrementa 1 para ficar com a numeração dos nós reais
            menorCaminhoAtual[i] += 1
        print(f"{menorCaminhoAtual} = Custo: {menorCusto}")

    else : #Imprimi o salvo
        for i in range(len(melhorCaminhoSalvo)) : #Incrementa 1 para ficar com a numeração dos nós reais
            melhorCaminhoSalvo[i] += 1
        print(f"{melhorCaminhoSalvo} = Custo: {melhorCustoSalvo}")

elif melhorCustoSalvo > 0 :
    for i in range(len(melhorCaminhoSalvo)) : #Incrementa 1 para ficar com a numeração dos nós reais
        melhorCaminhoSalvo[i] += 1
    print(f"{melhorCaminhoSalvo} = Custo: {melhorCustoSalvo}")

else :
    print("Não foi encontrado um caminho válido")