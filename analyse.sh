#!/usr/bin/env bash

threads=12

minimap_path_exec=/home/jagyugyaerik/minimap2/minimap2
ref_path=/opt/human_hg19/chr1.fa

mkdir -p 02_basecalled_reads
mkdir -p 03_read_names_fixed

python get_read_info.py /home/speter/nanopore/human_wgsR94/rel3/chr1/part2/ > 03_read_information/read_info.tsv
python python find_read_names.py 03_read_information/read_info.tsv > 03_read_information/common_reads.tsv

cd 02_basecalled_reads
read_files=$(ls)

for read in ; do
    set=${read%.fastq}

done