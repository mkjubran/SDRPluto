import numpy as np
import adi
import matplotlib.pyplot as plt
import pdb
import time

sample_rate = 1e6 # Hz
center_freq = 1000e6 # Hz
num_samps = 10000 # number of samples per call to rx()

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Config Tx
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = 0 # Increase to increase tx power, valid range is -90 to 0 dB
#sdr.tx_cyclic_buffer = True

# Config Rx
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 10.0 # dB, increase to increase the receive gain, but be careful not to saturate the ADC

### Transmit Sinewave
fc = 2000
ts = 1/float(sample_rate)
t = np.arange(0, num_samps*ts, ts)
x_symbols_i = np.sin(2*np.pi*t*fc) # Amplitude of the I-signal
x_symbols_q = np.cos(2*np.pi*t*fc) # Amplitude of the Q-signal
x_symbols_iq = x_symbols_i + 1j*x_symbols_q # j = sqrt(-1) . This is the Iq signal
samples = np.repeat(x_symbols_iq, 1)
tx_samples=np.copy(samples)
samples *= 2**14 # To scale the signal according to the range of the SDR

while True:
 # Stop transmitting
 sdr.tx_destroy_buffer()
 #time.sleep(2)

 # Start the transmitter
 sdr.tx_cyclic_buffer = True # Enable cyclic buffers
 sdr.tx(samples) # start transmitting

 # Clear buffer just to be safe
 for i in range (0, 10):
    raw_data = sdr.rx()

 # Receive samples
 rx_samples = sdr.rx()
 
 plt.figure(0)
 plt.clf()
 plt.plot(t,np.real(tx_samples))
 #plt.plot(np.imag(rx_samples[::10]))
 plt.ylabel("Amplitude")
 plt.title('Transmitted')
 plt.xlabel("Time")
 plt.pause(0.05) 

 plt.figure(1)
 plt.clf()
 plt.plot(t,np.real(rx_samples))
 plt.ylabel("Amplitude")
 plt.title('Received')
 plt.xlabel("Time")

 plt.pause(0.05) 
 time.sleep(2)

plt.show
