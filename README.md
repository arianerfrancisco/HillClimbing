# HillClimbing
 
O Hill Climbing é um algoritmo clássico para otimização, sendo bastante eficiente na tarefa de encontrar máximos ou mínimos locais, usando da técnica de explotação que vimos anteriormente.

Nesse algoritmo nós iniciamos de um ponto aleatório X e fazemos a sua avaliação.
Suponhamos que esse seja um ponto inicial no nosso espaço de solução

Feito isso, nós nos movemos do nosso ponto X original para um novo ponto vizinho ao que estamos o X’.

Se esse novo ponto X’ for uma solução melhor do que nosso ponto anterior, ficamos nele e fazemos esse processo novamente, porém caso seja inferior, voltamos para nosso ponto inicial X e tentamos visitar um outro vizinho.
