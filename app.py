from flask import Flask, request, render_template, redirect, url_for
import os
import matlab.engine

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Start MATLAB engine
eng = matlab.engine.start_matlab()
eng.addpath(r'D:\B-Tech{PC}\SEM-V\7-1-DIGITAL IMAGE PROCESSING\PCBDefect-main', nargout=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        output_path = os.path.join(RESULT_FOLDER, 'output_' + file.filename)

        # Call MATLAB function and capture intermediate outputs
        defect_report, steps, image_paths = eng.detect_pcb(input_path, output_path, nargout=3)

        # Render images
        return render_template('results.html', 
                               defect_report=defect_report, 
                               steps=steps, 
                               image_paths=image_paths)

if __name__ == '__main__':
    app.run(debug=True)
