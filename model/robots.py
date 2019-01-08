import leancloud
import config.leancloud
from leancloud_better_storage.storage.models import Model
from leancloud_better_storage.storage.fields import Field
from datetime import datetime



class Robots(Model):
    leancloud.init(config.leancloud.APP_ID, config.leancloud.APP_KEY)

    name = Field()
    desc = Field(default='')
    tags = Field(default='')
    app_id = Field()
    app_code = Field()
    author = Field()
    wechat = Field()
    email = Field()
    verified = Field(default=False)
    score_avg = Field(default=0)
    rating_num = Field(default=0)
    search_num = Field(default=0)
    publish_at = Field(default=datetime.now())


    @staticmethod
    def add(**kwargs):
        robot = Robots.create(**kwargs)
        robot.commit()

    @staticmethod
    def find(**kwargs):
        robot = Robots.query().filter_by(**kwargs).first()
        return robot

    @staticmethod
    def search(keyword):
        robots = leancloud.Object.extend('Robots')
        query_name = robots.query.contains('name', keyword)
        query_tags = robots.query.contains('tags', keyword)
        query_desc = robots.query.contains('desc', keyword)
        return leancloud.Query.or_(query_name, query_tags, query_desc).limit(10).find()

    @staticmethod
    def hot():
        return Robots.query().order_by(Robots.search_num.desc).find(limit=10)

    @staticmethod
    def new():
        return Robots.query().order_by(Robots.created_at.desc).find(limit=10)

    @staticmethod
    def top():
        return Robots.query().order_by(Robots.score_avg.desc).find(limit=10)


    @staticmethod
    def update(target_robot, **kwargs):
        for k, v in kwargs.items():
            setattr(target_robot, k, v)

        target_robot.commit()


    @staticmethod
    def searched(target_robot):
        search_num = target_robot.search_num
        Robots.update(target_robot, search_num=search_num+1)


    @staticmethod
    def delete(r):
        r.drop()




# robot_str_tmp = '\n\nName:{name}\nCode:{app_code}\nTags:{tags}\nDescription:{desc}'
# reply_robot_code = '\nReply {Code} will send you Robot Contact Card'
#
# realData = '乌云'
# s_list = Robots.search(keyword=realData)
#
# reply_str = 'Mixin Robots Search Results : ' + realData
#
#
# for r in s_list:
#     reply_str += robot_str_tmp.format(name=r.get('name'), app_code=r.get('app_code'),
#                                       tags=r.get('tags'), desc=r.get('desc'))
#
# print(reply_str)