# consumer-rabbitmq
 
## Objetivo
Backend responsável por consumir as mensagens publicadas no RabbitMQ.

## Sobre a Solução 
Atualmente os consumers estão hospedados em um servidor gratuito, entretanto, detalhes de como executar em ambiente local poderão ser consultados no tópico "Testes".

## Testes
O testes dos consumers podems ser realizados de forma local, apesar de atualmente um consumer estar ativo em um ambiente dedicado. 

Dessa forma, caso for realizado um teste, talvez seja possível observar que nem todas as mensagens serão consumidas pelo consumer ativado. Poderá ser solicitado a mim que realize a inativação desse consumer, para que se obtenha um resultado efetivo.

Para que seja possível, é necessarío:
- Possuir o Python (v3.11) instalado;
- Adicionar o Python ao Path;
- Abrir o Prompt de Comando.

Após abrir o Prompt, deverá ser acessado o diretório onde foi baixado o repositório. 

Deverá ser executado o comando "pip install -r requirements.txt".

Deverá ser executado o comando "python receive.py".

Será exibida uma mensagem "[*] Aguardando mensagens" e, quando publicadas as mensagens, o consumer irá automaticamente baixar da fila.

Será exibido um log no Prompt: "[*] Recebido" + conteúdo publicado.

Para gerar uma mensagem, poderá ser acessada a aplicação web desenvolvida: https://api-marcacao-ponto.herokuapp.com/ e realizado um registro de ponto.