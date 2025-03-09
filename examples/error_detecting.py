import sys
sys.path.append("../")
from utils.edit_distance import Hamming

data_sent = "01101110"
data_received = "11101010"

solver = Hamming()
print(solver(data_sent, data_received))

