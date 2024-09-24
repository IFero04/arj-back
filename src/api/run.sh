if [[ $1 == "dev" ]]; then
    python3 main.py
elif [[ $1 == "sit" || $1 == "prod" ]]; then
    python3 main.py
else
    echo "Need to follow format ./run.sh dev|sit|prod"
fi
