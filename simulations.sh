#!/bin/bash

## cancer genes ##

ERBB2="17 33600000 ERBB2"

MYC="8 127000000 MYC"

EGFR="7 55000000 EGFR"

BCL2="18 63000000 BCL2"

PIK3CA="3 179000000 PIK3CA"

cancerGenes=("${ERBB2}" "$MYC" "$EGFR" "$BCL2" "$PIK3CA")

for i in ${!cancerGenes[@]}; do
#	echo "element $i is ${cancerGenes[$i]}"
	set -- ${cancerGenes[$i]}
	echo chromosome $1 and position $2 and gene $3
	
	## Simple BFB simulations - no indels and no end deletions
	#endPos=$(( $2 + 3000000 ))
	#echo end position $endPos
	#echo COMMAND:./BFBSimulator.py 5 $1 $endPos new_hg38.fa -df 0 -dl 0 -dd simple -xf 0 -xl 0 -xd simple -o outputs/simple/${3} -p 0 -b 0 -bl 0
	#./BFBSimulator.py 5 $1 $2 $endPos new_hg38.fa -df 0 -dl 0 -dd simple -xf 0 -xl 0 -xd simple -o outputs/simple/${3} -p 0 -b 0 -bl 0
	
	for index in 1 2 3; do
		endPos=$(( $2 + 6000000 ))
		./BFBSimulator.py 10 $1 $2 $endPos new_hg38.fa -df 0 -dl 0 -dd simple -xf 0 -xl 0 -xd simple -o outputs/end_Deletions/${3}_${index} -p 0 -b 1 -bl 50000	
	done

	for ind in 1 2; do
                endPos=$(( $2 + 6000000 ))
                ./BFBSimulator.py 10 $1 $2 $endPos new_hg38.fa -o outputs/complex/${3}_${ind}
        done
done

