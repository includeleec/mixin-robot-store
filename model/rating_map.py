import leancloud
import config.leancloud
from leancloud_better_storage.storage.models import Model
from leancloud_better_storage.storage.fields import Field
from datetime import datetime

from model.mixin_user import MixinUser
from model.robots import Robots

class RatingMap(Model):
    leancloud.init(config.leancloud.APP_ID, config.leancloud.APP_KEY)

    user_id = Field()
    robot = Field()
    score = Field()

    @staticmethod
    def rating(user_id, app_id, score):

        robot = Robots.find(app_id=app_id)

        robots = leancloud.Object.extend('Robots')
        rating_map = leancloud.Object.extend('RatingMap')

        ratingMap = rating_map()

        ratingMap.set('user_id', user_id)
        ratingMap.set('robot', robots.create_without_data(robot.object_id))
        ratingMap.set('score', score)

        ratingMap.save()

        # caculate Robots score_avg,add rating_num
        r = Robots.find(app_id=app_id)
        print(r.rating_num, r.score_avg)
        rating_num = r.rating_num + 1
        score_avg = (r.score_avg * r.rating_num + score) / rating_num
        Robots.update(r, rating_num=rating_num + 1, score_avg=score_avg)





# RatingMap.rating(user_id='3553', app_id='7000', score=5)