# MetaMapLite Runner

a simple script for wrapping metamaplite to process files

Requires installation of MetaMapLite. 

Please edit MetaMapLiteRunner.py to include the appropriate path to your MetaMapLite installation.

Usage:

```
python MetaMapLiteRunner.py -l <logfilename> file1 fle2... 
```

Each input file will create two output files:

1. .mmi file is raw MetaMapLite output
2. .csv is the simplified output

Both should contain only codes and should therefore be de-identified.