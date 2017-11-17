# ClientUpdater

A client updater based upon manifest files. The utils folder contains a script I use to generate the manifest file. The script also uploads the updated files and manifest to a sftp server, the settings of which are configurable in that python file.

The updater supports authorization access, and can be enabled and disabled in the Config python file. The client determines updates by comparing the client files sha1 to that found in the generated manifest file.

The Config file also contains the variables for changing where the client is saved, where it downloads from, and all the other goodies. 
You would need to point the filedir variable in in ManifestGenerator towards the folder that contains the files you wish to generate a manifest for. The specialcase variables are there for special handwritten xml files that might be otherwise too hard to generate through script. In my case this was the libraries related to OS and arch.

The ManifestGenerator also requires you  to set the sftp variables. This is so you can connect to your own sftp server, and have the files automatically uploaded to the server. You can read the variables at the top of this file for more documentation.


For now, when you hit the run button all that happens is a simple project euler problem I had saved will be ran. The output for this project can be found in the errorlog.txt in the client directory.

You can run the project by invoking python on the Updater.py. I generally just do my work out of Pycharm.
