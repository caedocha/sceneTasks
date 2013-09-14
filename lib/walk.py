import helpers
import pprint as pp

d = helpers.DirHandler().init(None)
pp.pprint(d.list_assets("./scenes"))
