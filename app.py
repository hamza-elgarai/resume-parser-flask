from flask import Flask, flash, request, redirect, url_for
from flask_cors import CORS,cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
import os
import resume_parser_v2
@app.route('/hello')
@cross_origin()
def hello():
    return 'Hello, World!'
@app.route('/upload',methods=['POST'])
@cross_origin() 
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        new_path = os.path.join('./', file.filename)
        file.save(new_path)
        response = resume_parser_v2.extract_all_data(new_path)
        try:
            os.remove(new_path)
        except:
            pass
        return response
    return 'Please upload your file'


if __name__ == "__main__":
    app.run()
