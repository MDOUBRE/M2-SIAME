from os import environ, terminal_size
from random import seed

import sys
sys.path.extend(['/media/storage/camsi4/pyamak-noyau/'])
import pathlib

from pyAmakCore.classes.environment import Environment
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.agent import Agent

import env
import agent
import amas

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.tools.schedulable import Schedulable

envir = env.class_connectee(54)
amass = amas.gestionClasse(envir)

amass.put_token()
amass.start()
