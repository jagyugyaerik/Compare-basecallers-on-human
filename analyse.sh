#!/usr/bin/env bash

threads=12

minimap_path_exec=/home/jagyugyaerik/minimap2/minimap2
ref_path=/opt/human_hg19/chr1.fa
python_script_dir=/home/jagyugyaerik/nanopore/biostat
#
#mkdir -p 02_basecalled_reads
#mkdir -p 03_read_names_fixed
#mkdir -p 04_extract_reads
#
#python get_read_info.py /home/speter/nanopore/human_wgsR94/rel3/chr1/part2/ > 03_read_information/read_info.tsv
#python python find_read_names.py 03_read_information/read_info.tsv > 03_read_information/common_reads.tsv

cd 02_basecalled_reads
read_files=$(ls)

for f in $read_files; do
    set=${f%.fastq}

    all_reads=02_basecalled_reads/"$f"
    all_reads_fixed_names=03_read_names_fixed/"$f"
    extract_reads=04_extract_reads/"$f"
    alignment=05_alignment/"$set".paf

    printf "\n\n\n\n"
    echo "NORMALISE READ HEADERS: "$set
    echo "--------------------------------------------------------------------------------"
    python "$python_script_dir"/fix_read_names.py $all_reads 03_read_names_fixed/read_id_to_fast5 > $all_reads_fixed_names

    printf "\n\n\n\n"
    echo "EXTRACTING COMMON READS: "$set
    echo "--------------------------------------------------------------------------------"
    python "$python_script_dir"/extract_common_reads.py $all_reads 03_read_names_fixed/common_reads.tsv > $extract_reads

    printf "\n\n\n\n"
    echo "ALIGN READ TO REFERENCE: "$set
    echo "--------------------------------------------------------------------------------"
    ./minimap2 -k12 -t 12 -c /opt/human_hg19/chr1.fa "$extract_reads" > "$alignment"
    python

done