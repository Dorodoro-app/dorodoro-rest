CREATE TABLE "active_pomodoro"(
    "user_id" INTEGER NOT NULL,
    "is_active" BOOLEAN NOT NULL
);

ALTER TABLE
    "active_pomodoro" ADD PRIMARY KEY("user_id");
CREATE TABLE "current_pomodoro"(
    "user_id" INTEGER NOT NULL,
    "pomodoro_id" INTEGER NOT NULL
);

ALTER TABLE
    "current_pomodoro" ADD PRIMARY KEY("user_id");

CREATE TABLE "pomodoro"(
    "user_id" INTEGER NOT NULL,
    "pomodoro_id" SERIAL PRIMARY KEY,
    "status" VARCHAR(255),
    "start_time" TIMESTAMP(0) WITHOUT TIME ZONE,
    "stop_time" TIMESTAMP(0) WITHOUT TIME ZONE,
    "length" INTEGER,
    "time_elasped" INTEGER,
    "Date" DATE,
    "type" VARCHAR(255),
    "task_id" VARCHAR(255)
);
--  DROP table pomodoro; 
CREATE TABLE "status"(
    "stopped" INTEGER NOT NULL,
    "running" INTEGER NOT NULL,
    "paused" INTEGER NOT NULL,
    "completed" INTEGER NOT NULL
);