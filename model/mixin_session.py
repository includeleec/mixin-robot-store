import leancloud
import config.leancloud
from leancloud_better_storage.storage.models import Model
from leancloud_better_storage.storage.fields import Field
from datetime import datetime

WAIT_TO_ACTION = 10

class MixinSession(Model):

    leancloud.init(config.leancloud.APP_ID, config.leancloud.APP_KEY)
    user_id = Field()
    action_in = Field()
    app_id = Field()
    created_timestamp = Field(default=datetime.now().timestamp())

    @staticmethod
    def add(**kwargs):
        session = MixinSession.create(**kwargs)
        session.commit()

    @staticmethod
    def find(**kwargs):
        session = MixinSession.query().order_by(MixinSession.created_at.desc).filter_by(**kwargs).first()
        return session

    @staticmethod
    def get_app_id(user_id, action_in):
        r = MixinSession.find(user_id=user_id, action_in=action_in)
        if r:
            return r.app_id
        else:
            return False

    @staticmethod
    def inAction(user_id,  action_in, **kwargs):
        s = MixinSession.find(user_id=user_id)
        if s is not None:
            if s.action_in != action_in:

                MixinSession.delete(s)
                MixinSession.add(user_id=user_id, action_in=action_in, created_timestamp=datetime.now().timestamp(), **kwargs)

                print(user_id + ' add action_in ' + action_in)


            else:
                s.created_timestamp = datetime.now().timestamp()
                s.commit()

                print(user_id + ' update action_in ' + action_in)
        else:
            MixinSession.add(user_id=user_id, action_in=action_in, created_timestamp=datetime.now().timestamp(), **kwargs)
            print(user_id + ' add action_in ' + action_in)

    @staticmethod
    def isInAction(user_id, action_in):
        s = MixinSession.find(user_id=user_id)
        if s is not None:
            if s.action_in != action_in:
                # MixinSession.delete(s)
                return False
            else:
                delta_time = datetime.now().timestamp() - s.created_timestamp
                print(delta_time)
                if delta_time < WAIT_TO_ACTION:
                    print(action_in + ' is in action')
                    return True
                else:
                    print('wait to long')
                    return False
        else:
            return False


    @staticmethod
    def delete(m):
        m.drop()

#
# MixinSession.inAction(user_id='d33f7efd-4b0b-41ff-baa3-b22ea40eb44f', action_in='search')
#
# s = MixinSession.find(user_id='d33f7efd-4b0b-41ff-baa3-b22ea40eb44f')
# print(s)
#
# ina = MixinSession.isInAction(user_id='d33f7efd-4b0b-41ff-baa3-b22ea40eb44f', action_in='search')
# print(ina)


# if MixinSession.isInAction(user_id='d33f7efd-4b0b-41ff-baa3-b22ea40eb44f', action_in='search'):
#     print('type:' + 'kkk')

# user_id = 'd33f7efd-4b0b-41ff-baa3-b22ea40eb44f'
# MixinSession.inAction(user_id=userId, action_in='search')
# MixinSession.inAction(user_id=userId, action_in='app_code')

# MixinSession.add(user_id=user_id, action_in='rate_score', created_timestamp=datetime.now().timestamp(), app_id='dfdf')