from DataFromFile import FileData
from Analysis import Static, Modal
from Results import Results
data = FileData("data.txt")
a1 = Static(data)
a2 = Modal(data)
r1 = Results(a2)
r1.plot_mode_deformations(mode=3, scale=0.1)








