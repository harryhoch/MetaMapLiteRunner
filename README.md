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

Note that although the extension is ".csv", the simplified output file is actually pipe deliminted.

#MetaMapLiteServerRunner.py 

This version of the Runner uses an modified version of MetaMap Lite available at:
https://github.com/espinoj/public_mm_lite
This modified version provides the functionality for MetaMap to run as a daemon accepting input from either HTTP GET requests or via STDIN. To activate this feature the user should enter a single filename that is either `http://localhost:<port>` for HTTP Server Mode or `stdin` for stdin mode.   In HTTP Server mode enter requests as `http://localhost:<port>//process?filename=<filename>` In stdin mode the server waits for filename input.  Both formats will return json strings like `{'status':'processed','procTime':48.0,'filename':'/tmp/7602_200017_03262020_101127.LDS.txt'}`.

To use the MetaMapLiteServerRunner.py use the same switches available to MetaMapLiteRunner.py but add the -d switch to put it into daemon mode.  Number of CPUs i.e., -c still work.
 


