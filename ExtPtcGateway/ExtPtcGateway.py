'''
Created on 12.02.2015

@author: f.uhlenbruck
'''
from gui.c_mainFrame import c_mainFrame

if __name__ == '__main__':
    app = c_mainFrame()
    app.mainloop()

    try:
        app.destroy()
        app.quit()
    except:
        pass
    pass
