from helper.database import DatabaseHelper
from model.user import User
from model.group import Group

dbsession = DatabaseHelper.session()

import code
code.interact(local=locals())