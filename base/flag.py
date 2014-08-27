OWNER   = 1
REPLY      = 1 << 1
COMMENT    = 1 << 2
STAR       = 1 << 3
UPVOTE     = 1 << 4
BAN        = 1 << 5
REPORT     = 1 << 6
THANKS     = 1 << 7

SPEAK      = OWNER | REPLY | COMMENT

not_any = lambda a, b : (a | b) == 0
set_flag = lambda a, b : a | b

has_star = lambda a : a & STAR > 0
has_upvote = lambda a : a & UPVOTE > 0

