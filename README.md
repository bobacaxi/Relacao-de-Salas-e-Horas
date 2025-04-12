# Relações de Salas-Horas a partir de PDFs
Esse repositório é uma tentativa de automatizar o trabalho de produzir a relação de dias, salas e horas em que há aulas, posto que há um PDF da universidade com uma tabela de dias, aulas, salas e horários disponível.

O principal instrumento utilizado (além do python) é o PIP **pdfplumber**, especificamente seu método de extração de tabelas de PDFs. Sua documentação está disponível em https://pypi.org/project/pdfplumber/, caso queira modificar os códigos para uso específico. Também é utilizado o módulo **RE** nativo do python para separação de padrões de texto, e o módulo **datetime**, também nativo, para comparação direta entre horários.

Tenha certeza de instalar o PIP **pdfplumber** na sua IDE ou terminal antes de rodar os códigos.

Fiz esses código às pressas, então certamente não são os mais eficientes. Em algum momento pretendo utilizar as classes do python para redigí-los melhor, mas, por enquanto, como estão funcionam bem para uso cotidiano.


# relacao_dia_curso.py
Se você tem exatamente 1 (um) PDF com tabelas que especificam os dias, salas e horas de cada aula salvo, e quer a relação para um dia da semana em específico: 
<br/>

1. Abra o arquivo **relacao_dia_curso.py** para edição;

2. Na seção "Configurações" do código:
   - especificar o dia das aulas para relação;
     
   - especificar o caminho do arquivo PDF com as tabelas;
     
   - especificar possíveis exclusões de aulas (e.g. *exclusoes = ["Estágios", "Laboratório"]* ) e, se o caso, alterar excluir = True;

3. Rodar o código.


<br/>
Em seguida, a IDE vai printar a relação de salas e horas para o dia especificado, com o título (curso e turno) acima.


# relacao_dia.py
Se você tem mais de 1 (um) PDF com tabelas que especificam os dias, salas e horas de cada aula salvo, e quer a relação para um dia da semana em específico:
<br/>

1. Abra o arquivo **relacao_dia.py** para edição;

2. Na seção "Configurações" do código:

   - especificar o dia das aulas para relação;

   - especificar o caminho da pasta dos arquivos PDF com as tabelas, nomeados numericamente de 01-X (e.g. *07.pdf*);

   - especificar o número total de PDFs;

   - especificar possíveis exclusões de aulas (e.g. *exclusoes = ["Estágios", "Laboratório"]* ) e, se o caso, alterar *excluir = True*;
(é possível excluir aulas de somente alguns PDFs especificando no loop, como eu deixei pronto)

3. Rodar o código.

<br/>
Em seguida, a IDE vai printar a relação de salas e horas para o dia especificado, com o título (curso e turno) de cada PDF acima.


# relacao_semana.py
Se você tem mais de 1 (um) PDF com tabelas que especificam os dias, salas e horas de cada aula salvo, e quer a relação para todos os dias da semana:
<br/>

1. Abra o arquivo **relacao_semana.py** para edição;

2. Na seção "Configurações" do código: 

   - especificar o caminho da pasta dos arquivos PDF com as tabelas, nomeados numericamente de 01-X (e.g. *07.pdf*);

   - especificar o número total de PDFs;

   - especificar possíveis exclusões de aulas (e.g. *exclusoes = ["Estágios", "Laboratório"]* ) e, se o caso, alterar *excluir = True*;
(é possível excluir aulas de somente alguns PDFs especificando no loop, como eu deixei pronto)

3. Rodar o código.

<br/>
Em seguida, a IDE vai printar a relação de salas e horas para a semana, com o título (curso e turno) de cada PDF acima, começando da segunda e terminando na sexta. Se você quer printar os sábados também, adicionar sábado ao dicionário e alterar a range da variável k para 7 no loop.

# Considerações

Como eu fiz o código inicialmente para uso próprio, o título é recortado do texto inicial do arquivo PDF a partir de uma indexação específica ( i.e. a função extrair_titulo recorta o título logo após a palavra "Curso:"), ou seja, se o título não for recortado para você, mude o critério para recorte. O final do título é recortado pela identificação do turno, visto que normalmente consta nos textos iniciais dos documentos algo na forma de "Ciências Sociais GRAD Turno: MANHÃ"; se não for o seu caso, sugiro modificar a função *extrair_título*, na seção *Título* da função principal.

Além disso, se os turnos de sua universidade forem escritos de forma diferente e não forem reconhecidos, o título não será printado. Se isso ocorrer, adicione os turnos como constam em seus PDFs no dicionário *turnos*, e deve funcionar normalmente.

Por fim, os loops entre PDFs só funcionarão se os arquivos estiverem na mesma pasta especificada em *caminho* e numerados começando do número 01, como em *01.pdf*. Os números nos nomes dos arquivos devem estar sempre em 2 (dois) dígitos para serem identificados (e.g. *11.pdf* e *06.pdf*), e as extensões devem sempre ser *x.pdf*, e não *x.PDF*. Caso contrário, os arquivos não serão identificados.

# Exemplo - PUC-SP

Há, em anexo, PDFs disponíveis publicamente no site da PUC-SP, especificamente o quadro de horários dos cursos do Campus Monte Alegre, já numerados corretamente para listagem da relação de salas-horas. Há também um arquivo de texto que esclarece a que curso se refere o número de cada PDF, e um DOCX que já faz a listagem completa para todos os cursos do Campus Monte Alegre na semana toda.
