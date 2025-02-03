# PCB-Defect-Detection

## Abstract
PCB-Defect-Detection is a Flask-based web application designed for identifying defects in printed circuit boards (PCBs) using MATLAB for advanced image processing. The application facilitates seamless integration of Python and MATLAB, allowing users to upload PCB images, perform defect detection through multiple image processing steps, and visualize intermediate outputs.

The solution is especially useful for industries requiring automated quality checks on PCBs. It employs preprocessing techniques, edge detection, morphological operations, and connected component analysis to detect and report defects.

---

## Steps to Use
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd PCB-Defect-Detection
   ```
2. Install the required Python packages:
   ```bash
   pip install flask
   ```

3. Ensure MATLAB is installed on your system and the MATLAB Engine API for Python is set up. For MATLAB engine support, ensure you are using **Python 3.9**, **3.10**, or **3.11**.

4. Start the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000/`.

6. Upload an image of a PCB to detect defects. The application will display:
   - A step-by-step report of the image processing operations.
   - Intermediate images showing each stage of defect detection.
   - Final annotated output with defect markings.

---

## Packages Required
- Python:
  - `flask`
  - MATLAB Engine API for Python (pre-installed with MATLAB; refer to MATLAB's documentation for setup instructions).

---

## MATLAB Compatibility Note
The MATLAB Engine API for Python requires strict version compatibility. Ensure that your Python version is one of the following:
- Python **3.9**
- Python **3.10**
- Python **3.11**

Attempting to use unsupported Python versions may result in runtime errors or engine initialization failures.

---

## File Descriptions
### Python
- **app.py**: The main Flask application to handle file uploads, interact with MATLAB, and render results.

### MATLAB
- **pcb_defect.M**: MATLAB script that performs defect detection, including preprocessing, thresholding, edge detection, and defect analysis.

---

## Directory Structure
```
PCB-Defect-Detection/
├── app.py                    # Flask application
├── static/
│   ├── uploads/              # Folder for uploaded files
│   └── results/              # Folder for output and intermediate results
├── templates/
│   ├── index.html            # Home page template
│   ├── results.html          # Results display template
└── pcb_defect.M              # MATLAB script for defect detection
```

---

## Contributions
Feel free to submit issues or pull requests to improve this project!
