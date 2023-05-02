import threading
import requests



def popen_and_call(on_exit, function, inputs_function=None, inputs_on_exit=(None, None, None)):
    """
    Runs the function in a subprocess.Popen, and then calls the function
    on_exit when the function completes.
    on_exit is a callable object, and popen_args is a list/tuple of args that 
    would give to subprocess.Popen.

    :inputs_on_exit: tuple of str, first is back-end API url and second is backend API key and the third is the guildId

    original code src: https://stackoverflow.com/a/2581943/9070986
    """
    def run_in_thread(on_exit, function, inputs_function, inputs_on_exit):
        """
        max_timeout is in seconds, it is a bit more than 24 hours
        """
        function(inputs_function)
        on_exit(inputs_on_exit)
        return
    thread = threading.Thread(target=run_in_thread, args=(on_exit, function, inputs_function, inputs_on_exit))
    thread.start()
    # returns immediately after the thread starts
    return thread

def notify_backend(secrets):
    """
    notify the backend with some json message

    Parameters:
    -------------
    secrets : tuple of string
        length must be 3, the first is url and the second is api key, the third one is guildId
        the url to notify the backend
    
    """
    if len(secrets) == 3:
        ## the message to send when the analytics process ends
        body_obj = {'isInProgress': False}
        url = secrets[0] + '/' + secrets[2]
        
        x = requests.patch(url=url, json= body_obj, headers={'API-Key': str(secrets[1])})
        print(f'Back-end response: {x.status_code}')
    else:
        print('Wrong input for the notify backend function!')
