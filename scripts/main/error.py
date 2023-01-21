import traceback

from scripts.main.pygameElements import PygameNotification


def raiseError(Exception: Exception):
    PygameNotification("Unhandled Error [ {} ]".format(Exception), 5000).show()
    with open("logs/runtime.log", "a+") as f:
        f.write("\n[ERROR] UNHANDLED !!! | {} "
                "\n{}".format(Exception, traceback.format_exc()))
