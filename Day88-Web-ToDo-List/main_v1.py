from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor

app = Flask(__name__)
Bootstrap(app)

## Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
db = SQLAlchemy(app)

## Tasklist TABLE Configuration
class TaskList(db.Model):
    __tablename__ = "task_list"

    id = db.Column(db.Integer, primary_key=True)
    # task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))
    # task = relationship("Tasks", back_populates="items")
    name = db.Column(db.String(250), nullable=False)
    due_date = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    starred = db.Column(db.Boolean, nullable=False)
    tag = db.Column(db.Integer, nullable=True)


db.create_all()


@app.route("/")
def home():
    todo_list = db.session.query(TaskList).all()

    return render_template("index_v1.html", todo_list=todo_list)


@app.route("/add_item", methods=["POST"])
def addItem():
    # add new item
    new_item = TaskList(
        name=request.form.get("item_name"),
        due_date="",
        status=False,
        starred=False,
        tag=0
    )
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update_item", methods=["POST"])
def updateItem():
    todo_id = request.form.get("todo_id")
    todo = TaskList.query.filter_by(id=todo_id).first()
    todo.status = not todo.status
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/delete_item/<int:todo_id>")
def delete(todo_id):
    todo = TaskList.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)