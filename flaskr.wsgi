import sys

sys.stdout = sys.stderr
sys.path.insert(0, '/home/ubuntu/notebook/yts-api')

from app import app as application
