DB CONFIG

TABLE: POMODORO
timer_id
user_id
task_id
start_time
stop_time
length
Status
time_elasped
type
date

TABLE: STATUS_ENUM
Active: 1
Completed: 2
Abandoned: 3
InActive: 4


TABLE: TYPE_ENUM
pomodoro: 1
short_break: 2
long_break: 3

# START ENDPOINT
POST /api/start

INPUT
{
    user_id:
    length:
    type:
    task_id: # NOT REQUIRED
    type:
}

RESPONSE
{
    timer_id
    Status
}

# PAUSE ENDPOINT

PUT /api/pause

{
    timer_id
    current_time
}

I WILL MAKE THE TIMER INACTIVE
{
    timer_id
    time_elasped
    Status
}

# STOP/COMPLETED ENDPOINT

PUT /api/stop

{
    timer_id
    current_time
}
RESPONSE
{
    timer_id
    Status
}

# ABONDED/CANCELED/RESET ENDPOINT

PUT /api/cancel

{
    timer_id
    current_time
}
RESPONSE
{
    timer_id
    Status #Abandoned
}

# HISTORY

GET /api/histroy/?user_id=user_id&?timeline=today

RESPONSE
{
    timeline
    total_pomodoro
    total_pomodoro_time
    length_of_average_pomodoro
    each_pomodor_with_values [{pomodor_id, lenght, date}]
}