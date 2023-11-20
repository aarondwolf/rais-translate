# RAIS Stata Label Translate
 This repository provides translated variable and value labels for the RAIS Dataset. The Python code uses takes a Stata .dta file, pulls all varile and value labels, and uses Google Translate API to translate them to a language of your choice. 

 I have already generated labels for 5 languages, available in the `labels-{lang}` folder:
 - English (en)
 - Spanish (es)
 - French (fr)
 - Hindi (hi)
 - Mandarin (zh-CN)
 
 ## How do I use these labels?
 The output is two .do files for each .dta: `<dtaname>-varlabs.do` and `<dtaname>-vallabs.do`, which one can run within Stata after opening the dta file using `do <dtaname>-varlabs.do` and `do <dtaname>-vallabs.do`. 

 ## Translating a Single File
 Use `01_translate_local.ipynb` if you wish to only translate one file. In the 4th code block, you will see the code that tests the `doLabs()` function. This is used for a single file. Just replace all the strings with your file paths, and run!

 ## Disclaimer
 I am using cleaned RAIS dataset courtesy Ricardo Dahis (https://github.com/rdahis/clean_RAIS). Ricardo also provides some english labels under RAIS/extra/Variables_RAIS_1985-2018.xlsx. The workflow I use is more general and covers all variable and value labels, can be used to translate to multiple languages, and should provide a simplified method for attaching them to a dataset you are using (simply run the .do file), but there is a risk of Google Translate messing up the translation. Use at your own discretion! 

 ## Requirements
 1. Stata (any version)
 2. Python 3.8+ with pandas (`conda install -c conda-forge pandas`), Google Cloud Core (`conda install -c conda-forge google-cloud-core`) and Google Cloud Translate (`conda install -c conda-forge google-cloud-translate`) installed. (Optionally use pip)
 3. A Google Cloud Accout with Google Cloud CLI installed on your machine (see below for full instructions).

 ## Files
 **If you are just trying to learn how to translate one .dta file. `01_translate_local.ipynb` will suffice.** The other two are meant for looping over multiple files and translating them all. 

 1. `01_translate_local.ipynb`: A Jupyter notebook explaining the full process of connecting to Google Cloud, translating text, and creating programs to pull and translate the labels. Use this if you are just doing one or a couple datasets locally.
 2. `02_translate_cloud.py`: A Python file meant for cloud computing. Can also be used for locally running `python 02_translate_cloud.py` if this is preferred. This allows you to specify a language in the call to the file. e.g. `python 02_translate_cloud.py 'en'`.
 3. `03_array_job.sh`: A SLURM batch script for running 02_translate_cloud.py on a SLURM based High performance computing cluster in the cloud. The RAIS data I was using took up 750GB, so I ran everything in the cloud. This is likely unnecessary if you are only trying to translate one file at a time. 

 ## Replication Instructions
 For those who just want the labels, feel free to take the labels from this repository: No need to replicate.

 For those interested in replication, or for those interested in how to translate Stata dataset variable and value labels more generally, read on!
 
 ### Setting Up Google Cloud
 These setup instructions are repeated in `01_translate_local.ipynb`.

 Before you begin, you will need to set up an account and project in Google Cloud. You can use a personal Google account for this step.

 #### 1: Create a Google Cloud account and project
 1. Navigate to https://cloud.google.com/ to set up an account with Google Cloud (skip if you already use Google Cloud).
2. In the console, create a new project: https://developers.google.com/workspace/guides/create-project.
3. Enable Google Translate API on that project: https://cloud.google.com/translate/docs/setup

#### 2: Set up your Local Development Environment
1. Install Google Cloud CLI on your machine: https://cloud.google.com/sdk/docs/install 
2. On your local development environment, initialize Google Cloud for the first time: `gcloud init`.
3. Once you have authenticated, choose the default project. This makes it easier for you to interact with APIs enabled for that project.
4. You'll need to ensure the GC project is billable from local system auth: `gcloud auth application-default set-quota-project <PROJECT ID>`
5. Ensure Google Cloud core (`conda install -c conda-forge google-cloud-core`) and Google Cloud Translate (`conda install -c conda-forge google-cloud-translate
`) are installed in your anaconda environment. (Optionally use pip).

#### 3: [Optional] Set up gcloud on a SLURM cluster
1. Open a new SSH terminal to your cluster.
2. [Optional] Activate the conda environment for your project: `conda activate ENV_NAME`
2. Load gcloud CLI:  `module load gcloud/379.0.0`.
3. Initialize Google Cloud for the first time: `gcloud init`
4. The terminal will give you instructions. You must copy the code it gives you into a command prompt terminal on your local machine. That will then pop you over to a browser, where you will authenticate. Once that it done, your local terminal will provide you some code. Copy this back into your Quest terminal to complete authentication.
Note: If this fails for some reason, just type in `gcloud auth application-default set-quota-project <PROJECT ID>` to try again. You will know it worked when the last line in te terminal reads "Quota project "<PROJECT ID>" was added to ADC which can be used by Google client libraries for billing and quota. Note that some services may still bill the project owning the resource."
5. Select the project ID you wish to work with. This will make that project your default project. Form now on, any Google Cloud API commands you use will use the account and project that you authenticated with. You can change this for any given script, but will need to do so manually. I will not detail that here.
6. Ensure Google Cloud core (`conda install -c conda-forge google-cloud-core`) and Google Cloud Translate (`conda install -c conda-forge google-cloud-translate`) are installed in your anaconda environment. (Optionally use pip).

That's it! To quickly check whether it has worked (on LDE or SLURM), open a quick iPython environment (or notebook) and try the following:

```
from google.cloud import translate_v2 as translate
translate_client = translate.Client()
translate_client.translate("Hello!",target_language='fr',source_language='en')
```
```
OUT: {'translatedText': 'Bonjour!', 'input': 'Hello!'}
```

## Citations and Contact
Feel free to reach out if anything is not working. You can email me at aaron [dot] wolf [at] u [dot] northwestern [dot] edu. 


