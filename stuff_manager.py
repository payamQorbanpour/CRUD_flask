import os
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "stuff_db.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Stuff(db.Model):
    title = db.Column(db.String(80),
                      unique=True,
                      nullable=False,
                      primary_key=True)
    price = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.form:
        stuff = Stuff(title=request.form.get("title"), price=request.form.get("price"))
        db.session.add(stuff)
        db.session.commit()
    all_stuff = Stuff.query.all()
    return render_template('home.html', all_stuff=all_stuff)


@app.route('/update', methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    stuff = Stuff.query.filter_by(title=oldtitle).first()
    stuff.title = newtitle
    db.session.commit()
    return redirect("/")


@app.route('/delete', methods=['POST'])
def delete():
    title = request.form.get("title")
    stuff = Stuff.query.filter_by(title=title).first()
    db.session.delete(stuff)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
