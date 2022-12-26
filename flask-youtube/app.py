from flask import Flask, render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename, send_from_directory
import firebase_admin
from firebase_admin import firestore


app = Flask(__name__)
firebaseapp = firebase_admin.initialize_app()
db = firestore.client()


@app.route("/",methods=['GET','POST'])
def index(): # post
    print("INDEX")
    if request.method == 'GET':
        return render_template("youtube.html")

    print("INDEX POST")
    if request.method == 'POST':
        print("INDEX POST inside")
        correo = request.form['busqueda']
        print(correo)
        ## AGREGAR QUERY
        query = buscar()
        print(query)
        return render_template('search.html',query = query)
    return render_template('youtube.html')

def buscar(query = [["Nombre Video","URL","""data:image/jpeg;base64,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"""]]):
    res = list(query)
    for i in range(4):
        res.append(["Nombre #"+str(i),"URL", res[0][2]])
    return res

def getVideo(query = [["Nombre Video","https://storage.cloud.google.com/video-bucket-322/video.mp4"]]):
    res = list(query)
    for item in range(5):
        res.append(query[0])
    return res

@app.route("/test")
def test():
    girrages = db.collection(u'giraffe')
    query = girrages.where(u'url', u'in' , ['https://storage.googleapis.com/video-bucket-322/giraffes_1280p.mp4','sdfgadasd'])
    a = query.stream()
    print(a)
    for doc in a:
        print(doc.get('url'))
    return "good"

@app.route("/search",methods=['GET','POST'])
def search():
    print("INDEX")
    if request.method == 'GET':
        return render_template("search.html")

    print("INDEX POST")
    if request.method == 'POST':
        print("INDEX POST inside")
        correo = request.form['busqueda']
        print(correo)
        query = buscar(correo)
        
        return render_template('search.html',query = query)
    return render_template('youtube.html')

@app.route("/watch",methods=['GET','POST'])
def watch():
    print("INDEX")
    if request.method == 'GET':
        request.args.get('url')
        ## Obtener video
        print('url')
        query = getVideo()
        nombre = "name video"
        # HACER QUERY
        return render_template("watch.html",query = query,nombre = nombre)

    print("INDEX POST")
    if request.method == 'POST':
        #MANDARME AL SEARCH
        
        return render_template('search.html',pedido = query)
    return render_template('youtube.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)