CREATE TABLE "user"
(
    id bigint NOT NULL PRIMARY KEY,
    user_name varchar(255) NOT NULL UNIQUE
);

CREATE TABLE guild
(
    id bigint NOT NULL PRIMARY KEY,
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

    CONSTRAINT guild_settings_id_foreign FOREIGN KEY(id) REFERENCES guild(id)
);

CREATE TABLE "warning"
(
    id serial PRIMARY KEY,
    issued timestamp without time zone NOT NULL,
    issued_by bigint NOT NULL,
    issued_to bigint NOT NULL,
    issued_guild bigint NOT NULL,
    reason varchar(255),

    CONSTRAINT warning_issued_by_foreign FOREIGN KEY(issued_by) REFERENCES "user"(id),
    CONSTRAINT warning_issued_to_foreign FOREIGN KEY(issued_to) REFERENCES "user"(id),
    CONSTRAINT warning_issued_guild_foreign FOREIGN KEY(issued_guild) REFERENCES guild(id)
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

    CONSTRAINT mute_issued_by_foreign FOREIGN KEY(issued_by) REFERENCES "user"(id),
    CONSTRAINT mute_issued_to_foreign FOREIGN KEY(issued_to) REFERENCES "user"(id),
    CONSTRAINT mute_issued_guild_foreign FOREIGN KEY(issued_guild) REFERENCES guild(id)
);

CREATE TABLE kick
(
    id serial PRIMARY KEY,
    issued timestamp without time zone NOT NULL,
    issued_by bigint NOT NULL,
    issued_to bigint NOT NULL,
    issued_guild bigint NOT NULL,
    reason varchar(255),

    CONSTRAINT kick_issued_by_foreign FOREIGN KEY(issued_by) REFERENCES "user"(id),
    CONSTRAINT kick_issued_to_foreign FOREIGN KEY(issued_to) REFERENCES "user"(id),
    CONSTRAINT kick_issued_guild_foreign FOREIGN KEY(issued_guild) REFERENCES guild(id)
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

    CONSTRAINT ban_issued_by_foreign FOREIGN KEY(issued_by) REFERENCES "user"(id),
    CONSTRAINT ban_issued_to_foreign FOREIGN KEY(issued_to) REFERENCES "user"(id),
    CONSTRAINT ban_issued_guild_foreign FOREIGN KEY(issued_guild) REFERENCES guild(id)
);

CREATE TABLE ticket
(
    id serial PRIMARY KEY,
    ticket_guild bigint NOT NULL,
    ticket_channel_id bigint NOT NULL,
    user bigint NOT NULL,
    claimed_by bigint,

    CONSTRAINT ticket_guild_foreign FOREIGN KEY(ticket_guild) REFERENCES guild(id),
    CONSTRAINT ticket_user_foreign FOREIGN KEY(user) REFERENCES "user"(id),
    CONSTRAINT claimed_by_foreign FOREIGN KEY(claimed_by) REFERENCES "user"(id)
);