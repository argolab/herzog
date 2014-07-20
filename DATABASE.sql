CREATE TABLE `herzog_topic` (

       `tid` int(11) unsigned NOT NULL auto_increment,
       `boardname` varchar(40) NOT NULL,
       `owner` varchar(40) NOT NULL,
       -- `realowner` varchar(40) NOT NULL, -- 匿名版
       `title` varchar(60) NOT NULL,
       `posttime` timestamp NOT NULL ,
       `score` int(40) NOT NULL default 0,         -- 排名
       `lastreply` timestamp NOT NULL,
       `lastcomment` timestamp NOT NULL,

       `replynum` int(40) NOT NULL default 0,
       `partnum` int(40) NOT NULL default 0,

       `upvote` int(11) NOT NULL default 0,
       `fromaddr` varchar(20) NOT NULL,
       `fromapp` varchar(40) NOT NULL default '',   -- 来自哪个app

       `summary` varchar(200) NOT NULL default '',  -- 摘要
       `flag` int(20) NOT NULL default 0,           -- 属性

       `oldfilename` varchar(32) NOT NULL default '',  -- 对应的文件存储文件名

       `content` mediumtext,

       PRIMARY KEY (tid),            -- For :  ORDER BY tid
       KEY (boardname, tid),        -- For :  WHERE boardname= AND tid=
       KEY (boardname, score),      -- For :  WHERE boardname= ORDER BY score
       KEY (score),                  -- For :  ORDER BY score
       KEY (owner),                  -- For :  WHERE owner=
       KEY (boardname, owner),      -- For :  WHERE boardname= AND owner=
       KEY (tid, owner)            -- For :  WHERE tid= AND owner=

)ENGINE=InnoDB DEFAULT CHARSET=UTF8 ;

CREATE TABLE `herzog_reply` (

       `rid` int(11) unsigned NOT NULL auto_increment,

       `tid` int(11) unsigned NOT NULL,
       -- "WHERE tid= " is all post to topic[tid]
       
       `brid` int(11) unsigned NOT NULL,
       -- "WHERE brid=rid" is all post reply to lz, else it is comment
       -- "WHERE tid= ORDER BY brid" load all reply and comment by time

       `replyid` int(11) unsigned NOT NULL,
       -- "WHERE replyid=tid" is all post reply to lz

       `owner` varchar(40) NOT NULL,
       `title` varchar(60) NOT NULL,
       `posttime` timestamp NOT NULL ,

       `lastupdate` timestamp NOT NULL,

       `fromaddr` varchar(20) NOT NULL default '',
       `fromapp` varchar(40) NOT NULL default '',   -- 来自哪个app

       `flag` int(20) NOT NULL default 0,           -- 属性
       `oldfilename` varchar(32) NOT NULL,  -- 对应的文件存储文件名

       `content` mediumtext,

       PRIMARY KEY (rid),               -- FOR : ORDER BY tid
       KEY (tid),                      -- FOR : WHERE tid=
       KEY (brid),                     -- FOR : WHERE brid=
       KEY (tid, brid),               -- FOR : WHERE tid= AND brid=
       KEY (owner)                     -- FOR : ORDER BY owner

)ENGINE=InnoDB DEFAULT CHARSET=UTF8 ;

CREATE TABLE `herzog_postship` (
     `utid` int(11) unsigned NOT NULL auto_increment,

     `userid` varchar(20) NOT NULL,
     `tid` int(11) unsigned NOT NULL,

     `flag` int(11) unsigned NOT NULL,

      PRIMARY KEY (utid),
      KEY (userid),
      KEY (tid),
      KEY (userid, tid)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8 ;
