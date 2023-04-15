import socket


def doAssociatedAction(gesture: int):
    match gesture:
        case 0:
            return
        case 1:
            action1()
        case 2:
            action2()


def action1():
    sendSignalThroughTCP(1)


def action2():
    sendSignalThroughTCP(0)


def sendSignalThroughTCP(signal):
    host = socket.gethostname()
    port = 5001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    if signal == 1:
        s.sendall(b'D')
    else:
        s.sendall(b'A')
    s.close()
