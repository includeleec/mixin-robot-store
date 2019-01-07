import leancloud
import config.leancloud
from leancloud_better_storage.storage.models import Model
from leancloud_better_storage.storage.fields import Field
from datetime import datetime

from model.mixin_user import MixinUser
from model.robots import Robots

class RatingMap(Model):
    leancloud.init(config.leancloud.APP_ID, config.leancloud.APP_KEY)

    user = Field()
    robot = Field()
    score = Field()

    @staticmethod
    def rating(mixin_id, app_id, score):

        user = MixinUser.find(mixin_id=mixin_id)
        robot = Robots.find(app_id=app_id)

        robots = leancloud.Object.extend('Robots')
        mixin_user = leancloud.Object.extend('MixinUser')
        rating_map = leancloud.Object.extend('RatingMap')

        ratingMap = rating_map()

        # print(user.object_id)
        # print(robot.object_id)

        ratingMap.set('user', mixin_user.create_without_data(user.object_id))
        ratingMap.set('robot', robots.create_without_data(robot.object_id))
        ratingMap.set('score', score)

        ratingMap.save()




RatingMap.rating(mixin_id='3553', app_id='7000', score=5)