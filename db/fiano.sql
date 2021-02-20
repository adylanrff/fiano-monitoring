drop table if exists project_deliverable_schedule_tab;
drop table if exists project_deliverable_worker_tab;
drop table if exists project_deliverable_tab;
drop table if exists worker_tab;
drop table if exists project_tab;

create table if not exists project_tab (
	id SERIAL primary key,
	project_name varchar(256),
	project_status varchar(256),
	timeline_start_date date,
	timeline_end_date date,
	actual_start_date date,
	actual_end_date date,
	created_at date,
	updated_at date,
	
	UNIQUE(project_name)
);

create table if not exists project_deliverable_tab (
	id SERIAL primary key,
	project_id int references project_tab(id) not NULL,
	section varchar(64),
	item varchar(64),
	subitem varchar(64),
	deliverable_status varchar(32),
	price int,
	quantity int,
	unit varchar, 
	info varchar,
	created_at date, 
	updated_at date
);

create table if not exists worker_tab (
	id SERIAL primary key,
	worker_name varchar(32), 
	worker_type varchar(32),
	created_at date, 
	updated_at date, 
	salary int,
	
	UNIQUE(worker_name)
);

create table if not exists project_deliverable_worker_tab (
	id SERIAL primary key,
	project_deliverable_id int references project_deliverable_tab(id) not null,
	worker_id int references worker_tab(id) not null,
	created_at date, 
	updated_at date,

	UNIQUE(project_deliverable_id, worker_id)
);


create table if not exists project_deliverable_schedule_tab (
	id SERIAL primary key,
	project_deliverable_id int references project_deliverable_tab(id) not NULL,
	schedule_type varchar(32),
	start_date date, 
	end_date date,
	created_at date, 
	updated_at date,
	
	UNIQUE(project_deliverable_id, schedule_type)
);