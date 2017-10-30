import numpy as np
import random as rd
from sympy import symbols
from sympy import integrate

n = 26
k = 12
lamb = np.array([0.3, 0.7])  
ro = np.array([0, 0.4, 0, 0.6])

#Função que cria os polinômios usando matemática simbólica (sympy)
#para poder integrar os polinômios e testar se definem uma taxa igual a k/n
def poly_array(coef):

    x = symbols('x')
    for i in range(len(coef)):
        if i==0:
            y = coef[i]*x**i;
        else:
            y = y + coef[i]*x**i;

    return y

teste1 = (np.sum(lamb)==1 and np.sum(ro) == 1)

#testar se os polinomios concordam com a taxa do código
r = 1 - integrate(poly_array(ro),(x,0,1))/integrate(poly_array(lamb),(x,0,1))
#admite apenas as 5 primeiras casas decimais das variáveis. caso não seja feito, 
#sempre dará falso
teste2 = round(r,5) == round(k/n,5) 

if (teste1 and teste2): #caso os teste 1 e 2 falhem, o programa não pode ser executado
    
    ##################################################################################
    #                   INÍCIO DA DECLARAÇÃO DE VARIÁVEIS AUXILIARES

    #matriz H inicia com zeros
    h = np.zeros((k,n), dtype = int) 
    
    gv = len(lamb) #maior grau dos nós de variáveis
    gp = len(ro) #maior grau dos nós de paridade

    #quantidades associadas a cada grau para nós de variáveis
    ngvar = np.zeros((1,gv),  dtype = int)[0]
    #quantidades associadas a cada grau para nós de paridade
    ngpar = np.zeros((1,gp),  dtype = int)[0]
    
    #calcula a quantidade de vértices em cada grau
    for i in range(gv):
        if lamb[i] == 0:
            ngvar[i] = 0
        else:
            ngvar[i] = round(n*lamb[i])

    for i in range(gp):
        if ro[i] == 0:
            ngpar[i] = 0
        else:
            ngpar[i] = round(k*ro[i])

    #neste ponto, os vetores ngvar e ngpar indicam quantos vértices de cada grau deve vompor o grafo
    #ngvar = [12, 3, 56, 8] indica 12 vértices de grau 1, 3 de grau 2, 56 de grau 3 e 8 de grau 4       
    
    #vvar é um vetor cujos elementos indicam o grau de cada nó de variável do grafo
    vvar = np.zeros((1,0), dtype = int)
    
    for i in range(gv):
        vvar = np.append(vvar, (i+1)*np.ones((1,ngvar[i]), dtype = int))
    if len(vvar)!=n:
        erro = 1 #indica erro caso o numero de nós de variável seja diferente de n

    #vpar é um vetor cujos elementos indicam o grau de cada nó de paridade do grafo
    vpar = np.zeros((1,0), dtype = int)
    for i in range(gp):
        vpar = np.append(vpar, (i+1)*np.ones((1,ngpar[i]), dtype = int))
    if len(vpar)!=k:
        erro = 2 #indica erro caso o numero de nós de paridade seja diferente de k

    #coloca os vetores em ordem alatória
    rd.shuffle(vvar)
    rd.shuffle(vpar)

    var = np.array(range(n))
    par = np.array(range(k))

    busca2 = np.zeros((1,0), dtype = int)
    par2 = par

    ##################################################################################
    #  A partir deste ponto, será iniciado o processo de montagem da matriz

    for i in range(n):
        
        #testa se algum nó de paridade deve ser conectado obrigatoriamente nesta iteração
        if any(vpar==(n-i)):
            #print("entrou")
            busca = np.where(vpar == (n-i))[0] #procura os nós de paridade que precisam ser conectados nesta iteração
            
            if len(busca)>=vvar[i]:
                escolha = busca[:vvar[i]]
            else:
                #conecta ao nó de variável 'i' ós nós de paridade em busca (obrigatórios nessa iteração) e 'vvar[i]-len(busca)''
                #aleatórios do conjunto 'par\busca'
                f1 = np.delete(par2,np.append(busca, np.delete(par2,par)))
                f2 = vvar[i]-len(busca)
                escolha = np.append(busca, np.random.choice(f1,f2, replace = False))

                del f1, f2
        else: #caso não haja obrigatoriedade, são escolhidos nós de paridade aleatoriamente
            escolha = np.random.choice(par,vvar[i], replace = False)

        #atribui '1' para conexão entre os nós de paridade em 'escolha' e o nó de variável 'i'
        h[escolha, i] = np.ones_like(escolha)

        #vpar indica quantas edges precisam se conectar a cada nó de paridade
        vpar[escolha] = vpar[escolha] - 1

        #caso algum nó de paridade complete seu grau necessário, deve ser removido da lista de possíveis escolhas, 'par'
        if any(vpar == 0):
            #procura em 'vpar' os nós de paridade que já têm grau completo
            busca2 = np.where(vpar == 0)[0]
            #deleta os nós que completaram o grau nesta iteração, desconsiderando os nós que completaram grau na iteração 
            #anterior, estando estes armazenados em busca 3
            par = np.delete(par2,busca2)

            
    #return h

else:
    if teste1:
        print("Os coeficientes dos polinômios não somam 1")
    elif teste2:
        print("os polinomios definem uma taxa diferene de k/n")
    else:
        pass

print(h)
print(np.sum(h,0))
print(np.sum(h,1))