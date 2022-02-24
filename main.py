import os

from cv2 import FileStorage
from flask import url_for, Flask, request, redirect, flash, send_from_directory, send_file
UPLOAD_FOLDER = 'uploads'
from io import BytesIO
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
curr_file = [None]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            curr_file[0] =  BytesIO(file.stream.read())
            return '''
            <!doctype html>
            <title>Finished</title>
            <h1>Finished!</h1>
            <script> document.image_url ="''' + url_for('download_file', name=filename) + '''" </script>
            <img src=''' + url_for('download_file', name=filename) + ''' height=400> </img>
            <p> When finished, click this button </p>
            <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
            <script>
            document.corners = [];



            $('img').on('click', function(e) {
                e.preventDefault()
                document.corners.push(e)
                if (document.corners.length == 4){
                    res_str = ""
                    document.corners.forEach(corner=>{
                        res_str += corner.offsetX + "&" + corner.offsetY + "-"
                    })
                    $.getJSON('/submit/' + res_str,
                        function(data) {
                            //do nothing
                            console.log(data);
                        });
                }
                return false;
            });
            


            </script>
            <button type="button" onclick="">Submit</button>
            '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/current.jpeg')
def return_image():
    print(curr_file)

    return send_file(curr_file[0], download_name="current.jpeg")

@app.route('/submit/<string>')
def submit(string):
    print(string)
    return f"{string}"


if __name__ == "__main__":
    app.run(debug=True)
