import sys
sys.path.extend(['/media/storage/camsi4/pyamak-noyau/'])
import pathlib

from my_env import Classe_connectee
from my_amas import GestionClasse

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.enumeration.executionPolicy import ExecutionPolicy
from pyAmakCore.classes.tools.schedulable import Schedulable
from pyAmakCore.classes.tools.schedulerIHM import SchedulerIHM
from pyAmakCore.classes.scheduler import Scheduler

print("Rentrez un niveau seuil de luminosité pour al simulation\n")
lum = int(input())
envir = Classe_connectee()
amass = GestionClasse(envir, lum, ExecutionPolicy.ONE_PHASE)

scheduler = Scheduler(amass)

scheduler.start()
scheduler.run()

