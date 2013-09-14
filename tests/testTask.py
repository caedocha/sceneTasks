from main import TaskDispatcher
from notifier import Notifier
import tasks as t


n = Notifier()
td = TaskDispatcher(["caca","caca","caca"], n)
p = t.Project([], n)

td.initialize_task(p)

p.create()
