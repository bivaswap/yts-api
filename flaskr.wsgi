import sys

sys.stdout = sys.stderr
sys.path.insert(0, '/home/ubuntu/notebook/flaskr')

from flaskr import app as application
