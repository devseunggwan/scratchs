#!/bin/bash

mkdir -p python_installation_files
cd python_installation_files

dnf install --downloaddir . --downloadonly python3.12 python3.12-pip python3.12-devel  -y

# with install
if [[$1 == "-i"]]; then 
    rpm -ivh *.rpm
f