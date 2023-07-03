## dead end! flask_uploads is an old extension see uploads folder

from flask import Blueprint
#from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from flask_uploads import UploadSet, configure_uploads, IMAGES
route_blueprint = Blueprint('route_blueprint', __name__)

@route_blueprint.route('/upload/files', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        rec = Photo(filename=filename, user=g.user.id)
        rec.store()
        flash("Photo saved.")
        return redirect(url_for('show', id=rec.id))
    return render_template('upload.html')

@route_blueprint.route('/upload/photo/<id>')
def show(id):
    photo = Photo.load(id)
    if photo is None:
        abort(404)
    url = photos.url(photo.filename)
    return render_template('show.html', url=url, photo=photo)

@route_blueprint.route('/upload')
def index():
     return "Hello"
