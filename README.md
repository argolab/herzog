herzog
======

a fresh and green argobbs 

```
delete.py    : deltopic    -- 2
delete.py    : delreply    -- 2
new.py       : topic       -- 2
new.py       : reply       -- 2
new.py       : comment     -- 2
postship.py  : upvote      -- 2
postship.py  : unvote      -- 2
postship.py  : star        -- 2
postship.py  : unstar      -- 2
postship.py  : setv        -- 2
query.py                   -- 0
   .fresh
   .list
   .read
update.py                  -- 0
```

```
#mod firebird.new          -- 2
             .mail         -- 0
                .send
                .reply
                .del
                .list
             .queryuser    -- 0
#mod notifiy               -- 0
        .push
        .list
#mod picture               -- 0
        .keep
        .store
#mod 
```

```
#views                     
/ajax/login                -- 2
/ajax/logout               -- 2
/ajax/profile              -- 0
/fresh
/b/<boardname>
/t/<tid>?r=<rid>
/mail
/notification
/u/<userid>
```
