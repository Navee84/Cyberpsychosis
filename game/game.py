import sys
import os
sys.path.append(os.path.dirname(__file__)) 


from main import *

DEBUG = True

game = Main()

if DEBUG :

    import threading
    import code

    def start_console():
        code.interact(local=globals())

    thread_console = threading.Thread(target=start_console, daemon=True)
    thread_console.start()

pyglet.app.run(1/45)