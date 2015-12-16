# BaasBox Plugins Diff

This Python script performs a diff between plugins deployed on two different BaasBox servers.

It was inspired by the code at https://docs.python.org/2/library/difflib.html#a-command-line-interface-to-difflib

## Usage

You must provide at least 6 parameters:

+ URL of the first BaasBox server
+ appcode of the first BaasBox server
+ password of the user _admin_ of the first BaasBox server
+ URL of the second BaasBox server
+ appcode of the second BaasBox server
+ password of the user _admin_ of the second BaasBox server

You can have output in various formats, see below:

```shell
> python bb_plugins_diff.py -h
Usage: bb_plugins_diff.py [options] bb_url1 appcode1 adminpwd1 bb_url2 appcode2 adminpwd2

Options:
  -h, --help				Show this help message and exit
  -c						Produce a context format diff (default)
  -u						Produce a unified format diff
  -m						Produce HTML side by side diff (can use -c and -l in conjunction)
  -n						Produce a ndiff format diff
  -l LINES, --lines=LINES
							Set number of context lines (default 3)
```

## Only for Mac users

If you are using OSX you can find convenient to use:

```shell
> ./diff.sh 
```

Providing it the six parameters to connect with the BaasBox(es), the script directly opens a HTML file in Safari to show differences between plugins in a more human-readble way.

