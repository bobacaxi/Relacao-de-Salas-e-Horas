import re
import pdfplumber
from datetime import time

#region Configurações
dia = "segunda"

caminho = "/path/to/folder/"

# 1-100 PDFs
num_pdfs = 30

# exclusões da relação
exclusoes = [
    'NÚCLEO',
    'LANATO',
    'LEXP'
]

excluir = True
#endregion

#region Dicionários
dias = {"segunda":1, "terça":2, "quarta":3, "quinta":4, "sexta":5}

dias_inv = {v: k for k, v in dias.items()}

turnos = ['MANHÃ', 'MAT', 'NOITE', 'NOT', 'VESP', 'VESP/MAT', 'VESP/NOT', 'MAT/VESP', 'NOT/VESP']

#endregion

# função principal
def relacao_salas_horas(caminho_para_pdf, dia_da_relacao):
    #importar pdfs
    with pdfplumber.open(caminho_para_pdf) as pdf:
        #region Título
        # extrair paginas
        paginas = pdf.pages

        # extrair curso e turno com outros resquícios do PDF
        titulo_rasc = paginas[0].extract_text()[160:254]

        # verificar quebras de linha no texto
        def verificar_quebras(exemplo):
            resultado = ''
            separado = titulo_rasc.split(' ')
            list = []
            for item in separado:
                if '\n' in item:
                    conta = item.count('\n')
                    if conta == 1:
                        ind = item.index('\n')
                        list.append(item[:ind])
                        list.append(item[(ind+1):])
                    elif conta == 2:
                        ind = item.index('\n')
                        list.append(item[:ind])
                        item2 = item[(ind+1):]
                        ind2 = item2.index('\n')
                        list.append(item2[:ind2])
                        list.append(item2[(ind2+1):])
                else:
                    list.append(item)
            for i in range(len(list)):
                resultado += list[i] + ' '
            return resultado

        # turno e curso rascunho sem quebras de linha
        titulo_rasc_ver = verificar_quebras(titulo_rasc)

        def extrair_titulo(titulo_teste):
            splitted = titulo_teste.split(' ')
            text = ''
            minimo = 0
            for i in range(len(splitted)):
                if splitted[i] == 'Curso:':
                    minimo = i
                if splitted[i] in turnos:
                    maximo = i
                    for j in range(minimo +2, maximo + 1):
                        text += splitted[j] + ' '
            titulo_teste = text
            return titulo_teste

        # turno e curso retificado
        titulo = extrair_titulo(titulo_rasc_ver)

        #endregion

        #region Loop entre Todas as Páginas
        # relacao é uma lista que compila as relações de sala-hora para todas as páginas do PDF
        relacao = []

        #loop em todas as páginas
        for _ in range(len(paginas)):

            #region Extrair Informações do PDF
            # extrair tabela
            first_page = paginas[_]
            table = first_page.extract_table()

            # extrair aulas do dia indicado
            aulas = []
            for _ in range(1, len(table[:])):
                aulas.append(table[_][dias[dia_da_relacao]])

            # extrair apenas a sala e as horas
            salas_horas = []
            for item in aulas:
                if not item:
                    pass
                else:
                    # remover asteriscos
                    item = item.replace('*', '')

                    # para mais exclusões, editar aqui
                    if any([elem in item for elem in exclusoes]) and excluir:
                        pass
                    else:
                        time_room = item.split('/')[-1].strip()
                        if time_room[-1] == "-":
                            pass
                        else:
                            salas_horas.append(time_room)

            # separar as salas das horas
            salas_horas_sep = []
            for s in salas_horas:
                if not s:
                    salas_horas_sep.append(['', ''])
                else:
                    partes = re.split(r'\s*-\s*', s, 2)
                    if len(partes) >= 3:
                        time_part = ' - '.join(partes[:2])
                        classroom = partes[2].strip()
                        salas_horas_sep.append([classroom, time_part])
                    else:
                        salas_horas_sep.append(['', s])

            #endregion

            relacao.append(salas_horas_sep)

        # compilar as salas-horas para todas as páginas do pdf
        salas_horas_comp = [item for sublist in relacao for item in sublist]

        #region Ordenar a Relação de Salas-Horas
        # ordenar pelo horário de início e nome da sala
        # separar as horas e formatar em datetime
        def lista_tempo(lista):
            salas_horas_ini_fim = []
            for i in range(len(lista)):
                salas_horas_ini_fim.append(lista[i][1].split(' - '))
            salas_horas_i_f_datetime = []
            for item in salas_horas_ini_fim:
                temp = item[0].split(':')
                temp2 = item[1].split(':')
                salas_horas_i_f_datetime.append([temp, temp2])
            salas_horas_inicio = []
            for i in range(len(lista)):
                salas_horas_inicio.append([lista[i][0], [[time(int(salas_horas_i_f_datetime[i][0][0]), int(salas_horas_i_f_datetime[i][0][1]))],
                                                  [time(int(salas_horas_i_f_datetime[i][1][0]), int(salas_horas_i_f_datetime[i][1][1]))]]])
            return salas_horas_inicio

        # ordena as salas-horas conforme os tempos de início e números das salas
        def ordenar_key(item):
            room = item[0]
            time = item[1][0]
            match = re.search(r'\d+', room)
            numeric_part = int(match.group()) if match else 0
            return (time, numeric_part)

        salas_horas_ordenadas = sorted(lista_tempo(salas_horas_comp), key=ordenar_key)

        #endregion

        #region Formatar para Print
        # reformatar a lista - junta o tempo de início com o de término
        salas_horas_formatadas = []
        for item in salas_horas_ordenadas:
            room = item[0]
            start_time = item[1][0][0]
            end_time = item[1][1][0]

            formatted_time = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
            salas_horas_formatadas.append([room, formatted_time])

        # verificar quebras de linha na relação final de salas-horas
        salas_ver = [
            [element.replace('\n', ' ') for element in sublist]
            for sublist in salas_horas_formatadas
        ]

        #endregion

        #region Print
        # organização do texto para print
        texto = ''
        texto += titulo + '\n'
        try:
            tamanho_max = max(len(sublist[0]) for sublist in salas_ver)
            for item in salas_ver:
                diferenca = tamanho_max - len(item[0])
                texto += item[0] + ':   ' + diferenca*' ' + item[1] + '\n'
        except ValueError:
            for item in salas_ver:
                texto += item[0] + ':   ' + item[1] + '\n'

        # printa o texto com a relação de salas-horas
        print(texto)

        #endregion

        #endregion

#region Loop para Vários PDFs

#formatar o número dos PDFs
def formatar_num(num):
    if num < 10:
        return f'0{num}'
    elif 10 <= num < 100:
        return f'{num}'
    else:
        print("Número de PDFs < 100 somente!")

#loop para os pdfs
for i in range(1, num_pdfs + 1):
    #excluir as aulas de Núcleos de prática, estágios, para a Psicologia (pdfs 22-24)
    if i == 22:
        excluir = True
    elif i == 25:
        excluir = False

    relacao_salas_horas(caminho + f'{formatar_num(i)}.pdf', dia)

#endregion
