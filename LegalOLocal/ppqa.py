

from paperqa import Docs
my_docs = ["/home/zoroastro/Downloads/CONTRATO-DE-ARRENDAMIENTO(1).pdf"]


docs = Docs()
for d in my_docs:
    docs.add(d)

answer = docs.query("What manufacturing challenges are unique to bispecific antibodies?")
print(answer.formatted_answer)