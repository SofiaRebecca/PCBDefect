import os
from flask import Flask, request, render_template, redirect, url_for
import matlab.engine
from detect_defects import detect_and_draw  # Your Python detection function

app = Flask(__name__)

# Set up upload and result folders
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Configure the app to use static folders
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Start MATLAB engine
eng = matlab.engine.start_matlab()
eng.addpath(r'C:\Users\sofia\PCBDefect', nargout=0)  # Correct path to your project folder

@app.route('/')
def index():
    return render_template('index.html')  # HTML file for the home page

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the file is present
    if 'file' not in request.files or request.files['file'].filename == '':
        print("No file selected.")
        return redirect(url_for('index'))

    file = request.files['file']
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(input_path)

    output_path = os.path.join(app.config['RESULT_FOLDER'], 'output_' + file.filename)

    try:
        # Call Python function to detect defects using YOLO model
        bboxes, class_labels = detect_and_draw(
            model_path="C:/Users/sofia/PCBDefect/yolov5/runs/train/exp3/weights/best.pt",
            input_image_path=input_path,
            output_image_path=output_path
        )

        if len(bboxes) == 0:
            print("No bounding boxes detected.")  # Log if no bounding boxes detected

        # Convert bounding boxes and class labels to MATLAB-friendly format
        bboxes_matlab = matlab.double([list(map(float, bbox)) for bbox in bboxes])  # Ensure correct MATLAB format
        class_labels_matlab = matlab.double([float(label) for label in class_labels])  # Use MATLAB double instead of cell

        # Call MATLAB function to process results (e.g., generate report)
        defect_report, steps, image_paths = eng.detect_pcb(
            input_path,
            output_path,
            bboxes_matlab,
            class_labels_matlab,
            nargout=3
        )

        defect_report = list(defect_report)
        steps = list(steps)
        image_paths = [str(img) for img in image_paths]

        return render_template(
            'results.html',
            defect_report=defect_report,
            steps=steps,
            image_paths=image_paths
        )
    except Exception as e:
        print(f"Error during processing: {e}")
        return render_template('error.html', message="An error occurred during processing.")

if __name__ == '__main__':
    app.run(debug=True)