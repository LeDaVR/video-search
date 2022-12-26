from flask import Flask, render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename, send_from_directory
import firebase_admin
from firebase_admin import firestore


app = Flask(__name__)
firebaseapp = firebase_admin.initialize_app()
db = firestore.client()


@app.route("/",methods=['GET','POST'])
def index():

    if request.method == 'GET':
        query = []
        return render_template("youtube.html",query = query)

    if request.method == 'POST':
        busqueda = request.form['busqueda']
        tags = busqueda.split(' ')
        ## AGREGAR QUERY
        query = buscar(tags)
        return render_template('youtube.html',query = query)

def buscar(tags):
    videos_data = db.collection(u'video-data')
    query = videos_data.where(u'tag', u'in' , tags)
    results = query.stream()

    results_array = []
    for doc in results:
        results_array += [
            {
                'image_url' : 'https://storage.googleapis.com/thumbnail-bucket-322/'+doc.get('thumbnail'),
                'video_url' : doc.id
            }
        ]

    return results_array

@app.route("/watch/<id>",methods=['GET','POST'])
def watch(id):
    print("INDEX")
    if request.method == 'GET':
        request.args.get('url')
        ## Obtener video
        print('url')
        videos_data = db.collection(u'video-data').document(id)
        url = videos_data.get().to_dict()['url']
        # HACER QUERY
        return render_template("watch.html",url = url)

    print("INDEX POST")
    if request.method == 'POST':
        busqueda = request.form['busqueda']
        tags = busqueda.split(' ')
        ## AGREGAR QUERY
        query = buscar(tags)
        return render_template('youtube.html',query = query)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)