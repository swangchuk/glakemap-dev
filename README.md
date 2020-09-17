# Working with GLakeMap (Gacial Lake Mapping) Python Package

## 1. Installing machine learning packages
- Download and install Anacnonda software in your machine; links for details:
	https://www.anaconda.com/
	https://www.anaconda.com/products/individual
- Open the **Command Prompt** window and type `conda list`. The command should list a lists of packages availabe in the environemnt. If the command fails to list the packages, add Anacnonda to the **PATH** or use  **Anaconda Prompt** instead.
- Once conda command works, create a  **virtual environment** and install Python (recommend Python 3.6) and the following packages:
	```	
	conda install -c anaconda numpy
	conda install -c anaconda scipy
	conda install -c anaconda matplotlib
	conda install -c anaconda scikit-learn
	conda install -c anaconda pandas
	```
## 2. Installing arcpy package
- Install Background Geoprocessing (64-bit) software: https://desktop.arcgis.com/en/arcmap/latest/analyze/executing-tools/64bit-background.htm. Python 2.7 64-bit should be installed with this tool.

## 3. Installing snappy package
* Download and install SNAP software in your machine: http://step.esa.int/main/download/snap-download/
* Configure Python to use the SNAP-Python (snappy) interface: https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface
	- **Note**: Strongly recommend to use SNAP 64-bit version and Python 2.7 64-bit installed in step 2 for the latter.

## 3. Using glakemap package
- Download the glakemap package and set **glakemap-dev** as the current working directory.
- Open and edit the `config.py` file. Directions for **How To** are provided as comments.
- Recomend to use Visual Studio Code : https://code.visualstudio.com/, for execcuting codes inside `config.py`

## Possible Future Additions/Replacement

- Replace `arcpy` with `gdal` package for supporting `Python 3` and above for all tasks.
- Add different machine learning models.

## References

- If you use this program in your work, please kindly refer the following publications:
	- **Wangchuk**, S., & Bolch, T. (2020). Mapping of glacial lakes using Sentinel-1 and Sentinel-2 data and a random forest classifier: Strengths and challenges. **Science of Remote Sensing**, 2, 100008.
	- **Wangchuk**, S., Bolch, T., & Zawadzki, J. (2019). Towards automated mapping and monitoring of potentially dangerous glacial lakes in Bhutan Himalaya using Sentinel-1 Synthetic Aperture Radar data. **International journal of remote sensing**, 40(12), 4642-4667.