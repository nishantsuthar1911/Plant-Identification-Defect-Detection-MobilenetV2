import os
from flask import jsonify
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from settings import UPLOAD_FOLDER, OBJECT_DETECTION_MODEL
from detector import DetectorTF2
from identify import prepare_input_data,return_image_batch, predict_from_model

from flask_cors import CORS
from detect_objects import extract_bbox
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

cors = CORS(app, resources={r"*": {"origins": "*"}})

detector = DetectorTF2(OBJECT_DETECTION_MODEL, "label_map.pbtxt", class_id=None, threshold=0.6)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            # return redirect(request.url)
            return jsonify({"status":"bad",
                "data":{
                "message":"No file found"}
            })
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({"status":"bad",
                "data":{
                "message":"No file found"}
            })
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if extract_bbox(detector,os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                image_data = prepare_input_data()
                image_batch = return_image_batch(image_data)
                plant_name,decease_name,remedies = predict_from_model(image_batch)
            # remove uploaded file
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return jsonify({"status":"ok",
                    "data":{
                    "plant":plant_name.replace("_"," ").strip(),
                    "health":decease_name.replace("_"," ").strip(),
                    "remedies":remedies}
                })
            else:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return jsonify({"status":"bad",
                "data":{
                "message":"Could Not Identify Plant"}
            })
        else:
            return jsonify({"status":"bad",
                "data":{
                "message":"Not Allowed File"}
            })
    else:
        return jsonify({"status":"bad",
                "data":{
                "message":"Only POST Method allowed"}
            })


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)