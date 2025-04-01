import re
import pdfplumber
from datetime import time

excluir_nucleos = False

dias = {"SEGUNDA":1, "TERÇA":2, "QUARTA":3, "QUINTA":4, "SEXTA":5}

dias_inv = {v: k for k, v in dias.items()}

cursos = [
    'Administração',
    'Arte: História, Crítica e Curadoria'
    'Ciência da Computação',
    'Ciência de Dados e Inteligência Artificial',
    'Ciências Contábeis',
    'Ciências Sociais',
    'Comunicação das Artes do Corpo',
    'Comunicação e Multimeios',
    'Direito',
    'Filosofia',
    'Fisioterapia',
    'Fonoaudiologia',
    'História',
    'Jornalismo',
    'Letras',
    'Pedagogia',
    'Psicologia',
    'Publicidade e Propaganda',
    'Relações Internacionais',
    'Serviço Social'
]

turnos = ['MANHÃ', 'MAT', 'NOITE', 'NOT', 'VESP', 'VESP/MAT', 'VESP/NOT', 'MAT/VESP', 'NOT/VESP']

for k in range(1, 5):
    dia = dias_inv[k]
    print(dia)
    for i in range(1, 10):
        with pdfplumber.open(f"/home/xram/Desktop/COMORG/passagem de sala/0{i}.pdf") as pdf:
            #extrair paginas
            paginas = pdf.pages

            #extrair curso e turno
            titulo_rasc = paginas[0].extract_text()[190:254]

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

            titulo_rasc_ver = verificar_quebras(titulo_rasc)

            def extrair_titulo(titulo_teste):
                splitted = titulo_teste.split(' ')
                text = ''
                for i in range(len(splitted)):
                    if splitted[i] in turnos:
                        maximo = i
                        for j in range(maximo + 1):
                            text += splitted[j] + ' '
                titulo_teste = text
                return titulo_teste

            titulo = extrair_titulo(titulo_rasc_ver)

            #extrair aulas
            relatorio = []
            for _ in range(len(paginas)):

                #extrair tabela
                first_page = paginas[_]
                table = first_page.extract_table()

                #extrair aulas do dia indicado
                aulas = []
                for _ in range(1, len(table[:])):
                    aulas.append(table[_][dias[dia]])

                #extrair apenas a sala e as horas
                horas = []
                for item in aulas:
                    if not item:
                        pass
                    else:
                        if 'ÚCLEO' in item and excluir_nucleos:
                            pass
                        else:
                            time_room = item.split('/')[-1].strip()
                            if time_room[-1] == "-":
                                pass
                            else:
                                horas.append(time_room)

                #separar as salas das horas
                salas = []
                for s in horas:
                    if not s:
                        salas.append(['', ''])
                    else:
                        partes = re.split(r'\s*-\s*', s, 2)
                        if len(partes) >= 3:
                            time_part = ' - '.join(partes[:2])
                            classroom = partes[2].strip()
                            salas.append([classroom, time_part])
                        else:
                            salas.append(['', s])
                relatorio.append(salas)

            salas_comp = [item for sublist in relatorio for item in sublist]

            #ordenar pelo horário de início e nome da sala
            def lista_tempo(lista):
                hora = []
                for i in range(len(lista)):
                    hora.append(lista[i][1].split(' - '))
                hora_min = []
                for item in hora:
                    temp = item[0].split(':')
                    temp2 = item[1].split(':')
                    hora_min.append([temp, temp2])
                hora_inicio = []
                for i in range(len(lista)):
                    hora_inicio.append([lista[i][0], [[time(int(hora_min[i][0][0]), int(hora_min[i][0][1]))],
                                                      [time(int(hora_min[i][1][0]), int(hora_min[i][1][1]))]]])
                return hora_inicio

            def sort_key(item):
                room = item[0]
                time = item[1][0]
                # Extract the first numeric sequence in the room name [[9]][[10]]
                match = re.search(r'\d+', room)  # Find ANY digits, not just at the start
                numeric_part = int(match.group()) if match else 0  # Default to 0 if no digits
                return (time, numeric_part)

            salas_ordenadas = sorted(lista_tempo(salas_comp), key=sort_key)

            #reformatar a lista
            salas_ord = []
            for item in salas_ordenadas:
                room = item[0]
                start_time = item[1][0][0]  # First time in the first sublist [[1]]
                end_time = item[1][1][0]  # First time in the second sublist [[1]]

                # Format times as "HH:MM" [[2]]
                formatted_time = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                salas_ord.append([room, formatted_time])

            #verificar quebras de linha
            salas_ver = [
                [element.replace('\n', ' ') for element in sublist]
                for sublist in salas_ord
            ]

            #organização do texto
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

            print(texto)
    for i in range(10, 31):
        if i == 22:
            excluir_nucleos = True
        elif i == 25:
            excluir_nucleos = False
        with pdfplumber.open(f"/home/xram/Desktop/COMORG/passagem de sala/{i}.pdf") as pdf:
            # extrair paginas
            paginas = pdf.pages

            # extrair curso e turno
            titulo_rasc = paginas[0].extract_text()[190:254]


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
                            list.append(item[(ind + 1):])
                        elif conta == 2:
                            ind = item.index('\n')
                            list.append(item[:ind])
                            item2 = item[(ind + 1):]
                            ind2 = item2.index('\n')
                            list.append(item2[:ind2])
                            list.append(item2[(ind2 + 1):])
                    else:
                        list.append(item)
                for i in range(len(list)):
                    resultado += list[i] + ' '
                return resultado


            titulo_rasc_ver = verificar_quebras(titulo_rasc)


            def extrair_titulo(titulo_teste):
                splitted = titulo_teste.split(' ')
                text = ''
                for i in range(len(splitted)):
                    if splitted[i] in turnos:
                        maximo = i
                        for j in range(maximo + 1):
                            text += splitted[j] + ' '
                titulo_teste = text
                return titulo_teste


            titulo = extrair_titulo(titulo_rasc_ver)

            # extrair aulas
            relatorio = []
            for _ in range(len(paginas)):

                # extrair tabela
                first_page = paginas[_]
                table = first_page.extract_table()

                # extrair aulas do dia indicado
                aulas = []
                for _ in range(1, len(table[:])):
                    aulas.append(table[_][dias[dia]])

                # extrair apenas a sala e as horas
                horas = []
                for item in aulas:
                    if not item:
                        pass
                    else:
                        if 'ÚCLEO' in item and excluir_nucleos:
                            pass
                        else:
                            time_room = item.split('/')[-1].strip()
                            if time_room[-1] == "-":
                                pass
                            else:
                                horas.append(time_room)

                # separar as salas das horas
                salas = []
                for s in horas:
                    if not s:
                        salas.append(['', ''])
                    else:
                        partes = re.split(r'\s*-\s*', s, 2)
                        if len(partes) >= 3:
                            time_part = ' - '.join(partes[:2])
                            classroom = partes[2].strip()
                            salas.append([classroom, time_part])
                        else:
                            salas.append(['', s])
                relatorio.append(salas)

            salas_comp = [item for sublist in relatorio for item in sublist]

            # ordenar pelo horário de início e nome da sala
            def lista_tempo(lista):
                hora = []
                for i in range(len(lista)):
                    hora.append(lista[i][1].split(' - '))
                hora_min = []
                for item in hora:
                    temp = item[0].split(':')
                    temp2 = item[1].split(':')
                    hora_min.append([temp, temp2])
                hora_inicio = []
                for i in range(len(lista)):
                    hora_inicio.append([lista[i][0], [[time(int(hora_min[i][0][0]), int(hora_min[i][0][1]))],
                                                      [time(int(hora_min[i][1][0]), int(hora_min[i][1][1]))]]])
                return hora_inicio


            def sort_key(item):
                room = item[0]
                time = item[1][0]
                # Extract the first numeric sequence in the room name [[9]][[10]]
                match = re.search(r'\d+', room)  # Find ANY digits, not just at the start
                numeric_part = int(match.group()) if match else 0  # Default to 0 if no digits
                return (time, numeric_part)


            salas_ordenadas = sorted(lista_tempo(salas_comp), key=sort_key)

            # reformatar a lista
            salas_ord = []
            for item in salas_ordenadas:
                room = item[0]
                start_time = item[1][0][0]  # First time in the first sublist [[1]]
                end_time = item[1][1][0]  # First time in the second sublist [[1]]

                # Format times as "HH:MM" [[2]]
                formatted_time = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                salas_ord.append([room, formatted_time])

            # verificar quebras de linha
            salas_ver = [
                [element.replace('\n', ' ') for element in sublist]
                for sublist in salas_ord
            ]

            # organização do texto
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

            print(texto)