import leancloud
import config.leancloud
from leancloud_better_storage.storage.models import Model
from leancloud_better_storage.storage.fields import Field
from datetime import datetime

class MixinUser(Model):
    leancloud.init(config.leancloud.APP_ID, config.leancloud.APP_KEY)
    mixin_id = Field()
    name = Field()
    avatar = Field()
    # created_at = Field(default=datetime.now())

    @staticmethod
    def add(**kwargs):
        user = MixinUser.create(**kwargs)
        user.commit()

    @staticmethod
    def find(**kwargs):
        user = MixinUser.query().filter_by(**kwargs).first()
        return user

    @staticmethod
    def list():
        return MixinUser.query().order_by(MixinUser.created_at.desc).find(limit=10)

    @staticmethod
    def delete(m):
        m.drop()

# m = MixinUser.add(name='lee44c1', mixin_id='3553', avatar='dd324dddf')
# l = MixinUser.list()
# for mm in l:
#     print(mm.name, mm.created_at)