from flask import Flask, request, render_template, Blueprint, url_for, redirect

main_routes=Blueprint('main',__name__)

@main_routes.route('/', methods=['GET','POST'])

def login():
    return render_template('login.html')