#!/bin/bash

#SBATCH -n 1
#SBATCH -N 1
#SBATCH --mem=7500


#SBATCH -t 6:15:00 #Indicate duration using HH:MM:SS
#SBATCH -p serial_requeue #Based on your duration               


#SBATCH -o ./training_outputs/holdem_10_%a_output.txt
#SBATCH -e ./training_outputs/holdem_10_%a_errs.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=elanasimon@college.harvard.edu


# --------------

cd ~/cs182-poker
python -m poker.holdem.cfrm \
--i "$SLURM_ARRAY_TASK_ID" \
--n_shards 199 \
--n_iterations 12500 \
--strategy_folder ten_cards \
--starting_job 7 \