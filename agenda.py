import sys
from typing import List
from typing import Tuple

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'


class Compromisso:
  def __init__(self, desc, data, hora, pri, contexto, projeto):
    self.desc = desc
    self.data = data
    self.hora = hora
    self.pri = pri
    self.contexto = contexto
    self.projeto = projeto

itens = Compromisso('Fazendo crochê', '24082020', '1956', '(A)', '@Casa', '+VIDA')
# print(itens.data)

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais podem ser implementados como uma tupla, dicionário  ou objeto. A função
# recebe esse item através do parâmetro extras.
#
# extras tem como elementos data, hora, prioridade, contexto, projeto
#
def adicionar(descricao:str, extras:Tuple):
  if descricao == ' ':
      return False
  else:
      if dataValida(extras[0]) and horaValida(extras[1]) and prioridadeValida(extras[2]) and contextoValido(extras[3]) and projetoValido(extras[4]):
          return True

  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False
  finally:
    fp.close()


  return True


# Valida a prioridade.
def prioridadeValida(pri:str):
  if len(pri) == 3 and pri[0] == '(' and pri[2] == ')' and (
          pri[1] >= 'A' or pri[1] <= 'Z' or pri[1] >= 'a' or pri[1] <= 'z'):
    return True
  return False


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin:str):
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    h = int(horaMin[0] + horaMin[1])
    m = int(horaMin[2] + horaMin[3])
    if h >= 00 and h <= 23 and m >= 00 and m <= 59:
      return True
    else:
      return False


# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data:str):
  if len(data) != 8 or not soDigitos(data):
    return False
  dia = data[0] + data[1]
  mes = data[2] + data[3]
  ano = data[4] + data[5] + data[6] + data[6]
  if dia < '01' or dia > '31' or mes < '01' or mes > '12' or len(ano) != 4:
    return False
  else:
    if dia <= '31' and (
            mes == '01' or mes == '03' or mes == '05' or mes == '07' or mes == '08' or mes == '10' or mes == '12'):
      return True
    elif dia <= '30' and (mes == '04' or mes == '06' or mes == '09' or mes == '11'):
      return True
    elif dia <= '29' and mes == '02':
      return True
    else:
      return False


# Valida que o string do projeto está no formato correto.
def projetoValido(proj:str):
  if len(proj) >= 2 and proj[0] == '+':
    return True
  return False


# Valida que o string do contexto está no formato correto.
def contextoValido(cont:str):
  if len(cont) >= 2 and cont[0] == '@':
    return True
  return False


# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero):
  if type(numero) != str:
    return False
  for x in numero:
    if x < '0' or x > '9':
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas:List):
  while linhas[3] == ' ':
    break
  else:
    itens = []
    for l in linhas:
      if dataValida(linhas[0]) and horaValida(linhas[1]) and prioridadeValida(linhas[2]) and contextoValido(linhas[4]) and projetoValido(linhas[5]):
        data = linhas[0].strip()
        linhas.pop(0)
        hora = linhas[0].strip()
        linhas.pop(0)
        pri = linhas[0].strip()
        linhas.pop(0)
        desc = linhas[0].strip()
        contexto = linhas[1].strip()
        linhas.pop(1)
        projeto = linhas[1].strip()
        linhas.pop(1)
        descricao = str(desc).strip()
        itens.append(descricao)
        extras = (data, hora, pri, contexto, projeto)
        itens.append(extras)
        return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():


listar()


def ordenarPorDataHora(itens):

  ################ COMPLETAR

  return itens
   
def ordenarPorPrioridade(itens):

  ################ COMPLETAR

  return itens

def fazer(num):

  ################ COMPLETAR

  return 

def remover():

  ################ COMPLETAR

  return

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):

  ################ COMPLETAR

  return 

def desenhar(dias): 

  ################ COMPLETAR
  
  return



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos):
  if comando[3] == ' ':
    return
  else:
    if dataValida(comandos[2].strip()) and horaValida(comandos[3].strip()) and prioridadeValida(comandos[4].strip()) and contextoValido(comandos[6].strip()) and projetoValido(comandos[7].strip()):
      if comandos[1] == ADICIONAR:
        comandos.pop(0) # remove 'agenda.py'
        comandos.pop(0) # remove 'adicionar'
        itemParaAdicionar = organizar([' '.join(comandos)])[0]
        # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
        adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
      elif comandos[1] == LISTAR:
        return
        ################ COMPLETAR

      elif comandos[1] == REMOVER:

        ################ COMPLETAR

      elif comandos[1] == FAZER:
        return

        ################ COMPLETAR

      elif comandos[1] == PRIORIZAR:
        return

        ################ COMPLETAR

      else :
        print("Comando inválido.")


# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
