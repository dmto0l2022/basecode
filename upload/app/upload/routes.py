from flask import Blueprint
from flask import current_app

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from datetime import datetime



UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

upload_page_bp = Blueprint('upload_page_bp', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_page_bp.route('/app/upload/files', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        now = datetime.now()
        iso_date = now.strftime('%Y%m%d%H%M%S%f')
        extension = file.filename.rsplit('.', 1)[1].lower()
        newfolder = iso_date
        newfilename = 'data.' + extension
        path2folder = os.path.join(current_app.config['UPLOAD_FOLDER'], newfolder)
        print(path2folder)
        print(newfilename)
        fullfilepath = os.path.join(path2folder, newfilename)
        print(fullfilepath)
        try:
            os.makedirs(path2folder)    
        except FileExistsError:
            print("Directory " , path2folder ,  " already exists")  
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            file.save(fullfilepath)
            ##return redirect(url_for('download_file', name=filename))
    return render_template('upload.html')

'''
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
'''

@upload_page_bp.route('/app/upload')
def index():
     return "Hello"
