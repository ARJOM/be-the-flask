CREATE TABLE ongs(
	id varchar(8) primary key,
	name varchar(80) not NULL,
	email varchar(80) not NULL,
	whatsapp varchar(80) not NULL,
	city varchar(80) not NULL,
	uf varchar(2) not NULL
);

CREATE TABLE incidents(
	id integer primary key autoincrement,
	title varchar(80) not NULL,
	description text not NULL,
	value decimal not NULL,
	ong_id varchar(8) not NULL,
	foreign key(ong_id) references ongs(id)
)