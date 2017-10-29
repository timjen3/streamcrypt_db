# streamcrypt_db
this is a toy project to try to make an encrypted data store for embedded applications (as in software lives with the database)
that loads objects from the store one at a time allowing the application to read the object, process it, discard it, and move 
on to the next object.

A simple analogy can be seen by comparing the process of reading a file line by line using Python with an imagination of how
this streamcrypt db would work:

in python currently one can iterate over lines in a file like this:

```
fp = open("my_data.txt", "r")
for line in fp:
  print(line)
```

Imagine this:

```
db = open("my_database.db", mode="r", key=<encryption key>)
for record in db.list("my list1"):
  print(record)
```

the idea is really simple, and can be summed up like this:
* ability to load a list of values with a retrieval name
* ability to call and retrieve stored lists of values by name
* ability to load one object into memory at a time

h4. what makes this harder than you would think

The complexity arises from the need to de-duplicate records. For example, if you have previously written some object
defined by id=1, and want to send a new object defined by id=1 then it should be an update operation instead of a write
operation. The database will need to know where the object defined as id=1 is located and replace it with the new data.
Replacing the data may not mean overwriting the data, it could be updating an index with the new data location, and 
setting a task to clean up the old data location.

h4. some notes about nosql data stores

the main point of nosql is that disk space is no longer a concern therefore let's stop holding back performance with it. 
furthermore, if disk space is no longer a concern let's store large objects instead of tiny representations of data. 
serialize the object (such as with json) and save to disk. this concept is quite powerful on it's own because it's easy to 
imagine systems like that with very little code. there is a definite risk of laziness leading developers down 
paths of generating piles of data simply because they can. After all, you do not need to have any knowledge of relational 
databases to follow such a model. At the far extreme is this idea of recording all data (event stream) and on the other end you
have very wide "tables" with tons of data duplication in your database but no need (and sometimes no ability) to 
join tables to one another. This 'black magic' is definitely working for large organizations and will probably continue to.

this is a special case, because it is not a database that runs as a service in memory.
Here are some examples of what is out there already: https://wiki.python.org/moin/DatabaseInterfaces

I'll do some additional research and probably post notes here.
