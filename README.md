# Example repo for testing with tornado / sqlalchemy

## Setup
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r ./requirements.txt

# run tests
python3 -m unittest tests/test.py

# run locally
python3 main.py

# new tab
curl -X PUT localhost:8888/ -H "Content-Type: application/json" -d '{"key": "name", "value": "matt"}'

curl -X GET localhost:8888/name
# {"key": "name", "value": "Matt"}
