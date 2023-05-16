from log import Logger
import os
import platform
import ctypes
import sys

class Common():
    def __init__(self, log_name:str):
        """
         Initialize the logger. This is called by __init__ and should not be called directly. You should use this instead
         
         @param log_name - The name of the logger
        """
        self.log = Logger(log_name)
        
    def get_free_space_mb(self, dirname):
        """
         Get free space in MB for a directory. This is based on statvfs on the file system
         
         @param dirname - Name of directory to check
         
         @return Free space in MB or 0 on error ( not found or too big to be considered a free space
        """
        try:
            # Total free space in bytes of the file.
            if platform.system() == 'Windows':
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
                return free_bytes.value / 1024 / 1024
            else:
                st = os.statvfs(dirname)
                return st.f_bavail * st.f_frsize / 1024 / 1024
        except:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.log.getLogger().error('ERRO DURANTE EXECUÇÃO na FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.get_free_space_mb.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace("\n", " ")))
            
        
    def create_folder(self, name, dirname):
        """
         Creates a folder if it doesn't exist. It checks if the folder exists and if it doesn't it creates it
         
         @param name - Name of the folder to create
         @param dirname - Directory where the folder will be created. It is used to create the folder
         
         @return Full path of the
        """
        
        try:
            name = name.replace(':', ' - ')
            directory = os.listdir(dirname)
            complete = os.path.join(dirname, name)
            # print(complete)
            # Check if file exists in directory or not
            if(name not in directory):
                # Create a directory if it doesn t exist.
                if not os.path.isdir(complete):
                    os.mkdir(complete)
                    return complete
                return complete
            else:
                return complete
        except Exception as err:
            exc_type, exc_tb = sys.exc_info()[0], sys.exc_info()[-1]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.log.getLogger().error('ERRO DURANTE EXECUÇÃO na FUNÇÃO {}: TIPO - {} - ARQUIVO - {} - LINHA - {} - MESSAGE:{}'.format(self.create_folder.__name__, exc_type, fname, exc_tb.tb_lineno, exc_type.__doc__.replace("\n", " ")))
            