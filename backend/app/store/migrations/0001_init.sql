CREATE TABLE IF NOT EXISTS teams (
    team_id INT PRIMARY KEY,
    key VARCHAR(8),
    name VARCHAR(64),
    city VARCHAR(64)
);
CREATE TABLE IF NOT EXISTS players (
    player_id INT PRIMARY KEY,
    name VARCHAR(128),
    team VARCHAR(8),
    position VARCHAR(8),
    active BOOLEAN
);
CREATE TABLE IF NOT EXISTS games (
    game_key VARCHAR(32) PRIMARY KEY,
    season INT, week INT,
    date_utc TIMESTAMP,
    home_team VARCHAR(8), away_team VARCHAR(8)
);
CREATE TABLE IF NOT EXISTS player_week (
    id SERIAL PRIMARY KEY,
    player_id INT,
    game_key VARCHAR(32),
    season INT, week INT,
    team VARCHAR(8), opp VARCHAR(8), position VARCHAR(8),
    pass_yds FLOAT, pass_td FLOAT, interceptions FLOAT,
    rush_att FLOAT, rush_yds FLOAT, rush_td FLOAT,
    targets FLOAT, receptions FLOAT, rec_yds FLOAT, rec_td FLOAT,
    fumbles_lost FLOAT,
    ppr FLOAT, half_ppr FLOAT,
    created_at TIMESTAMP,
    UNIQUE(player_id, season, week)
);
CREATE TABLE IF NOT EXISTS injuries (
    id SERIAL PRIMARY KEY,
    player_id INT, season INT, week INT,
    status VARCHAR(32), practice VARCHAR(32)
    );
    CREATE TABLE IF NOT EXISTS depth_chart (
    id SERIAL PRIMARY KEY,
    team_id INT, player_id INT, position VARCHAR(12), depth_order INT
);