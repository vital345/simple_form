import secrets
import os
from PIL import Image
from flask import Flask, flash, redirect
from flask.helpers import url_for
from flask.json import jsonify
from flask.templating import render_template
from wtforms.validators import ValidationError
from forms import PersonalForm
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bgevgecewdgc0ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = '/static/images'
db = SQLAlchemy(app)


class D_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    position = db.Column(db.String(20))
    insta_id = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    image = db.Column(db.String(200),nullable=False, default='Default.jpeg')



# db.create_all()

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/', methods=['GET', 'POST'])
def home():
    form = PersonalForm()
    if form.validate_on_submit():
        name = D_model.query.filter_by(name=form.name.data).first()
        if not name:
            d_model = D_model(name=form.name.data, 
                                position=form.position.data,
                                insta_id=form.insta_id.data,
                                linkedin=form.linkedin.data,
                                github=form.github.data,
                                image='images/Default.jpeg')
            db.session.add(d_model)
            db.session.commit()
            if form.image.data:
                user = D_model.query.filter_by(name=form.name.data).first()
                user.image = f'images/{save_picture(form.image.data)}'
                db.session.commit()
            flash(f'the things are injected for {form.name.data}', 'success')
            return redirect(url_for('home'))
        else:
            raise ValidationError('That username is taken try another one!!!')
    return render_template('form.html', form = form)

@app.route('/data')
def get_data():
    data = D_model.query.all()
    output = []

    for people in data:
        people_data = {}
        people_data['name'] = people.name
        people_data['position'] = people.position
        people_data['insta_id'] = people.insta_id
        people_data['linkedin'] = people.linkedin
        people_data['github'] = people.github
        people_data['image'] = people.image
        output.append(people_data)
    
    return jsonify(output)




if __name__ == "__main__":
    app.run(debug=True)