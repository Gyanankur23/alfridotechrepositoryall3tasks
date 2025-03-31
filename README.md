IOOS Tool Data Interface

Description
  
This project is part of the Google Summer of Code 2025 initiative, aimed at contributing to the IOOS (Integrated Ocean Observing System) by developing web-based user interfaces for their tools. Using Python, Pyodide, Pyscript, HTML, CSS, and JavaScript, this solution streamlines data management, quality control, and user engagement.

The interface allows users to: 
 
- Upload datasets in CSV format.  

- Preview the uploaded dataset in a table format.  

- Perform Quality Control (QC) checks using IOOS tools like ioos-qc.

This repository includes fully functional code files along with instructions on how to use them effectively.

Project Details  

Title: Build Web UI Versions Using Pyodide/Pyscript for IOOS Tools  

Contributor: Gyanankur Baruah 
 
Technologies Used: Python, Pyodide, Pyscript, HTML, CSS, JavaScript, and IOOS tools.  

Purpose: To enhance accessibility and usability of IOOS data validation tools through interactive web interfaces.

File Structure  

IOOS.html: The main HTML file for the web interface.  

IOOS.css: The CSS file for styling the interface.  

IOOS.js: JavaScript file for handling dataset uploads and rendering.  

IOOS.py: Python script for running IOOS-specific Quality Control checks using Pyodide/Pyscript.

How to Use  

1. Clone the Repository  

git clone
 https://github.com/Gyanankur23/alfridotechrepositoryall3tasks.git


cd alfridotechrepositoryall3tasks

2. File Details  

Open IOOS.html in your browser to launch the interface.  
Ensure all associated files (IOOS.css, IOOS.js, IOOS.py) are in the same directory.  

3. Workflow  

Upload Dataset:  

Click on the "Upload Dataset" button and select a CSV file.  
The uploaded dataset will be displayed in a table for preview.  

Run QC Checks:  

Click on the "Run Quality Control (QC) Checks" button.  
The Python script IOOS.py will process the dataset using the ioos-qc library.  
QC results will appear below the table in the "QC Results" section.  

4. Modify QC Configurations  

To run specific quality control checks, update the QC configuration file path in the Python code (IOOS.py) as needed.

Example Workflow  

1. Upload a CSV file containing oceanographic data.  
2. View the dataset in the table.  
3. Perform quality control checks (e.g., validating data entries, checking for anomalies).  
4. View the QC results directly in the browser interface.

Accessing the Project  

Find the project on GitHub here:
 https://github.com/Gyanankur23/alfridotechrepositoryall3tasks

GSOC 2025  


This project is a contribution for the Google Summer of Code 2025 initiative, showcasing innovation in open-source tools and technologies to improve oceanographic data processing and accessibility.
