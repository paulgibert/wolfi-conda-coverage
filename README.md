# wolfi-conda-coverage

Attempts to match and count wolfi packages to conda packages.

#### Setup
```
make build
```

This command will setup the project and generate `wolfi-packages.txt` which contains the latest wolfi packages
containing `py3` in the name. This method for identifying wolfi python packages is *probably* not a catch-all.

#### Usage
```
make count
```

The count will be printed to the console. A wolfi-to-conda table of matches will be saved to `matches.json`.

The counter matches against wolfi packages that follow the naming convention:

`[py3*]-[package_name]-[version]-[revision]`

`package_name` is compared against the conda package name for matching. Version and architecture is ignored. This method captures most of the packages but occasionally misses one. For example, although both wolfi and conda support tensorflow, the wolfi version is called "tensorflow-core" while conda just calls the package "tensorflow" resulting in a mismatch.