AUTHOR     = 1
REPLY      = 1 << 1
COMMENT    = 1 << 2
STAR       = 1 << 3
UPVOTE     = 1 << 4
BAN        = 1 << 5
REPORT     = 1 << 6
THANKS     = 1 << 7

NEWPOST    = AUTHOR | STAR 
SPEAK      = AUTHOR | REPLY | COMMENT

#---------- TOPIC FLAG -------------

T_RECOMMEN     = 1 << 3
T_REPORT       = 1 << 4
T_DELETE       = 1 << 5

#---------- POST FLAG ---------------

P_NOREPLY    = 1 << 2
P_DELETE     = 1 << 3

not_any = lambda a, b : (a | b) == 0
set_flag = lambda a, b : a | b
