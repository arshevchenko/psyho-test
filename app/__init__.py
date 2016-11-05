from flask import Flask
import rsa

app = Flask(__name__)
(public_key, private_key) = rsa.newkeys(512)

from app import views
from app import api
