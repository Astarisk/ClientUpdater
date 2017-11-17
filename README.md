# ClientUpdater

A client updater based upon manifest files. The utils folder contains a script I use to generate the manifest file. The script also uploads the updated files and manifest to a sftp server, the settings of which are configurable in that python file.

The updater supports authorization access, and can be enabled and disabled in the Config python file. The client determines updates by comparing the client files sha1 to that found in the generated manifest file. The Config file also contains the variables for changing where the client is saved, where it downloads from, and all the other goodies. For now, when you hit the run button all that happens is a simple project euler problem I had saved will be ran. The output for this project can be found in the errorlog.txt in the client directory.
