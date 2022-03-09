# importing os module
import os

# Get the value of 'HOME'
# environment variable
key = 'HOME'
value = os.getenv(key)

# Print the value of 'HOME'
# environment variable
print("Value of 'HOME' environment variable :", value)

# Get the value of 'JAVA_HOME'
# environment variable
key = 'JAVA_HOME'
value = os.getenv(key)

# Print the value of 'JAVA_HOME'
# environment variable
print("Value of 'JAVA_HOME' environment variable :", value)

key = 'home'
value = os.getenv(key)

# Print the value of 'home'
# environment variable
print("Value of 'home' environment variable :", value)

# Python program to explain os.getenv() method

# importing os module
import os

# Get the value of 'home'
# environment variable
key = 'home'
value = os.getenv(key, "geass")

# Print the value of 'home'
# environment variable
print("Value of 'home' environment variable :", value)


from werkzeug.security import generate_password_hash,check_password_hash
passhash=generate_password_hash("cat")
print(passhash)
print(check_password_hash(passhash,"cat"))
print(check_password_hash(passhash,"dog"))

from sqlalchemy import extract
from kkblog.models import Admin, Post, Category, Comment, Link


import datetime
print(datetime.datetime(2006,1,2,13,4,5))

post = Post(
            title="成功",
            body="人生，人生",
            category_id=1,
            timestamp=datetime.datetime(2006,1,2,13,4,5)
        )

import sqlalchemy as sa

z = Post.query.group_by(sa.func.strftime("%Y")).all()

from kkblog.extensions import bootstrap, db

sql_year_count="SELECT count(*) from post GROUP BY strftime('%Y', timestamp)"
sqll="SELECT DISTINCT strftime('%Y', timestamp)  as year from post"

kkl=db.session.execute(sqll)
kk_count=db.session.execute(sql_year_count)