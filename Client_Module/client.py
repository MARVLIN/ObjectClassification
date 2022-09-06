from websocket import create_connection

def listen():

    # Connect to WebSocket API and subscribe to trade feed for XBT/USD and XRP/USD
    ws = create_connection("ws://23.254.176.188:8080")
    ws.send('Ready for capture')

    # Infinite loop waiting for WebSocket data
    count = 0
    msg = ws.recv()
    print(msg)
    if msg != 'snap':
        return True
    else:
        print('error')

def scan_complete():

    ws = create_connection("ws://23.254.176.188:8080")
    ws.send('stop')
    return True

