# Working with GLakeMap (Gacial Lake Mapping) Python Package

## 1. Installing machine learning packages
- Download and install Anacnonda software in your machine; links for details:
	https://www.anaconda.com/
	https://www.anaconda.com/products/individual
- Open the **Command Prompt** window and type `conda list`. The command should list a lists of packages availabe in the environemnt. If the command fails to list the packages, add Anacnonda to the **PATH** or use  **Anaconda Prompt** instead.
- Once conda command works, create a  **virtual environment** and install Python (Python 3.6 recommended) and the following packages:
	```	
	conda install -c anaconda numpy
	conda install -c anaconda scipy
	conda install -c anaconda matplotlib
	conda install -c anaconda scikit-learn
	conda install -c anaconda pandas
	```

## 2. Installing snappy package
* Download and install SNAP software in your machine: http://step.esa.int/main/download/snap-download/
* Configure Python to use the SNAP-Python (snappy) interface: https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface
	- **Note**: use Python 2.7 64-bit
## 3. Installing arcpy package

1) Make glakemap package (..\..\glakemap-dev\glakemap) the current working directory.

2) Open and edit the "config.py" file. Directions for How To are provided as comments.
