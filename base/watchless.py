import os
import inspect
import os.path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler) :

    def on_modified(self, event):
        filename = event.src_path.split('/')[-1]
        if filename.endswith('.less') :
            print filename
            if filename.startswith("page_") :
                src = "less/%s" % filename
                cssname = filename[5:-5]
                build = "less/build_%s.css" % cssname
                copyto = "static/css/%s.css" % cssname
            else :
                cssname = ''
                src = "less/styles.less"
                build = "less/build.css"
                copyto = "static/css/base.css"
            if os.system("lessc %s > %s" % (src, build)) == 0 :
                os.system("cp %s %s" % (build, copyto))
                print ' * Rebuild css...[%s]' % cssname

def main() :
    print ' * Watch less file...' 
    o = Observer()
    path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'less/')
    o.schedule(MyHandler(), path=path, recursive=True)
    o.start()
