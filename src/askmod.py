import random
import komm

input_len = 10000
#INPUT = [0, 1, 0, 0, 0, 1, 0, 1]
INPUT = [random.choice([0, 1]) for _ in range(input_len)]

ask = komm.ASKModulation(4)
channel = komm.AWGNChannel(1.0)

#print(f'TRANSMITTING: {INPUT}')
modulated = ask.modulate(INPUT)
transmitted = channel(modulated)

demodulated = ask.demodulate(transmitted)
#print(f'RECEIVED: {demodulated}')

#print(modulated)
#print(transmitted)
errors = 0
for d, i in zip(demodulated, INPUT):
    if d != i:
        errors += 1
    #print(f"{d}, {i}")
error_rate = errors/input_len * 100
print(f"{error_rate}%")
