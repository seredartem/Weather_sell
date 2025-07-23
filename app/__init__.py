from flask import Flask, Blueprint
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
