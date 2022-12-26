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
        busqueda = request.form['busqueda']
        tags = busqueda.split(' ')
        ## AGREGAR QUERY
        query = buscar(tags)
        return render_template('search.html',query = query)
    return render_template('youtube.html')

def buscar(tags):
    videos_data = db.collection(u'video-data')
    query = videos_data.where(u'tag', u'in' , tags)
    results = query.stream()

    results_array = []
    for doc in results:
        results_array += [
            {
                'image_url' : 'https://storage.googleapis.com/thumbnail-bucket-322/'+doc.get('thumbnail'),
                'video_url' : doc.get('url')
            }
        ]
    

    return results_array

def getVideo(query = [["Nombre Video","https://storage.cloud.google.com/video-bucket-322/video.mp4"]]):
    res = list(query)
    for item in range(5):
        res.append(query[0])
    return res

@app.route("/test")
def test():
    videos_data = db.collection(u'video-data')
    query = videos_data.where(u'tag', u'in' , ['giraffe','sdfgadasd'])
    results = query.stream()
    urls = ""

    for doc in results:
        urls += doc.get('url')
    

    return urls

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
    app.run(host="0.0.0.0", port=8080, debug=True)