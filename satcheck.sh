if [ $# -eq 0 ] 
    then
        echo "No arguments supplied"
fi

if [ -z "$1" ] 
    then
        echo "Empty argument supplied"
fi

if [ -z "$2" ]
    then
       echo "Empty argument supplied"
fi

python3 cmdln.py "$1" "$2" > output.txt

