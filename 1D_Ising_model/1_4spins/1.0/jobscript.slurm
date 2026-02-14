#!/bin/bash

#SBATCH --nodes=1                   # the number of nodes
#SBATCH --ntasks-per-node=64             # the number of cores
#SBATCH --mem=30G
#SBATCH --job-name="1D_4"     # sets job name
#SBATCH --exclude=ccc0302
#SBATCH -o %x.o%A
#SBATCH -e %x.e%A
#SBATCH -t 4:00:00           # sets maximum total CPU time
#SBATCH -p secondary

python main.py  > output
