import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return render_template("calculator.html")
    else:
        return render_template("index.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method=="POST":
        height=request.form.get("height")
        weight=request.form.get("weight")
        sys=request.form.get("radios")
        if not height:
            return render_template("error.html",error="Enter the height!")
        if not weight:
            return render_template("error.html",error="Enter the weight!")
        try:
            height=float(height)
            weight=float(weight)
        except ValueError:
            return render_template("error.html",error="Please enter numeric data only")

        if sys=="metric":
            BMIn = weight / (height/100)**2
        else:
             BMIn = (weight / (height)**2)*703
        BMIn=round(BMIn,2)
        if BMIn <= 18.4:
            msg=("you are underweight.")
        elif BMIn <= 24.9:
            msg=("you are healthy.")
        elif BMIn <= 29.9:
            msg=("you are over weight.")
        elif BMIn <= 34.9:
            msg=("you are severely over weight.")
        elif BMIn <= 39.9:
            msg=("you are obese.")
        else:
            msg=("you are severely obese.")
        return render_template("result.html",BMIn=BMIn,msg=msg)
    else:
        return render_template("calculator.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        return redirect("calculator.html")
    else:
        return render_template("result.html")
@app.route("/error", methods=["GET", "POST"])
def error():
    return render_template("error.html", error="Unauthorised Access")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',error="Page not found! 404"),404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',error="Internal error detected! 500"),500


