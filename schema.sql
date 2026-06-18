-- Drop existing tables if they exist (Be careful if you have existing data!)
DROP TABLE IF EXISTS user_actuals;
DROP TABLE IF EXISTS position_targets;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS competencies;
DROP TABLE IF EXISTS user_managers;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    pass TEXT,
    role TEXT,
    name TEXT,
    position TEXT,
    special_expertise TEXT,
    special_expertise_detail TEXT
);

-- Create user_managers table
CREATE TABLE user_managers (
    user_id TEXT,
    manager_id TEXT
);

-- Create competencies table
CREATE TABLE competencies (
    id SERIAL PRIMARY KEY,
    original_id TEXT,
    name TEXT,
    icon TEXT,
    type TEXT,
    l1 TEXT,
    l2 TEXT,
    l3 TEXT,
    l4 TEXT,
    l5 TEXT,
    competency_group TEXT
);

-- Create positions table
CREATE TABLE positions (
    name TEXT PRIMARY KEY,
    role_response TEXT,
    job_group TEXT
);

-- Create position_targets table
CREATE TABLE position_targets (
    position_name TEXT,
    competency_idx INTEGER,
    target_level INTEGER
);

-- Create user_actuals table
CREATE TABLE user_actuals (
    user_id TEXT,
    competency_idx INTEGER,
    actual_level INTEGER,
    evidence TEXT,
    additional_expectation TEXT,
    learning_topic TEXT,
    eval_date TEXT
);
