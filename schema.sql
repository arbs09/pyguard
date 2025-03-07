CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY, 
    user_name TEXT, 
    first_seen DATE, 
    last_seen DATE
);

CREATE TABLE IF NOT EXISTS global_xp (
    user_id TEXT PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS server_xp (
    user_id TEXT,
    server_id TEXT,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, server_id)
);

CREATE TABLE IF NOT EXISTS statuses (
    type TEXT,
    status TEXT,
    PRIMARY KEY (type, status)
);

CREATE TABLE IF NOT EXISTS bot_owners (
    user_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS bad_users (
    user_id TEXT PRIMARY KEY,
    reason TEXT
);

CREATE TABLE IF NOT EXISTS bad_servers (
    server_id TEXT PRIMARY KEY,
    reason TEXT
);

CREATE TABLE IF NOT EXISTS server_settings (
    server_id TEXT,
    parm TEXT,
    value TEXT,
    PRIMARY KEY (server_id, parm)
);

CREATE TABLE IF NOT EXISTS server_whitelist (
    server_id TEXT,
    user_id TEXT,
    PRIMARY KEY (server_id, user_id)
);

CREATE TABLE IF NOT EXISTS server_default_settings (
    parm TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS channel_settings (
    server_id TEXT,
    channel_id TEXT,
    type TEXT,
    value TEXT,
    PRIMARY KEY (server_id, channel_id, type)
);