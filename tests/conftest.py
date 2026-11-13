import os
import sys
import time
from pathlib import Path

# O JavaScript do site usa a data local. A Action roda em UTC; fixar o fuso do Brasil
# antes de qualquer MiniRacer faz os testes de data local valerem lá também (M1 da 1A).
os.environ["TZ"] = "America/Sao_Paulo"
time.tzset()

sys.path.insert(0, str(Path(__file__).parent))
