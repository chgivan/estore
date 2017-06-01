### Run Test Database


docker run \
    --name db \
    -e POSTGRES_USER=person \
    -e POSTGRES_PASSWORD=mysercetpassword \
    -p "5432:5432" \
    -d postgres:alpine

set POSTGRES_USER=person
set POSTGRES_PASSWORD=mysercetpassword
set POSTGRES_DB=person
set POSTGRES_HOST=192.168.99.100

docker exec -it db psql -U person

#Run Test service
pip install -r requirements.txt
python service.py

Person
    - firstName: String
    - lastName: String
    - email: String
    - role: String
    - name: String