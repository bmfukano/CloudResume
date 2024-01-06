#!/bin/bash

for d in */; do
    pushd "$d"
    ZIP_NAME=${d%/}
    zip -j ../${ZIP_NAME}.zip src/*.py
    rm ${ZIP_NAME}.zip
    rm -rf package
    popd
done
