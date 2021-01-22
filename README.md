# Working with Glacial Lake Mapping Python Package (GLakeMap)

## 1. Installing machine learning packages
- Download and install Anacnonda software in your machine; links for details:
	https://www.anaconda.com/
	https://www.anaconda.com/products/individual
- Open the **Command Prompt** window and type `conda list`. The command should list a lists of packages availabe in the environemnt. If the command exits with an error, add Anacnonda to the **PATH** or use  **Anaconda Prompt** instead.
- Once conda command works, create a  **virtual environment** and install Python (recommend Python 3.6) and the following packages:
	```	
	conda install -c anaconda numpy
	conda install -c anaconda scipy
	conda install -c anaconda matplotlib
	conda install -c anaconda scikit-learn
	conda install -c anaconda pandas
	```
## 2. Installing arcpy package
- Install Background Geoprocessing (64-bit) software: https://desktop.arcgis.com/en/arcmap/latest/analyze/executing-tools/64bit-background.htm. Python 2.7 64-bit should be installed with this tool and `arcpy` package should also work.

## 3. Installing snappy package
* Download and install SNAP software in your machine: http://step.esa.int/main/download/snap-download/
* Configure Python to use the SNAP-Python (snappy) interface: https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface
	- **Note**: Strongly recommend to use SNAP 64-bit version and Python 2.7 64-bit installed in step 2 for the latter.

## 3. Downloading data and using glakemap package
- Download Sentinel-1, Sentinel-2, and DEM data and place them, respectively, inside the folder `data_directory` which is provide along with the package. Downloading DEM data is not necessary. Check `Process Dem Data` section of  the `config.py` file.
- Download `glakemap` package and set **glakemap-dev** as the current working directory. You can also clone the repository if you have **Git** installed in your machine. If so,  use `git clone` command.
- Open and edit the `config.py` file. Directions for **How To** are provided as comments.
- Recomend to use Visual Studio Code : https://code.visualstudio.com/, for execcuting codes inside `config.py`. It is easy/handy to change between Python versions in VS Code. Spyder IDE can be used as well to excute the machine learning codes.
- Changing Python versions apply only when you have acees to ArcGIS Desktop

## **Notes**
- Steps 2 and 3 are for supporting `arcpy` and `snappy` functionalites, concurrently, in Python 2.7.
- To support all workflows simultaneously, installation of ArcGIS Pro is must and environemnt setup should be done correctly (see step 4). Howeever, you are strongly recommended to follow steps 1-3 as parameter for some tools between ArcGIS Desktop and Pro might differ and program might run into errors.

## 4. Running all workflows in Python 3
- Create and clone the environemnt (ENV) within ArcGIS Pro software: https://pro.arcgis.com/en/pro-app/arcpy/get-started/what-is-conda.htm. If creating ENV fails with an error, run ArcGIS pro as an administrator and try again.
- Once ENV is created, open Command Prompt and type `conda env list`. Conda should list all the availabe ENVs in your system along with the one you created.
- Potentially, there could be **no ENV name** for your newly created/cloned environemnt within ArcGIS Pro. To give one, enter e.g. `conda create --name my_env_name --clone C:\Users\user_name\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone1`. Now, if you type `conda env list` again in Command Prompt, your ENV with newly given ENV name should appear in the list. If it does, now activate ENV  with the command `conda activate my_evn_name`. If it succeded, an asterisk symbol should appear on the ENV name indicating that it is active/activated. Now, you should be able to install any module into the newly created ENV using the `conda` command. Refer: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
- Follow Step 3 for installing `snappy` package, except use Python 3 instead of Python 2. Install machine learning packages, too, as step 1.

## Possible Future Addition/Replacement

- Replace `arcpy` with `gdal` package for supporting `Python 3` and above for all tasks in an open access manner.
- Add different machine learning models.

## Query/Support
- Links here were provided to support you with relevant resources that I personally found useful while setting up proper and working environemnt.
- If you have any trouble or question, be it setting up the environemnt correcly or running the code successfully, drop me an email: sw274@st-andrews.ac.uk

## References

- If you use this program in your work, please kindly refer the following publications:
	- **Wangchuk**, S., & Bolch, T. (2020). Mapping of glacial lakes using Sentinel-1 and Sentinel-2 data and a random forest classifier: Strengths and challenges. **Science of Remote Sensing**, 2, 100008.
	- **Wangchuk**, S., Bolch, T., & Zawadzki, J. (2019). Towards automated mapping and monitoring of potentially dangerous glacial lakes in Bhutan Himalaya using Sentinel-1 Synthetic Aperture Radar data. **International journal of remote sensing**, 40(12), 4642-4667.
