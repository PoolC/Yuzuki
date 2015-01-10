CREATE VIEW `reply_sphinx` AS SELECT
`reply`.`uid` AS `uid`,
`reply`.`article_id` AS `article_id`,
`board`.`uid` AS `board_id`,
`reply`.`content` AS `content`
FROM ((`reply` JOIN `article`) JOIN `board`)
WHERE ((`reply`.`article_id` = `article`.`uid`)
AND (`article`.`board_id` = `board`.`uid`)
AND (`reply`.`enabled` = 1));