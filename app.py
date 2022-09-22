from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
import config
app = Flask(__name__)


app.config['S3_KEY'] = config.s3_key
app.config['S3_SECRET'] = config.s3_secret_key


s3_client = boto3.client('s3', aws_access_key_id=app.config['S3_KEY'], aws_secret_access_key=app.config['S3_SECRET'])


@app.route('/')
def hello():
   return "Hello World"

@app.route('/', methods = ["POST"])
def upload_file():
   file = request.files['file']
   filename = secure_filename(file.filename)
   file.save(filename)
   bucket = request.form['bucket']
   try:
      s3_client.upload_file(filename, bucket, filename)
   except ClientError as e:
      return jsonify(error=400, text=str(e)), 400
   return jsonify(msg="File uploaded successfully"), 201

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)