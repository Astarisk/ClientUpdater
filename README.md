# ClientUpdater

An early Python project: a small desktop updater and Java launcher built around XML manifests and a wxPython interface.

The interesting part is the update flow: read a manifest, select files for the current operating system and architecture, compare local SHA-1 hashes, and download missing or changed files. The repository includes sample manifests and a small Java demo.

## What's here

- [Updater.py](Updater.py) starts the desktop application; [GUI.py](GUI.py) provides update and launch controls.
- [Downloader.py](Downloader.py) downloads manifests and files, compares local hashes, and supports optional HTTP Basic authentication.
- [Config.py](Config.py) defines download URLs, local directories, authentication settings, and manifest filtering.
- [util/ManifestGenerator.py](util/ManifestGenerator.py) generates manifests and contains an SFTP publishing experiment, including support for hand-written XML entries for platform-specific files.
- [testfiles/](testfiles/) contains the sample update payload and manifest.

## Trying the desktop demo

This is a historical learning project with Windows-style paths and unpinned dependencies. Review `Config.py` before running: it defaults to the sample files in this repository and a `TestClient` directory under the user's home directory.

The desktop app requires Python 3 and wxPython. Java must be on `PATH` to use the demo launcher. From the repository root, the entry point is:

```sh
python Updater.py
```

The Run action launches `SimpleDemo.jar` and writes its output to `errorlog.txt` in the configured client directory. Dependency installation and runtime compatibility have not been revalidated on current environments.

## Manifest generation

The optional generator uses `pysftp` and has separate source-directory and SFTP settings at the top of the script. It performs uploads when run; it is not needed to explore the desktop demo. Its special-case XML supports OS and architecture-specific entries, while recursive directory handling is unfinished.

The publishing code needs review before reuse: it disables SFTP host-key checking, and its change comparison does not include newly added manifest entries. The updater's optional saved credentials are plain text, and SHA-1 is used for change detection, not signed-update verification.

This repository preserves an early experiment in desktop tooling, manifests, and distribution rather than a maintained release system.
