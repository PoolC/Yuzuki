from helper.database import DatabaseHelper
from model.user import User
from model.group import Group

DatabaseHelper.create_all()
dbsession = DatabaseHelper.session()

user_foo = User("foo", "foohoo", "foopass", "fooreal", "foo@foo.com", None, None, None, None)
user_bar = User("bar", "barhoo", "barpass", "barreal", "bar@bar.com", None, None, None, None)
user_baz = User("baz", "bazhoo", "bazpass", "bazreal", "baz@baz.com", None, None, None, None)
dbsession.add(user_foo)
dbsession.add(user_bar)
dbsession.add(user_baz)

group_foo = Group("gfoo")
group_bar = Group("gbar")
group_baz = Group("gbaz")
dbsession.add(group_foo)
dbsession.add(group_bar)
dbsession.add(group_baz)

group_foo.users.append(user_foo)
group_foo.users.append(user_bar)
group_foo.users.append(user_baz)

group_bar.users.append(user_bar)
group_bar.users.append(user_baz)

group_baz.users.append(user_baz)

dbsession.commit()

import code
code.interact(local=locals())