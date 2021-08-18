from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
from os import environ
from flask_bootstrap import Bootstrap
import smtplib

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
Bootstrap(app)

EMAIL = environ.get("USER_EMAIL")
PASSWORD = environ.get("PASSWORD")


class CommentForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={"placeholder": "Your name"})
    email = StringField(validators=[DataRequired(), Email(message="The email you entered was not valid")],
                        render_kw={"placeholder": "Your Email"})
    subject = StringField(render_kw={"placeholder": "Subject"})
    message = StringField(validators=[DataRequired()], render_kw={"placeholder": "Your message"})
    submit_btn = SubmitField("Send message")


@app.route("/", methods=["GET", "POST"])
def home():
    form = CommentForm()
    if form.validate_on_submit():
        with smtplib.SMTP_SSL("smtp.gmail.com", port=465) as connection:
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=f"Subject: New Form Response \n\n"
                    f"Person's name: {form.name.data}\n"
                    f"Person's email: {form.email.data}\n"
                    f"Subject: {form.subject.data}\n"
                    f"Message: {form.message.data}"
            )
        flash("Successfully sent message!")
        return redirect(url_for("home"))

    return render_template("index.html", form=form)


if __name__ == '__main__':
    app.run()
