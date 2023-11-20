#!/bin/bash
#SBATCH --job-name=rais
#SBATCH --output=rais-translate-%A_%a.out
#SBATCH --account=<insert-project-account-id>
#SBATCH --nodes=1 --cpus-per-task=1
#SBATCH --mem-per-cpu=32G
#SBATCH --partition normal
#SBATCH --time=2:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=<insert-email>
#SBATCH --array=1-5  # Number of target languages

# Define the list of target languages
target_languages=("en" "fr" "es" "hi" "zh-CN")

# cd to directory
cd <path-to-data>

# activate the environment
source activate <your-conda-environment>

# load gcloud
module load gcloud/379.0.0

# Get the specific target language for this job
target_language=${target_languages[$SLURM_ARRAY_TASK_ID - 1]}

# Run script for the specific target language
python 01_translate_cloud.py "$target_language"
