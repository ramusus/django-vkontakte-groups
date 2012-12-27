# -*- coding: utf-8 -*-
from celery.task import Task

class VkontakteGroupUpdateUsersM2M(Task):
    def run(self, group, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info(u'VK group "%s" users m2m relations updating started' % group)
        try:
            group.update_users_m2m()
            logger.info(u'VK group "%s" users m2m relations succesfully updated' % group)
        except:
            logger.error(u'Unknown error while updating users m2m relations of VK group "%s"' % group)