DB=../diskat.db

all:

migrate:
	cat migrate.sql | ../sqlite $(DB)

create-table:
	cat $(TABLE).sql | ../sqlite $(DB)
