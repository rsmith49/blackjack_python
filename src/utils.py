import time


start_time = None


def tic():
    """
    Behaves like MATLAB's tic, toc functions -
    call tic() to start timer, then call toc() to print seconds elapsed
    NOTE: Doesn't work with async stuff (obviously)
    :return:
    """
    global start_time
    start_time = time.time()


def toc():
    global start_time
    print(time.time() - start_time)
