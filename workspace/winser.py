import win32serviceutil
import win32service
import win32event
import os
import servicemanager

class python_workspace(win32serviceutil.ServiceFramework):
    _svc_name_ = "python_workspace"
    _svc_display_name_ = "python_workspace"  
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        #win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        path = os.path.abspath(os.path.dirname(__file__))

        while 1:
            # Wait for service stop signal, if I timeout, loop again
            rc = win32event.WaitForSingleObject(self.hWaitStop, 100)
            # Check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                # Stop signal encountered
                servicemanager.LogInfoMsg("python_workspace - STOPPED!")  #For Event Log
                break
            else:
                #what to run
                try:
                    from app import app
                    host='0.0.0.0'
                    app.run(host, 3000)
                    servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, '')) 
                except:
                    rasie("failed")
                #end of what to run

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(python_workspace)