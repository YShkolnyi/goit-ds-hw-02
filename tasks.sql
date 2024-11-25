-- Table: users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Table: status
DROP TABLE IF EXISTS status;
CREATE TABLE status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);
/*
ne rozumiju jak u name mogut' buty unikal'ni danni?
V umovi DZ jasno vkazano, schob name buły unikal'nymy.
A potom vkazano, schob do zapovnenja cogo polja vykorystovuvaty try ryadky:
    new
    in progress
    completed
Iakshcho ja pravil'no zrozumiv, to vyhodyt', shcho tildky mayuchy 3 zavdannya mozhna nadaty jym unikal'nyj status. Chetverte zavdannya povtoryt' odyn zi statusiv i perestane buty unikal'nym.
Svyadomo ne pyshy UNIQUE. Iakshcho pomyljajus', proshu pro posjanynnya.
*/

-- Table: tasks
DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);