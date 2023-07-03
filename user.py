from flask import Flask, render_template, url_for, request, redirect,session, Blueprint

user_menu_bp = Blueprint('user',__name__,url_prefix='/menu')