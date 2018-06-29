# Installing

`virtualenv` and the like are things you might want to bother with before going forward.

## The APIs
`pip install -r requirements.txt`

## The Database
```
brew install mysql
```

### Creating the tables
```
mysql -uroot # connect to a MySQL shell as the root user
mysql> source setup.sql;
mysql> quit;
```

# Running

## The Game Server
`FLASK_APP=server.py flask run`

## The Random Agent
`FLASK_APP=random_agent.py flask run`

## The Database
`brew services start mysql` # will keep MySQL running in the background.

### Creating the tables
```
mysql -uroot # connect to a MySQL shell as the root user
mysql> source setup.sql;
mysql> quit;
```

# Testing
`pytest`