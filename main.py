from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
from os import environ
from flask_bootstrap import Bootstrap
import time

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
Bootstrap(app)


class CommentForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={"placeholder": "Your name"})
    email = StringField(validators=[DataRequired(), Email(message="The email you entered was not valid")], render_kw={"placeholder": "Your Email"})
    subject = StringField(render_kw={"placeholder": "Subject"})
    message = StringField(validators=[DataRequired()], render_kw={"placeholder": "Your message"})
    submit_btn = SubmitField("Send message")


@app.route("/", methods=["GET", "POST"])
def home():
    form = CommentForm()
    if form.validate_on_submit():
        flash("Successfully sent message!")
        return redirect(url_for("home"))

    return render_template("index.html", form=form)


if __name__ == '__main__':
    app.run()
