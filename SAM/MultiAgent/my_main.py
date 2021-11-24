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

envir = Classe_connectee(54)
amass = GestionClasse(envir, ExecutionPolicy.ONE_PHASE)

#amass.cycle()

#scheduler = SchedulerIHM(amass)
scheduler = Scheduler(amass)

scheduler.start()
scheduler.run()

