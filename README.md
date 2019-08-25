# sistemas_distribuidos
Repositório voltado para entrega dos trabalhos de sistemas distribuídos.

A ideia do meu projeto para a discilplina é um conjunto de textos online sobre aves em que várias pessoas podem ler ao mesmo tempo e editar para complementar e trazer novas informações sobre determinada espécie, ou seja, se eu sou uma especialista em araras eu poderia colocar informações adicionais na página de araras, caso outra pessoa já tivesse escrito algo mas que esteja errado eu também poderia editar ou apagar. 

Esse projeto pode ser dividido em algumas partes, um servidor que mantém todas as páginas no ar, um banco de dados que guarda todas as páginas em uma máquina e uma interface web para que os usuários possam visualizar e editar as páginas de seu interesse.

Testes interessantes a serem feitos :
- teste de concorrência : dado vários usarios acessando a mesma página e editando ao mesmo tempo se o servidor consegue suportar e manter as páginas no ar .
- teste de exclusividade : como garantir que apenas uma pessoa edite 1 página de cada vez, ou seja, nunca será possível que 2 pessoas editem a mesma página simultaneamente.
- teste de persistência dos dados : garantir que o site mantém os dados para acessar qualquer hora do dia em qualquer lugar .

Funcionalidades principais :

- Acesso a várias páginas distintas sobre várias espécies .
- Capacidade de edição para o usuário editar as páginas .
- Sistema de login e senha em que a edição só é possível para membros logados .

Obs.: No caso do acesso apenas para leitura não é necessário login.

