CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS command_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    input_text TEXT NOT NULL,
    model_output TEXT NOT NULL,
    is_correct BOOLEAN,
    corrected_output TEXT,
    model_name TEXT,
    model_version TEXT,
    feedback_notes TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);