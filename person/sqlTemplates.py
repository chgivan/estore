createPersonTableSQL = """
    CREATE TABLE IF NOT EXISTS persons (
        id serial PRIMARY KEY,
        firstName varchar(50),
        lastName varchar(50),
        email varchar(50) UNIQUE NOT NULL,
        role varchar(5) NOT NULL,
        CHECK (role IN ('admin','user'))
    );
"""

insertPersonSQL = """
    INSERT INTO persons (firstName, lastName, email, role)
    VALUES (%(firstName)s, %(lastName)s, %(email)s, %(role)s) RETURNING id;
"""

def convertRow2Person(row):
    return {
        'id': row[0],
        'firstName': row[1],
        'lastName': row[2],
        'email': row[3],
        'role': row[4]
    }

selectAllIdsSQL = """
    SELECT id FROM persons
"""

selectFullPersonSQL = """
    SELECT id, firstName, lastName, email, role
    FROM persons
    WHERE (%(id)s) = id
"""
