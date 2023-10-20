# pyuniformancegrabber
A Package for python that communicates with a Honeywell PHD Server via a seperate 32-bit executible written in .NETFramework.

A 32-bit executible is used rather than directly using PHDAPINET.dll to allow avoid issues when using a 64-bit version of R and accessing a 32-bit DLL.
Data is passed between the executible and the package using XML and then parsed into a dataframe.

# Installation

# Dependencies

* Pandas
* lxml
# Use

``` python

from pyuniformancegrabber import uniformance
#Uniformance can also be provided hostname, port, username, password
#By default port=3000, username='', password=''
a = uniformance("MALSHW1")
#tags can be added either individually or as a list
a.add_tag('A.RL_AI7361.BATCH')
a.add_tag('A.RL_AI7361.GRADE')

a.add_tag(['A.RL_AI7361.BATCH','A.RL_AI7361.GRADE'])

#You can check if a tag exists at the host with 
a.check_tag('A.RL_AI7361.GRADE')

#show_tags will return a list of tags
a.show_tags()

# A number of parameters can be controlled when grabbing data
#all server parameters and sample parameters can be viewed with
a.show_parameters()

#Start and end time take a wide range of formats from dd/mm/yyyy, to a string with format NOW-1D
a.set_starttime('NOW-1D')
a.set_endtime('NOW')

#Sampling Frequency
#Honeywell offer a range of sample type "Snapshot", "Average", "Resampled", "Raw", "InterpolatedRaw".
#If using a type which supports setting sample frequency,
#ensure use samplefrequency is set to true and sampletype supports the action
a.set_useSampleFrequency(False)
a.set_SampleFrequency('60')
a.set_SampleType('Raw')

#Other parameters
a.set_ReductionFrequency('60')
a.set_ReductionOffset('Around')
a.set_ReductionType('None')

#get_results returns a list of dataframes, where each dataframe contains the results for one tag
m= a.get_results()
```
