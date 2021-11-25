from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
#Habilitando el uso del ORM en la app flask mediante el objeto "db"
db = SQLAlchemy(app)

#postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ykzkzpgmvzkpby:c21aa599196bc30fb6be66b0bedee674544de5e059248eb74ce3d2dd7234d1ea@ec2-52-86-193-24.compute-1.amazonaws.com:5432/d2gso1vmakss48'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Notas(db.Model):
    '''Clase Notas'''
    __tablename__ = "notas"
    idNota = db.Column(db.Integer, primary_key = True)
    tituloNota = db.Column(db.String(80))
    cuerpoNota = db.Column(db.String(150))

    def __init__(self, tituloNota, cuerpoNota):
        self.tituloNota = tituloNota
        self.cuerpoNota = cuerpoNota

@app.route('/')#Te manda hasta la raiz del navegador
def index():
    objeto = {"nombre": "Tairi",
              "apellido": "Jaimes"
             }
    nombre = "Tairi"
    lista_nombres = ["Daniela", "Juan", "Raquel"]
    return render_template("index.html", variable = lista_nombres )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/acercademi")
def acercademi():
    return render_template("acercademi.html")

@app.route("/crearnota", methods=['POST'])
def crearnota():
    campotitulo = request.form["campotitulo"]
    campocuerpo = request.form["campocuerpo"]
    print(campotitulo)
    print(campocuerpo)
    notaNueva = Notas(tituloNota=campotitulo,cuerpoNota=campocuerpo)
    db.session.add(notaNueva)
    db.session.commit()

    return redirect ("/leernotas")

@app.route("/leernotas")
def leernotas():
    consulta_notas = Notas.query.all()
    print(consulta_notas)
    for nota in consulta_notas:
        titulo = nota.tituloNota
        cuerpo = nota.cuerpoNota
        print(nota.tituloNota)
        print(nota.cuerpoNota)
        
    #return "Notas Consultadas"
    return render_template("leerNotas.html", consulta = consulta_notas)

@app.route("/eliminarnota/<id>")
def eliminar(id):
    nota = Notas.query.filter_by(idNota=int(id)).delete()
    print(nota)
    db.session.commit()
    return redirect ("/leernotas")

@app.route("/editarnota/<id>")
def editar(id):
    nota = Notas.query.filter_by(idNota=int(id)).first()
    print(nota)
    print(nota.tituloNota)
    print(nota.cuerpoNota)
    return render_template("modificarNota.html", nota = nota)

@app.route("/modificarnota", methods=['POST'])
def modificarnota():
    idnota = request.form['idnota']
    nuevo_titulo = request.form['campotitulo']
    nuevo_cuerpo = request.form['campocuerpo']
    nota = Notas.query.filter_by(idNota=int(idnota)).first()
    nota.tituloNota = nuevo_titulo
    nota.cuerpoNota = nuevo_cuerpo
    db.session.commit()
    return redirect ("/leernotas")

if __name__ == "__main__":
    db.create_all()
    app.run()
