from flask import Flask, render_template, request, session, url_for, redirect


app = Flask(__name__)

# Chave secreta para usar sessões
app.secret_key = 'projeto147'  # Substitua por uma chave segura

# Lista de tópicos atualizada (5 tópicos)
topics = [
    {"name": "Condições e Meio Ambiente de Trabalho na Indústria da Construção", "url": "/conditions"},
    {"name": "Equipamentos de Proteção Individual (EPIs)", "url": "/epis"},
    {"name": "Trabalho em Altura", "url": "/height"},
    {"name": "Segurança em Instalações e Serviços em Eletricidade", "url": "/electricity"},
    {"name": "Segurança no Trabalho em Máquinas e Equipamentos", "url": "/machines"}
]

# Perguntas do quiz (placeholder, serão substituídas por você)
quiz_questions = [
    {
        "text": "Pergunta sobre Condições (NR-18): O que é obrigatório no canteiro de obras?",
        "options": ["Água potável", "Música alta", "Nenhum EPI", "Falta de iluminação"],
        "correct_answer": 0
    },
    {
        "text": "Sobre os EPIs, qual das alternativas abaixo representa uma responsabilidade exclusiva do empregador, segundo a NR-6?",
        "options": ["Exigir que o trabalhador guarde o EPI ao final do expediente", "Fiscalizar o uso correto dos EPIs e fornecer substituições sempre que necessário", "Comunicar ao SESMT quando um EPI for danificado", "Devolver o EPI ao final de cada semana para higienização coletiva"],
        "correct_answer": 1
    },
    {
        "text": "Qual é a altura mínima para um trabalho ser considerado em altura, conforme a NR-35?",
        "options": ["1 metro", "2 metros", "5 metros", "10 metros"],
        "correct_answer": 1
    },
    {
        "text": "Segundo a NR-10, qual é a medida prioritária ao trabalhar com eletricidade?",
        "options": ["Uso de ferramentas com isolamento", "Treinamento com 40 horas de duração", "Manutenção preventiva da rede", "Desenergização da instalação"],
        "correct_answer": 3
    },
    {
        "text": "De acordo com a NR-12, qual das opções abaixo é considerada um dispositivo de segurança obrigatório em máquinas?",
        "options": ["Tela de proteção facial do trabalhador", "Sinal sonoro de início de jornada", "Dispositivo de parada de emergência em local de fácil acesso", "Manual de operação plastificado preso à máquina"],
        "correct_answer": 2
    }
]



@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/summary')
def summary():
    return render_template('summary.html', topics=topics)

@app.route('/conditions')
def conditions():
    return render_template('conditions.html')

@app.route('/epis')
def epis():
    return render_template('epis.html')

@app.route('/height')
def height():
    return render_template('height.html')

@app.route('/electricity')
def electricity():
    return render_template('electricity.html')

@app.route('/machines')
def machines():
    return render_template('machines.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # Inicializar a sessão do quiz
    if 'quiz_answers' not in session:
        session['quiz_answers'] = []
        session['current_question_index'] = 0

    total_questions = len(quiz_questions)

    # Verificar se o quiz foi concluído
    if session['current_question_index'] >= total_questions:
        # Calcular a pontuação
        score = 0
        answers = []
        for i, user_answer in enumerate(session['quiz_answers']):
            correct_answer = quiz_questions[i]['correct_answer']
            if user_answer == correct_answer:
                score += 1
            answers.append((quiz_questions[i], user_answer, correct_answer))

        # Resetar a sessão para permitir novo quiz
        session.pop('quiz_answers', None)
        session.pop('current_question_index', None)

        return render_template('quiz.html', quiz_completed=True, score=score, total_questions=total_questions, answers=answers)

    # Mostrar a pergunta atual
    current_question_index = session['current_question_index']
    current_question = quiz_questions[current_question_index]

    if request.method == 'POST':
        # Salvar a resposta do usuário
        user_answer = int(request.form['answer'])
        session['quiz_answers'].append(user_answer)
        session['current_question_index'] += 1
        session.modified = True
        return redirect(url_for('quiz'))

    return render_template('quiz.html', quiz_completed=False, current_question=current_question, current_question_index=current_question_index)


if __name__ == '__main__':
    app.run(debug=True)