import socket
import subprocess
import argparse

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server",
	help="address for the locket to be binded", default = '0.0.0.0')
ap.add_argument("-p", "--player",
	help="the currently used player", default = 'vlc')
args = vars(ap.parse_args())

server_socket = socket.socket()
server_socket.bind((args['server'], 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    # Run a viewer with an appropriate command line. Uncomment the mplayer
    # version if you would prefer to use mplayer instead of VLC
    if args['player'] == 'vlc':
        cmdline = ['vlc', '--demux', 'h264', '-']
    if args['player'] == 'mplayer':    
        cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    while True:
        # Repeatedly read 1k of data from the connection and write it to
        # the media player's stdin
        data = connection.read(1024)
        if not data:
            break
        player.stdin.write(data)
finally:
    connection.close()
    server_socket.close()
    player.terminate()

