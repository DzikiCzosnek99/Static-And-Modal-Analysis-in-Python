from DataFromFile import FileData
from Analysis import Static, Modal
from Results import Results

data = FileData("data.txt")
a1 = Static(data)
r1 = Results(a1)
r1.plot_deformations()
r1.plot_deformations(scale=50)
a2 = Modal(data)
r2 = Results(a2)
r2.plot_mode_deformations(mode=1, scale=0.1)
r2.plot_mode_deformations(mode=2, scale=0.1)
r2.plot_mode_deformations(mode=3, scale=0.1)
r2.plot_mode_deformations(mode=4, scale=0.1)
r2.plot_mode_deformations(mode=5, scale=0.1)
r2.plot_mode_deformations(mode=6, scale=0.1)
r2.plot_mode_deformations(mode=7, scale=0.1)


