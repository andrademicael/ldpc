i = 8

#testa se algum nó de paridade deve ser conectado obrigatoriamente nesta iteração
if any(vpar==(n-i)):
    print("entrou")
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

