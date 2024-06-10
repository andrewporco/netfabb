## Setup (do once at start)
1. Extract netfabb-dataset-generation to W:/Desktop/
2. Identify your user path of the shared W drive (e.g. right click netfabb-dataset-generation folder and view location)
   - If you see 'users1', do nothing
   - If it has 'users[another number]', right click netfabb-dataset-generation/run.bat and Edit
     - Change 'set USER_ID=1' to have the right number and save the file

3. Create a folder on the shared W drive  --  W:/miniconda
4. Download and install miniconda to W:/miniconda

5. Extract the stl dataset to the correct location depending on your W drive space
   - Non-PhD students have W drives capped at 2GB
     - Place the stl.zip file on the W drive
     - Extract stl.zip directly to C:/Users/%username%/
   - PhD students have hundreds of GB available
     - Extract the full shape stl.zip dataset to W:/

## Procedure (do on each computer)
#### Start:
- Non-PhDs with capped W drives should extract stl.zip to C:/Users/$username$/
- Open W:/Desktop/netfabb-dataset-generation/start-stop-indices.txt and edit index range
- Double click W:/Desktop/netfabb-dataset-generation/run.bat to run all simulations between specified [start, stop) indices  

#### Finish:
- Compress the output files in C:/users/$username$/SandBox (right-click > send to > Compressed folder > name [start-stop-indices].zip)
- Copy zip file to external hard drive - "zip-files" folder
