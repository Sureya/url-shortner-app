CREATE  TABLE IF NOT EXISTS serverless.short_url(
uuid integer not null constraint short_url_pk primary key,
url text not null,
result_url text
);
