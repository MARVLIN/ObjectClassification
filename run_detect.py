import subprocess
#subprocess.run(['python', 'detect.py', '--source', '0', '--weights', 'best.pt', '--view-img'])

def run():
    return subprocess.run(['python', 'detect.py', '--source', '0', '--weights', 'best.pt', '--view-img'])
