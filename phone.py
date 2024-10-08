from flask import Flask, request

import os

from dotenv import load_dotenv
load_dotenv()
print(os.environ['TESTER'])