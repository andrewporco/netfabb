# Netfabb Tools
Tools for working with data from Autodesk Netfabb in Python

## Description of files
- [ensight.py](ensight.py) - Read .geo and .ens files in EnSight Fortran Binary format
- [extract-netfabb-data-binary.py](extract-netfabb-data-binary.py) - Input a directory with Netfabb (binary) results. Outputs .npz files with vertex coordinates, edge connectivities, and nodal displacements at the final time step. The script could potentially be modified to export information other than nodal displacements.
- [extract-netfabb-data-ascii.py](extract-netfabb-data-ascii.py) - Same as above, but for ASCII result files.

## Provided examples
2 Netfabb result files are included, both from shapes in the [Fusion360 Gallery Dataset](https://github.com/AutodeskAILab/Fusion360GalleryDataset)
- [ASCII Example](example-result-files/ascii)
- [Fortran Binary Example](example-result-files/binary)


## Useful links
- [Netfabb Output Files](https://help.autodesk.com/view/NETF/2024/ENU/?guid=GUID-FFA9FD93-2501-42A7-9272-1CB462FBC077) - 
Explanations of what each output file contains

- [Netfabb User Manual PDF Download](https://www.autodesk.com/akn-aknsite-article-attachments/ae612cb3-8d78-4bad-a6b5-26104ffbd63d.pdf) - 
Generally useful user manual for Netfabb

- [Netfabb Examples Manual](https://damassets.autodesk.net/content/dam/autodesk/external-assets/support-articles/sample-files-and-offline-documents-for-netfabb/examples_2024_0.pdf) - 
Contains examples of Netfabb output for different types of simulations

- [EnSight User Manual](https://dav.lbl.gov/archive/NERSC/Software/ensight/doc/Manuals/UserManual.pdf) - 
Documents the binary and ASCII EnSight file formats, which Netfabb uses for its simulation results


## Notes about output files
- For .geo element connectivity information, see page 402 of the EnSight manual linked above.
- For the mechanical simulation, there are 2 mechanical output file indices for every 1 .geo file index -- and then an extra .geo file with index 0. Time step information is in the .case file. 
  - The highest mechanical output file index corresponds to the highest .geo file index. This .geo contains the part only and not the build plate.