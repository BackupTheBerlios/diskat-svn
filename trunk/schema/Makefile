DB=../diskat.db
DB_DIST=diskat-dist.db

all:

migrate:
	cat migrate.sql | ../sqlite $(DB)

create-db:
	cat $(TABLE).sql | ../sqlite $(DB_DIST)
