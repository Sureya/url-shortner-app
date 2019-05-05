CREATE TABLE IF NOT EXISTS serverless.urls(
	uuid varchar(1000) not null
		constraint urls_pk
			primary key,
	url integer not null,
	short_url integer
);
