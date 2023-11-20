
# Written by Aaron Wolf
# This code includes the necessary imports and initializations for translating variable and value labels in a Stata .dta file using the Google Translate API.

import pandas as pd
from google.cloud import translate_v2 as translate
import os
import getpass
import sys


# Set the target language
## You can pass a language when executing python 02_translate_cloud.py.
## For example: python 02_translate_cloud.py 'en'
## Retrieve the passed argument (target_language)
if len(sys.argv) > 1:
    targetLanguage = sys.argv[1]
    # Use the target_language variable in your script
else:
    # Default to english. You can change this to any language you want
    targetLanguage = 'en'
print(f"Target language is set to: {targetLanguage}")

# I use this to easily toggle between my local machine and the server
if getpass.getuser() == '<local-username>':
    maindir = '<path-to-local-main-directory>'
elif getpass.getuser() == '<server-username>':
    maindir = 'path-to-server-main-directory'
os.chdir(maindir)

# Define a function to translate each value in a given dictionary
def translate_dict(dictionary, client, target='en', source='pt'):
    """
    Translates each value in a given dictionary using the Google Translate API.

    Args:
        dictionary (dict): The dictionary containing text strings to be translated.
        client (google.cloud.translate_v2.Client): The Google Translate client.
        target (str, optional): The target language code. Defaults to 'en'.
        source (str, optional): The source language code. Defaults to 'pt'.

    Returns:
        dict: The dictionary with translated values.
    """
    for key, value in dictionary.items():
        result = client.translate(value, target_language=target, source_language=source)
        dictionary[key] = result['translatedText'].replace("&#39;", "'")
    return dictionary


# Define the final function to read in the data and translate the variable and value labels
def labTrans(file, client, target='en', source='pt'):
    """
    Reads in a Stata .dta file, extracts the variable and value labels, and translates them using the Google Translate API.

    Args:
        file (str): The path to the Stata .dta file.
        client (google.cloud.translate_v2.Client): The Google Translate client.
        target (str, optional): The target language code. Defaults to 'en'.
        source (str, optional): The source language code. Defaults to 'pt'.

    Returns:
        tuple: A tuple containing the translated variable labels dictionary and the translated value labels dictionary.
    """
    # read in file and get the variable and value labels
    reader = pd.read_stata(file, iterator=True)
    varlabels_source = reader.variable_labels()
    vallabs_source = reader.value_labels()

    # translate variable labels
    varlabels_target = translate_dict(varlabels_source, client, target, source)

    # For each key in vallabs_source, translate the value labels
    vallabs_target = {}
    for key in vallabs_source.keys():
        vallabs_target[key] = translate_dict(vallabs_source[key], client, target, source)

    return varlabels_target, vallabs_target


# Now take the output of the labTrans function and write the labels to do files
def doLabs(infile, outfile_stub, client, target='en', source='pt'):
    """
    Takes the output of the labTrans function and writes the translated variable and value labels to .do files.

    Args:
        infile (str): The path to the Stata .dta file.
        outfile_stub (str): The path and filename stub for the output .do files.
        client (google.cloud.translate_v2.Client): The Google Translate client.
        target (str, optional): The target language code. Defaults to 'en'.
        source (str, optional): The source language code. Defaults to 'pt'.
    """
    varlabels_target, vallabs_target = labTrans(infile, client, target, source)

    # Ensure outfile ends in .do. If not, return error
    if outfile_stub[-3:] != '.do':
        print('Error: outfile must end in .do')
        return

    # Create file names: -varlabs.do and -vallabs.do
    varlab_file = outfile_stub[:-3] + '-varlabs.do'
    vallab_file = outfile_stub[:-3] + '-vallabs.do'

    # Get the name of the file without the path
    fname = os.path.basename(infile)

    # Write the variable labels to a do file with each line being "label variable varname "varlabel""
    with open(varlab_file, 'w',encoding='utf-8') as f:
        f.write(f'* Translated Variable Labels for {fname} \n')
        f.write(f'* Author: Aaron Wolf (aaron.wolf@u.northwestern.edu) \n')
        for key, value in varlabels_target.items():
            f.write('label variable ' + key + ' "' + value + '"\n')

    # Do the same for vallabels (if vallabs_target is not empty)
    if vallabs_target:
        with open(vallab_file, 'w',encoding='utf-8') as f:
            f.write(f'* Translated Value Labels for {fname} \n')
            f.write(f'* Author: Aaron Wolf (aaron.wolf@u.northwestern.edu) \n')
            for key, value in vallabs_target.items():
                f.write(f'* {key} \n')
                for k, v in value.items():
                    f.write(f'label define {key} {k} "{v}", modify \n')
    else:
        print(f'No value labels in {fname}')

# Now loop through all directories and files in reiswd
# and translate all files. Save the label in the same relative directory and with the same name
reiswd = '../../RAIS Dataset 2023/output/data/'
dirlist = os.listdir(f'{reiswd}') # Directory with folders full of data
labdir = f'code/labels-{targetLanguage}'                # Main Directory to save the do files (in relative folders)
if not os.path.exists(labdir):
    os.makedirs(labdir)

# Initiate the Google translate client
client = translate.Client()             

# Loop through each directory in dirlist
for dir in dirlist:
    print(dir)
    
    # Make sure the directory ../{labdir}/{dir} exists
    if not os.path.exists(f'{labdir}/{dir}'):
        os.makedirs(f'{labdir}/{dir}')
    
    # Loop through the files in the current directory
    filelist = os.listdir(f'{reiswd}/{dir}')
    for file in filelist:
        # Check if the file is a .dta file
        if file.endswith('.dta'):
            print(file)
            
            # Set the input and output file paths
            infile = os.path.join(reiswd, dir, file)
            outfile_stub = f'{labdir}/{dir}/' + file.replace('.dta', '.do')
            
            # Translate the labels and save to the output file
            doLabs(infile, outfile_stub, client, target=targetLanguage, source='pt')
