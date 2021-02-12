CREATE TABLE IF NOT EXISTS project_tab (
    id SERIAL PRIMARY KEY, 
    project_name varchar(64),
    project_status varchar(32),
    timeline_start_date int,
    timeline_end_date int,
    real_timeline_start_date int,
    real_timeline_end_date int,
    created_at int,
    updated_at int
);

CREATE TABLE IF NOT EXISTS project_deliverable_tab (
    id SERIAL PRIMARY KEY,
    project_id int REFERENCES project_tab(id),
    section varchar(32),
    item varchar(32),
    subitem varchar(32),
    deliverable_status varchar(32),
    price int,
    quantity int,
    unit varchar(32),
    created_at int,
    updated_at int
);

CREATE TABLE IF NOT EXISTS worker_tab (
    id SERIAL PRIMARY KEY,
    worker_name varchar(64),
    worker_type varchar(32),
    created_at int, 
    updated_at int,
    salary int
);

CREATE TABLE IF NOT EXISTS project_deliverable_worker_tab (
    id SERIAL PRIMARY KEY,
    project_deliverable_id int REFERENCES project_deliverable_tab(id),
    worker_id int REFERENCES workers_tab(id),
    created_at int,
    updated_at int
);

CREATE TABLE IF NOT EXISTS project_deliverable_schedule_tab (
    project_deliverable_id int REFERENCES project_deliverable_tab(id),
    schedule_type varchar(32),
    start_time int,
    end_time int,

    UNIQUE(project_deliverable_id, schedule_type)
)
