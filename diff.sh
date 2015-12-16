#!/bin/bash

if [ "$#" -lt 6 ]; then
	echo "ERROR: you must provide: BaasBox_URL_1 appcode1 adminpwd1 BaasBox_URL_2 appcode2 adminpwd2"
	exit 1
fi

python bb_plugins_diff.py -m -l 10 -c $* > tmp.html && open -a /Applications/Safari.app tmp.html
