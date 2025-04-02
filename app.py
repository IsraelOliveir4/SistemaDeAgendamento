from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)

# Modelo de Agendamento
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    servico = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    horario = db.Column(db.String(5), nullable=False)

# Criar o banco de dados
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    agendamentos = Agendamento.query.all()
    return render_template("index.html", agendamentos=agendamentos)

# Criar novo agendamento
@app.route("/novo", methods=["GET", "POST"])
def novo_agendamento():
    print("Rota /novo foi chamada!")  # <- Depuração
    if request.method == "POST":
        cliente = request.form["cliente"]
        servico = request.form["servico"]
        data = request.form["data"]
        horario = request.form["horario"]

        novo = Agendamento(cliente=cliente, servico=servico, data=data, horario=horario)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("novo.html")

# Editar um agendamento
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    if request.method == "POST":
        agendamento.cliente = request.form["cliente"]
        agendamento.servico = request.form["servico"]
        agendamento.data = request.form["data"]
        agendamento.horario = request.form["horario"]
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("editar.html", agendamento=agendamento)

# Excluir um agendamento
@app.route("/excluir/<int:id>")
def excluir_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    db.session.delete(agendamento)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)