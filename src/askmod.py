import math
import random
import sys
from ast import literal_eval as make_tuple
import matplotlib
import numpy as np #for numerical computing
import matplotlib.pyplot as plt #for plotting functions
from scipy.special import erfc #erfc/Q function

import komm


class ReflectionChannel:
    def __init__(self, snr=np.inf, signal_power=1.0):
        self.snr = snr
        self.signal_power = signal_power

    def __call__(self, input_signal):
        input_signal = np.array(input_signal)
        reversed_input = input_signal[::-1]
        size = input_signal.size
        signal_power = self.signal_power
        reflection_power = signal_power / float(self.snr)

        if input_signal.dtype == np.complex128:
            reflection = np.sqrt(reflection_power / 2) * (reversed_input + 1j * np.random.normal(size=size))
        else:
            reflection = np.sqrt(reflection_power) * reversed_input

        return input_signal + reflection


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
        r.write("Modulation:;Orders:;Amplitudes:;Input size:;SNR:;BER [%]:;SER [%]:\n")
        for line in data:
            if line.__len__() > 0:
                line = line.split(';')[0].strip()
                arguments = line.split(' ')
                input_len = int(arguments[1])
                inputs = [random.choice([0, 1]) for _ in range(input_len)]
                if arguments[0] == 'APSK':
                    orders = make_tuple(arguments[3])
                    symbol_len = 0
                    for o in orders:
                        symbol_len += o
                    symbol_len = math.log(symbol_len, 2)
                    amplitudes = make_tuple(arguments[4])
                    if len(arguments) > 5:
                        phase_offset = make_tuple(arguments[5])
                        modulation = komm.APSKModulation(orders, amplitudes, phase_offset)
                    else:
                        modulation = komm.APSKModulation(orders, amplitudes)
                    print("------------APSK-modulation------------")
                    r.write("APSK;")
                elif arguments[0] == 'ASK':
                    orders = int(arguments[3])
                    symbol_len = math.log(orders, 2)
                    amplitudes = float(arguments[4])
                    modulation = komm.ASKModulation(orders, amplitudes)
                    print("------------ASK-modulation------------")
                    r.write("ASK;")
                elif arguments[0] == 'PSK':
                    orders = int(arguments[3])
                    symbol_len = math.log(orders, 2)
                    amplitudes = float(arguments[4])
                    modulation = komm.PSKModulation(orders, amplitudes)
                    print("------------PSK-modulation------------")
                    r.write("PSK;")
                else:
                    continue
                err_sum = 0.0
                sym_err_sum = 0.0
                # channel = komm.AWGNChannel(arguments[2])
                channel = ReflectionChannel(snr=arguments[2])
                # modulated1 = modulation.modulate(inputs)
                # transmitted1 = channel(modulated1)
                # fig, ax1 = plt.subplots(nrows=1, ncols=1)
                # ax1.plot(np.real(transmitted1), np.imag(transmitted1), '*')
                for j in range(1):
                    modulated = modulation.modulate(inputs)
                    transmitted = channel(modulated)
                    demodulated = modulation.demodulate(transmitted)
                    errors = 0
                    symbol_errors = 0
                    index = 0
                    skip_next = False
                    for d, i in zip(demodulated, inputs):
                        if d != i:
                            errors += 1
                        if index % symbol_len == 0:
                            skip_next = False
                        if d != i and skip_next == False:
                            symbol_errors += 1
                            skip_next = True
                        index += 1
                    error_rate = errors / input_len * 100
                    err_sum += error_rate
                    symbol_error_rate = symbol_errors / (input_len / symbol_len) * 100
                    sym_err_sum += symbol_error_rate
                error_rate = err_sum / 100
                symbol_error_rate = sym_err_sum / 100
                print(f"Symbol length: {symbol_len}")
                print(f"Orders: {orders}")
                print(f"Amplitudes: {amplitudes}")
                print(f"Input size: {input_len}")
                print(f"Signal to noise ratio: {arguments[2]}")
                print(f"Bit error rate: {round_half_up(error_rate, 2)}%")
                print(f"Symbol error rate: {round_half_up(symbol_error_rate, 2)}%")
                r.write(f"{orders};{amplitudes};{input_len};{arguments[2]};{round_half_up(error_rate, 2)};{round_half_up(symbol_error_rate, 2)}\n")
    # plt.show()
    f.close()
    r.close()


# def TEST():
#     # ---------Input Fields------------------------
#     nSym = 10 ** 3  # Number of symbols to transmit
#     EbN0dBs = np.arange(start=-4, stop=13, step=2)  # Eb/N0 range in dB for simulation
#     BER_sim = np.zeros(len(EbN0dBs))  # simulated Bit error rates
#
#     M = 2  # Number of points in BPSK constellation
#     m = np.arange(0, M)  # all possible input symbols
#     A = 1;  # amplitude
#     constellation = A * np.cos(m / M * 2 * np.pi)  # reference constellation for BPSK
#
#     # ------------ Transmitter---------------
#     inputSyms = np.random.randint(low=0, high=M, size=nSym)  # Random 1's and 0's as input to BPSK modulator
#     s = constellation[inputSyms]  # modulated symbols
#
#     fig, ax1 = plt.subplots(nrows=1, ncols=1)
#     ax1.plot(np.real(constellation), np.imag(constellation), '*')
#
#     # ----------- Channel --------------
#     # Compute power in modulatedSyms and add AWGN noise for given SNRs
#     for j, EbN0dB in enumerate(EbN0dBs):
#         gamma = 10 ** (EbN0dB / 10)  # SNRs to linear scale
#         P = sum(abs(s) ** 2) / len(s)  # Actual power in the vector
#         N0 = P / gamma  # Find the noise spectral density
#         n = np.sqrt(N0 / 2) * np.random.standard_normal(s.shape)  # computed noise vector
#         r = s + n  # received signal
#
#     # -------------- Receiver ------------
#     detectedSyms = (r <= 0).astype(int)  # thresolding at value 0
#     BER_sim[j] = np.sum(detectedSyms != inputSyms) / nSym  # calculate BER
#
#     BER_theory = 0.5 * erfc(np.sqrt(10 ** (EbN0dBs / 10)))
#
#     fig, ax = plt.subplots(nrows=1, ncols=1)
#     ax.semilogy(EbN0dBs, BER_sim, color='r', marker='o', linestyle='', label='BPSK Sim')
#     ax.semilogy(EbN0dBs, BER_theory, marker='', linestyle='-', label='BPSK Theory')
#     ax.set_xlabel('$E_b/N_0(dB)$')
#     ax.set_ylabel('BER ($P_b$)')
#     ax.set_title('Probability of Bit Error for BPSK over AWGN channel')
#     ax.set_xlim(-5, 13)
#     ax.grid(True)
#     ax.legend()
#     plt.show()


modulations_testing()
# TEST()
