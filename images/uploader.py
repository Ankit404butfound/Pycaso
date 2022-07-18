from flask import *  
app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return """<html>  
<head>  
    <title>upload</title>  
</head>  
<body>  
    <form action = "/success" method = "post" enctype="multipart/form-data">  
        <input type="file" name="file" />  
        <input type = "submit" value="Upload">  
    </form>  
</body>  
</html>  """ 
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        return "success"  
  
if __name__ == '__main__':  
    app.run("0.0.0.0", debug = True)  
