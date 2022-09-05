import sys
import random

articles = ["o", "a", "um", "uma", "os", "as", "uns", "umas"]
subjects = ["mulhres", "dinheiro", "whisky", "mulher", "bebado", "livro", "café", "padre", "jornal", "bar", "casa", "bicicleta", "caminhão", "ônibus", "avião", "navio","cigarro", "cachorro", "pássaro", "churrasco"]
verbs = ["bebe", "come", "dorme", "corre", "pula", "salta", "caminha", "anda", "voa", "nada", "pesca", "comprou", "vendeu", "fumou", "leu alto", "escreveu", "cantou", "dançou", "pinta", "desenha", "faz"]
adverbs = ["devagar", "rápido", "lentamente", "rapidamente", "depressa", "devagar", "lentamente", "rapidamente", "vagarosamente", "melancolicamente", "felizmente", "tristemente", "alegremente"]

sentence=[[articles,subjects,verbs,adverbs],[articles,subjects,verbs]]

lines = 9
if len(sys.argv) > 1:
        try:
                if 1 <= int(sys.argv[1]) <= 10:
                        lines = int(sys.argv[1])
        except ValueError as err:
                print(err)

while lines:
        sentence_type = sentence[random.randint(0,1)]
        line = ""
        column = 0
        while column < len(sentence_type):
                line += random.choice(sentence_type[column])
                line += " "
                column += 1
        print(line)
        lines -= 1