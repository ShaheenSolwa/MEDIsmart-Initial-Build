########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import redirect,Blueprint, render_template, url_for, flash, request
from flask_login import login_required, current_user
from __init__ import create_app, db
from werkzeug.utils import secure_filename
import os

########################################################################################
# our main blueprint
main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('About.html')

@main.route('/') # profile page that return 'profile'
@login_required
def profile():
    return render_template('index.html')

@main.route('/pricing')
def Pricing():
    return render_template('pricing.html')

@main.route('/contribute')
def Contribute():
    return render_template('contribute.html')

@main.route('/contribute', methods=['POST'])
def uploadContributions():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+'/contributions', filename))
            # print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')
            return render_template('contribute.html', filename=filename)
        else:
            flash('Allowed image types are -> png, jpg, jpeg')
            return redirect(request.url)

@main.route('/contribute/display/<filename>')
def display_image2(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename=app.config['UPLOAD_FOLDER']+'/contributions/' + filename), code=301)

@main.route('/predict', methods=['POST'])
def uploaded():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')
            return render_template('predict.html', filename=filename)
        else:
            flash('Allowed image types are -> png, jpg, jpeg')
            return redirect(request.url)

@main.route('/predict/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    #select = request.form.get('tools')
    #print(select)
    return render_template('predict.html')


app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode