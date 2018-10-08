#!/bin/bash

ZIP_NAME=""

print_help () {
    echo "Usage: zipRelease.sh [OPTIONS]"
    echo "Create the zip-file release for the ExploreBank plugin."
    echo "This creates a zip-file with a name determined by the plugin version"
    echo "from 'load.py'. This can be overriden with the -n option."
    echo ""
    echo "Options:"
    echo "  -h          Help. Print this help message"
    echo "  -n          Name, Zip-file name to use instead of the generated name."
    exit 1
}
while getopts ":hn:z" opt; do
    case $opt in
        h)
            print_help
            ;;
        n)
            ZIP_NAME=${OPTARG}
            ;;
        z)
            set -o xtrace
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Invalid option: -$OPTARG requires an argument" >&2
            exit 1
            ;;
    esac
done
#Remove parsed arguments
shift "$((OPTIND-1))"

if [ -z ${ZIP_NAME} ]; then
   #No name override provided
   VER_STR=$(grep "VERSION =" load.py | awk '{print $3}' | sed "s/'//g" | sed "s/\./_/g")
   ZIP_NAME="ExploreBank_${VER_STR}"
fi

mkdir ExploreBank
cp __init__.py load.py explore_bank.py README.md ExploreBank/
zip -r $ZIP_NAME ExploreBank
rm -r ExploreBank
