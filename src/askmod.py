import math
import random
import sys
from ast import literal_eval as make_tuple
import matplotlib

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
        r = open("results.csv", "w")
        r.write("Modulation:;Orders:;Amplitudes:;Input size:;SNR:;BER [%]:\n")
        for line in data:
            if line.__len__() > 0:
                line = line.split(';')[0].strip()
                arguments = line.split(' ')
                input_len = int(arguments[1])
                inputs = [random.choice([0, 1]) for _ in range(input_len)]
                if arguments[0] == 'APSK':
                    orders = make_tuple(arguments[3])
                    amplitudes = make_tuple(arguments[4])
                    if len(arguments) > 5:
                        phase_offset = make_tuple(arguments[5])
                        modulation = komm.APSKModulation(orders, amplitudes, phase_offset)
                    else:
                        modulation = komm.APSKModulation(orders, amplitudes)
                    # print("------------APSK-modulation------------")
                    r.write("APSK;")
                elif arguments[0] == 'ASK':
                    orders = int(arguments[3])
                    amplitudes = float(arguments[4])
                    modulation = komm.ASKModulation(orders, amplitudes)
                    # print("------------ASK-modulation------------")
                    r.write("ASK;")
                elif arguments[0] == 'PSK':
                    orders = int(arguments[3])
                    amplitudes = float(arguments[4])
                    modulation = komm.PSKModulation(orders, amplitudes)
                    # print("------------PSK-modulation------------")
                    r.write("PSK;")
                else:
                    continue
                err_sum = 0.0
                channel = komm.AWGNChannel(arguments[2])
                for j in range(100):
                    modulated = modulation.modulate(inputs)
                    transmitted = channel(modulated)
                    demodulated = modulation.demodulate(transmitted)
                    errors = 0
                    for d, i in zip(demodulated, inputs):
                        if d != i:
                            errors += 1
                    error_rate = errors / input_len * 100
                    err_sum += error_rate
                error_rate = err_sum / 100
                # print(f"Orders: {orders}")
                # print(f"Amplitudes: {amplitudes}")
                # print(f"Input size: {input_len}")
                # print(f"Signal to noise ratio: {arguments[2]}")
                # print(f"Error rate: {round_half_up(error_rate, 2)}%")
                r.write(f"{orders};{amplitudes};{input_len};{arguments[2]};{round_half_up(error_rate, 2)}\n")
    f.close()
    r.close()


modulations_testing()
