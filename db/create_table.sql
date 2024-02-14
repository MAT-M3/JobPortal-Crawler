CREATE TABLE IF NOT EXISTS job_offers (
	id SERIAL PRIMARY KEY,
	position_id TEXT UNIQUE NOT NULL,
	position_name TEXT,
	searched_position TEXT,
	company TEXT,
	location TEXT,
	wage TEXT,
	portal TEXT,
	link TEXT,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);