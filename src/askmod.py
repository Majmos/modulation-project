import math
import random
import sys
from ast import literal_eval as make_tuple

import komm


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


def modulations():
    while 1:
        print("-----------MODULATION-PROJECT-----------")
        print("1. ASK modulation")
        print("2. PSK modulation")
        print("3. APSK modulation")
        print("4. Exit")
        action = input()
        input_len = 10000 * 3
        inputs = [random.choice([0, 1]) for _ in range(input_len)]
        if action == '1':
            modulation = komm.ASKModulation(4)
            print("ASK modulation")
        elif action == '2':
            modulation = komm.PSKModulation(4)
            print("PSK modulation")
        elif action == '3':
            modulation = komm.APSKModulation((4, 4), (1.0, 2.0))
            print("APSK modulation")
        elif action == '4':
            sys.exit(0)
        channel = komm.AWGNChannel(1.0)
        modulated = modulation.modulate(inputs)
        transmitted = channel(modulated)
        demodulated = modulation.demodulate(transmitted)
        errors = 0
        for d, i in zip(demodulated, inputs):
            if d != i:
                errors += 1
        error_rate = errors / input_len * 100
        print(f"Input size: {input_len}")
        print(f"Error rate: {error_rate}%")


def modulations_testing():
    with open('config.ini') as f:
        data = f.read().split('\n')
        r = open("results.txt", "w")
    for line in data:
        line = line.split(';')[0].strip()
        arguments = line.split(' ')
        input_len = int(arguments[1])
        inputs = [random.choice([0, 1]) for _ in range(input_len)]
        if arguments[0] == 'APSK':
            orders = make_tuple(arguments[3])
            amplitudes = make_tuple(arguments[4])
            modulation = komm.APSKModulation(orders, amplitudes)
            print("------------APSK-modulation------------")
            print(f"Amplitudes: {amplitudes}")
            r.write(f"Modulation: APSK; Amplitudes: {amplitudes} ")
        elif arguments[0] == 'ASK':
            orders = int(arguments[3])
            modulation = komm.ASKModulation(orders)
            print("------------ASK-modulation------------")
            r.write(f"Modulation: ASK; ")
        elif arguments[0] == 'PSK':
            orders = int(arguments[3])
            modulation = komm.PSKModulation(orders)
            print("------------PSK-modulation------------")
            r.write(f"Modulation: PSK; ")
        else:
            continue
        channel = komm.AWGNChannel(arguments[2])
        modulated = modulation.modulate(inputs)
        transmitted = channel(modulated)
        demodulated = modulation.demodulate(transmitted)
        errors = 0
        for d, i in zip(demodulated, inputs):
            if d != i:
                errors += 1
        error_rate = errors / input_len * 100
        print(f"Orders: {orders}")
        print(f"Input size: {input_len}")
        print(f"Signal to noise ratio: {arguments[2]}")
        print(f"Error rate: {round_half_up(error_rate, 2)}%")
        r.write(f"Orders: {orders}; Input size: {input_len}; SNR: {arguments[2]}; BER: {round_half_up(error_rate, 2)}%\n")
    f.close()
    r.close()


modulations_testing()
