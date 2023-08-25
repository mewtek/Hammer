CREATE TABLE "user"
(
    user_id bigint NOT NULL PRIMARY KEY,
    user_name varchar(255) NOT NULL UNIQUE
);

CREATE TABLE guild
(
    guild_id bigint NOT NULL PRIMARY KEY,
    guild_name varchar(255) NOT NULL,
    banned boolean NOT NULL DEFAULT false
);

CREATE TABLE guild_settings
(
    id bigint NOT NULL PRIMARY KEY,
    prefix varchar(3) NOT NULL DEFAULT '!',
    max_warns_kick int NOT NULL DEFAULT 3,
    max_warns_ban int NOT NULL DEFAULT 6,
    logging boolean NOT NULL DEFAULT false,
    log_channel bigint,
    dm_user_on_action boolean NOT NULL DEFAULT false,
    muted_role_id bigint,

    CONSTRAINT guild_settings_id_foreign FOREIGN KEY(id) REFERENCES guild(guild_id)
);

CREATE TABLE "warning"
(
    id serial PRIMARY KEY,
    issued timestamp without time zone NOT NULL,
    issued_by bigint NOT NULL,
    issued_to bigint NOT NULL,
    issued_guild bigint NOT NULL,
    reason varchar(255),

    CONSTRAINT warning_issued_by_foreign FOREIGN KEY(issued_by) REFERENCES "user"(user_id),
    CONSTRAINT warning_issued_to_foreign FOREIGN KEY(issued_to) REFERENCES "user"(user_id),
    CONSTRAINT warning_issued_guild_foreign FOREIGN KEY(issued_guild) REFERENCES guild(guild_id)
);

CREATE TABLE mute
(
    id serial PRIMARY KEY,
    issued timestamp without time zone NOT NULL,
    issued_by bigint NOT NULL,
    issued_to bigint NOT NULL,
    issued_guild bigint NOT NULL,
    expires timestamp without time zone NOT NULL,
    reason varchar(255),

    CONSTRAINT mute_issued_by_foreign FOREIGN KEY(issued_by) REFERENCES "user"(user_id),
    CONSTRAINT mute_issued_to_foreign FOREIGN KEY(issued_to) REFERENCES "user"(user_id),
    CONSTRAINT mute_issued_guild_foreign FOREIGN KEY(issued_guild) REFERENCES guild(guild_id)
);

CREATE TABLE kick
(
    id serial PRIMARY KEY,
    issued timestamp without time zone NOT NULL,
    issued_by bigint NOT NULL,
    issued_to bigint NOT NULL,
    issued_guild bigint NOT NULL,
    reason varchar(255),

    CONSTRAINT kick_issued_by_foreign FOREIGN KEY(issued_by) REFERENCES "user"(user_id),
    CONSTRAINT kick_issued_to_foreign FOREIGN KEY(issued_to) REFERENCES "user"(user_id),
    CONSTRAINT kick_issued_guild_foreign FOREIGN KEY(issued_guild) REFERENCES guild(guild_id)
);

CREATE TABLE ban
(
    id serial PRIMARY KEY,
    issued timestamp without time zone NOT NULL,
    issued_by bigint NOT NULL,
    issued_to bigint NOT NULL,
    issued_guild bigint NOT NULL,
    expires timestamp without time zone NOT NULL DEFAULT '2269-01-01 00:00:00'::timestamp without time zone,
    reason varchar(255),

    CONSTRAINT ban_issued_by_foreign FOREIGN KEY(issued_by) REFERENCES "user"(user_id),
    CONSTRAINT ban_issued_to_foreign FOREIGN KEY(issued_to) REFERENCES "user"(user_id),
    CONSTRAINT ban_issued_guild_foreign FOREIGN KEY(issued_guild) REFERENCES guild(guild_id)
);