import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

ARN = config.get("IAM_ROLE", "ARN")
LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")


# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table"
user_table_drop = "DROP TABLE IF EXISTS user_table"
song_table_drop = "DROP TABLE IF EXISTS song_table"
artist_table_drop = "DROP TABLE IF EXISTS artist_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES
staging_events_table_create= """
    CREATE TABLE staging_events (
        artist VARCHAR,
        auth VARCHAR,
        first_name VARCHAR,
        gender CHAR,
        item_in_session INTEGER,
        last_name VARCHAR,
        length DECIMAL,
        level VARCHAR,
        location VARCHAR,
        method VARCHAR,
        page VARCHAR,
        registration VARCHAR,
        session_id INTEGER NOT NULL SORTKEY DISTKEY,
        song VARCHAR,
        status INTEGER,
        ts TIMESTAMP,
        user_agent VARCHAR,
        user_id INTEGER
    )
"""

staging_songs_table_create = """
    CREATE TABLE staging_songs (
        num_songs INTEGER,
        artist_id VARCHAR PRIMARY KEY,
        artist_latitude DECIMAL,
        artist_location VARCHAR,
        artist_longitude DECIMAL,
        artist_name VARCHAR,
        song_id VARCHAR NOT NULL,
        title VARCHAR,
        duration DECIMAL,
        year INTEGER
    )
"""

songplay_table_create = """
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id INTEGER IDENTITY(0,1) SORTKEY,
        start_time TIMESTAMP NOT NULL,
        user_id INTEGER NOT NULL DISTKEY,
        level VARCHAR NOT NULL,
        song_id VARCHAR NOT NULL,
        artist_id VARCHAR NOT NULL,
        session_id INTEGER NOT NULL NOT NULL,
        location VARCHAR,
        user_agent VARCHAR
    )
"""

user_table_create = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER NOT NULL SORTKEY,
        first_name VARCHAR,
        last_name VARCHAR,
        gender CHAR,
        level VARCHAR
    )
    """

song_table_create = """
    CREATE TABLE IF NOT EXISTS songs (
        song_id VARCHAR NOT NULL SORTKEY,
        title VARCHAR NOT NULL,
        artist_id VARCHAR NOT NULL,
        year INTEGER NOT NULL,
        duration DECIMAL NOT NULL
    )
"""

artist_table_create = """
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR NOT NULL SORTKEY,
        name VARCHAR,
        location VARCHAR,
        latitude DECIMAL,
        longitude DECIMAL
    )
"""

time_table_create = """
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP NOT NULL SORTKEY, 
        year INTEGER, 
        month INTEGER, 
        week INTEGER, 
        day INTEGER, 
        hour INTEGER, 
        weekday INTEGER
    )
"""

# STAGING TABLES
staging_events_copy = """
    COPY staging_events FROM {}
    CREDENTIALS 'aws_iam_role={}'
    FORMAT AS JSON {}
    TIMEFORMAT as 'epochmillisecs'
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
    COMPUPDATE OFF
    REGION 'us-west-2'
""".format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = """
    COPY staging_songs FROM {}
    CREDENTIALS 'aws_iam_role={}'
    JSON 'auto'
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
    COMPUPDATE OFF
    REGION 'us-west-2'
""".format(SONG_DATA, ARN)

# FINAL TABLES
songplay_table_insert = """
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT ts, se.user_id, se.level, s.song_id, s.artist_id, se.session_id, se.location, se.user_agent 
    FROM staging_events as se
    JOIN staging_songs as s ON se.artist = s.artist_name
    WHERE se.page = 'NextSong'
"""

user_table_insert = """
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT user_id, first_name, last_name, gender, level
    FROM staging_events
    WHERE page = 'NextSong'
"""

song_table_insert = """
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT song_id, title, artist_id, year, duration
    FROM staging_songs
    WHERE song_id IS NOT NULL
"""

artist_table_insert = """
    INSERT INTO artists(artist_id, name, location, latitude, longitude)
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL
"""

time_table_insert = """
    INSERT INTO time(start_time, year, month, week, day, hour, weekday)
    SELECT DISTINCT ts,
    EXTRACT(year FROM ts),
    EXTRACT(month FROM ts),
    EXTRACT(week FROM ts),
    EXTRACT(day FROM ts),
    EXTRACT(hour FROM ts),
    EXTRACT(weekday FROM ts)
    FROM staging_events
    WHERE page = 'NextSong'
    AND ts IS NOT NULL
"""

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
