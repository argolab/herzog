CREATE TABLE `herzog_cms_page` (
      `pid` int(11) unsigned NOT NULL auto_increment,
      `pagepath` varchar(40) NOT NULL,
      `pagename` varchar(40) NOT NULL,
      `tpl` varchar(40) NOT NULL,
      `rid` varchar(40) NOT NULL,
      `lastupdate` timestamp NOT NULL default CURRENT_TIMESTAMP
                  on update CURRENT_TIMESTAMP,
      `lastuserid` varchar(20) NOT NULL,
      
      PRIMARY KEY (pid),
      KEY (pagepath),
      KEY (rid),
      KEY (lastupdate),
      KEY (lastuserid)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8 ;
       
CREATE TABLE `herzog_cms_resource` (
      `rid` int(11) unsigned NOT NULL auto_increment,
      `resname` varchar(40) NOT NULL,
      `lastupdate` timestamp NOT NULL default CURRENT_TIMESTAMP
                  on update CURRENT_TIMESTAMP,
      `lastuserid` varchar(20) NOT NULL,

      `ds` text NOT NULL,

      PRIMARY KEY (rid),
      KEY (resname),
      KEY (lastupdate),
      KEY (lastuserid)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8 ;
