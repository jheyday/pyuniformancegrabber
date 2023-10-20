# RUniformanceGrabber
A Package for R that communicates with a Honeywell PHD Server via a seperate 32-bit executible written in .NETFramework and run via the package [processx](https://cran.r-project.org/web/packages/processx/index.html).

A 32-bit executible is used rather than directly using PHDAPINET.dll to allow avoid issues when using a 64-bit version of R and accessing a 32-bit DLL.
Data is passed between the executible and the package using XML and then parsed into a dataframe.


# Installation

# Dependencies

* Pandas
* lxml



# Use
