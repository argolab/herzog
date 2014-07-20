AUTHOR     = 1
REPLY      = 1 << 1
COMMENT    = 1 << 2
STAR       = 1 << 3
UPVOTE     = 1 << 4
BAN        = 1 << 5
REPORT     = 1 << 6


NEWPOST    = AUTHOR | STAR 
SPEAK      = AUTHOR | REPLY | COMMENT
