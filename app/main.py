from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

ALUNOS = [{'matricula': 0, 'nome': 'Ana', 'nota': 72.00},
{'matricula': 1, 'nome': 'Bruna', 'nota': 71.50},
{'matricula': 2, 'nome': 'Carlos', 'nota': 68.50},
{'matricula': 3, 'nome': 'Diogo', 'nota': 70.00},
{'matricula': 4, 'nome': 'Ester', 'nota': 69.00}]

def aborta_se_o_aluno_nao_existe(matricula):
    encontrei = False
    for aluno in ALUNOS:

        if aluno['matricula'] == int(matricula):
            encontrei = True
    if encontrei == False:
        abort(404, mensagem="O aluno com matricula = {} não existe".format(matricula)) #404:Not Found

parser = reqparse.RequestParser()
parser.add_argument('matricula', type=int, help='matricula do aluno')
parser.add_argument('nome', type=str, help='nome do aluno')
parser.add_argument('nota', type=float, help='nota do aluno')


class Aluno(Resource):
    def get(self, matricula):
        aborta_se_o_aluno_nao_existe(matricula)
        return ALUNOS[int(matricula)]
    def delete(self, matricula):
        aborta_se_o_aluno_nao_existe(matricula)
        del ALUNOS[int(matricula)]
        return '', 204, #204: No Content
    def put(self, matricula):
        aborta_se_o_aluno_nao_existe(matricula)
        args = parser.parse_args()
        for aluno in ALUNOS:
            if aluno['matricula'] == int(matricula):
                aluno['matricula'] = args['matricula']
                aluno['nome'] = args['nome']
                aluno['nota'] = args['nota']
                break
        return aluno, 200, #200: OK

class ListaAluno(Resource):
    def get(self):
        return ALUNOS
    def post(self):
        args = parser.parse_args()
        matricula = -1
        for aluno in ALUNOS:
            if int(aluno['matricula']) > matricula:
                matricula = int(aluno['matricula'])
        matricula = matricula + 1
        aluno = {'matricula': matricula, 'nome': args['nome'], 'nota': args['nota']}
        ALUNOS.append(aluno)
        return aluno, 201, #201: Created

##
## Roteamento de recursos:
##
api.add_resource(Aluno, '/alunos/<matricula>')
api.add_resource(ListaAluno, '/alunos')

if __name__ == '__main__':
    app.run(debug=True)