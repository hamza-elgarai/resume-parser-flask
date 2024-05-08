app = Flask(__name__)
import os
import resume_parser
from flask import Flask, flash, request, redirect, url_for
@app.route('/hello')
def hello():
    return 'Hello, World!'
@app.route('/upload',methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        new_path = os.path.join('./', file.filename)
        file.save(new_path)
        return resume_parser.extract_all_data(new_path)
    return 'Please upload your file'


if __name__ == "__main__":
    app.run()
