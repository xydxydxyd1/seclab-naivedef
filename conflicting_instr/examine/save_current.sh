#!/bin/bash
# save_current.sh filename
# Save the last result (based on default arguments) into
# saved_results/$filename.pkl
while getopts "" opt; do
    case $opt in
	\?)
	    echo "Invalid option: -$OPTARG" >&2
	    ;;
    esac
done
if [[ "$#" -ne 1 ]]; then
    echo "Illegal number of parameters" >&2
    exit 1
fi

unsaved_fp="../data/judge.pkl"
save_filepath="saved_results/$1.pkl"

echo "Saving $unsaved_fp to $save_filepath"
cp $unsaved_fp $save_filepath
