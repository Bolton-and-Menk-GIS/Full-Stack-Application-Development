import os
import sys
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(thisDir))
from app.models import engine

engine.execute('pragma integrity_check')