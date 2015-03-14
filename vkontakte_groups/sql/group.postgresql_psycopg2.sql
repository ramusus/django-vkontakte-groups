--vkontakte_groups_group_members

CREATE UNIQUE INDEX vkontakte_groups_group_members_time_from_3col_uniq
ON vkontakte_groups_group_members (group_id, user_id, time_from)
WHERE time_from IS NOT NULL;

CREATE UNIQUE INDEX vkontakte_groups_group_members_time_from_2col_uniq
ON vkontakte_groups_group_members (group_id, user_id)
WHERE time_from IS NULL;

CREATE UNIQUE INDEX vkontakte_groups_group_members_time_to_3col_uniq
ON vkontakte_groups_group_members (group_id, user_id, time_to)
WHERE time_to IS NOT NULL;

CREATE UNIQUE INDEX vkontakte_groups_group_members_time_to_2col_uniq
ON vkontakte_groups_group_members (group_id, user_id)
WHERE time_to IS NULL;

-- Foreign Key: user_id_refs_remote_id_c2a7ff93

ALTER TABLE vkontakte_groups_group_members DROP CONSTRAINT user_id_refs_remote_id_c2a7ff93;

--ALTER TABLE vkontakte_groups_group_members
--  ADD CONSTRAINT user_id_refs_remote_id_c2a7ff93 FOREIGN KEY (user_id)
--      REFERENCES vkontakte_users_user (remote_id) MATCH SIMPLE
--      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;
