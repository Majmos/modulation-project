import komm

INPUT = [0, 1, 0, 0, 0, 1, 0, 1]

ask = komm.ASKModulation(4)
channel = komm.AWGNChannel(50.0)

print(f'TRANSMITTING: {INPUT}')
modulated = ask.modulate(INPUT)
transmitted = channel(modulated)

demodulated = ask.demodulate(transmitted)
print(f'RECEIVED: {demodulated}')
