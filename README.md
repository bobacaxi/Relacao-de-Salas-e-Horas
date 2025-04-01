# Produção de Relações de Salas-Horas a partir de PDFs
Esse repositório é uma tentativa de automatizar o trabalho de produzir a relação de dias, salas e horas em que há aulas, posto que há um PDF da universidade com uma tabela de dias, aulas, salas e horários disponível.

O principal instrumento utilizado (além do python) é o PIP pdfplumber, especificamente seu método de extração de tabelas de PDFs. Sua documentação está disponível em https://pypi.org/project/pdfplumber/, caso queira modificar os códigos para uso específico. Também é utilizado o módulo RE nativo do python para separação de padrões de texto, e o módulo datetime, também nativo, para comparação direta entre horários.

Tenha certeza de instalar o PIP "pdfplumber" na sua IDE ou terminal antes de rodar os códigos.

Fiz esses código às pressas, então certamente não são os mais eficientes. Em algum momento pretendo utilizar as classes do python para redigí-los melhor, mas, por enquanto, como estão funcionam bem para uso cotidiano.


# relacao_dia_curso.py
Se você tem exatamente 1 (um) PDF com tabelas que especificam os dias, salas e horas de cada aula salvo, e quer a relação para um dia da semana em específico:

1 - Abra o arquivo relacao_dia_curso.py para edição;

2 - Na seção "Configurações" do código:

2.1 - especificar o dia das aulas para relação;

2.2 - especificar o caminho do arquivo PDF com as tabelas;

2.3 - especificar possíveis exclusões de aulas (e.g. exclusao = "Estágios") e, se o caso, alterar excluir = True;

3 - Rodar o código.

Em seguida, a IDE vai printar a relação de salas e horas para o dia especificado, com o título (curso e turno) acima.


# relacao_dia.py
Se você tem mais de 1 (um) PDF com tabelas que especificam os dias, salas e horas de cada aula salvo, e quer a relação para um dia da semana em específico:

1 - Abra o arquivo relacao_dia.py para edição;

2 - Na seção "Configurações" do código:

2.1 - especificar o dia das aulas para relação;

2.2 - especificar o caminho da pasta dos arquivos PDF com as tabelas, nomeados numericamente de 01-X (e.g. "07.pdf");

2.3 - especificar o número de PDFs;

2.3 - especificar possíveis exclusões de aulas (e.g. exclusao = "Estágios") e, se o caso, alterar excluir = True;
(é possível excluir aulas de somente alguns PDFs especificando no loop, como eu deixei pronto)

3 - Rodar o código.

Em seguida, a IDE vai printar a relação de salas e horas para o dia especificado, com o título (curso e turno) de cada PDF acima.


# relacao_semana.py
Se você tem mais de 1 (um) PDF com tabelas que especificam os dias, salas e horas de cada aula salvo, e quer a relação para todos os dias da semana:

1 - Abra o arquivo relacao_semana.py para edição;

2 - Na seção "Configurações" do código:

2.1 - especificar o caminho da pasta dos arquivos PDF com as tabelas, nomeados numericamente de 01-X (e.g. "07.pdf");

2.2 - especificar o número de PDFs;

2.3 - especificar possíveis exclusões de aulas (e.g. exclusao = "Estágios") e, se o caso, alterar excluir = True;
(é possível excluir aulas de somente alguns PDFs especificando no loop, como eu deixei pronto)

3 - Rodar o código.

Em seguida, a IDE vai printar a relação de salas e horas para a semana, com o título (curso e turno) de cada PDF acima, começando da segunda e terminando na sexta. Se você quer printar os sábados também, adicionar sábado ao dicionário e alterar a range da variável "k" para 6 no loop.

# Considerações

Como eu fiz o código inicialmente para uso próprio, o título é recortado do texto inicial do arquivo PDF a partir de uma indexação específica ( i.e. titulo_rasc = paginas[0].extract_text()[190:254] ), ou seja, se o título for recortado errado para você, mude o número inicial do recorte.

O final do título é recortado pela identificação do turno, visto que normalmente consta nos textos iniciais dos documentos algo na forma de "Ciências Sociais GRAD Turno: MANHÃ"; se não for o seu caso, sugiro modificar a função "extrair_título", na seção Título da função principal. Além disso, se os turnos de sua universidade forem escritos de forma diferente e não forem reconhecidos, o título não será printado. Se isso ocorrer, adicione os turnos de seus PDFs no dicionário "turnos", e deve funcionar normalmente.
