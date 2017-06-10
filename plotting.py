"""Plot Functions."""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import calculation


def plot_time(signal,
              fs=None,
              ax=None,
              scale='linear',
              sides='onesided',
              title=None,
              label=None,
              **kwargs):
    """Plot in Time Domain.

    """
    if ax is None:
        ax = plt.gca()
    if fs is None:
        fs = 1
        ax.set_xlabel("Samples")
    else:
        ax.set_xlabel("t / s")
    t = _time_vector_onesided(signal, fs)
    if scale == 'linear':
        ax.set_ylabel('Amplitude (linear)')
    elif scale == 'db':
        signal = _db_calculation(signal)
        ax.set_ylabel('Amplitude / dB')
    else:
        raise NameError("Invalid scale")
    if sides == 'onesided':
        ax.plot(t, signal, label=label, linewidth=2.0)
    elif sides == 'twosided':
        ax.plot(
            _time_vector_twosided(signal,
                                  fs),
            np.fft.fftshift(signal),
            label=label, linewidth=1.0)
    else:
        raise NameError("Invalid sides")
    if title is not None:
        ax.set_title(title)
    ax.grid(True)
    ax.ticklabel_format(useOffset=False)
    return ax


def plot_freq(signal,
              fs,
              ax=None,
              scale='linear',
              mode='magnitude',
              stem=False,
              sides=None,
              title=None,
              **kwargs):
    """Plot in Frequency Domain.

    """
    result, freqs = _spectral_helper(
        signal, fs, scale=scale, mode=mode, **kwargs)

    if ax is None:
        ax = plt.gca()

    if scale == 'linear':
        ax.set_ylabel('Magnitude (linear)')
    elif scale == 'db':
        ax.set_ylabel('Magnitude / dB')
    else:
        raise NameError("Invalid scale")
    if mode == 'magnitude':
        if title is not None:
            ax.set_title(title)
        else:
            ax.set_title('Magnitude Spectrum')
    elif mode == 'phase':
        if title is not None:
            ax.set_title(title)
        else:
            ax.set_title('Phase Spectrum')
        ax.set_ylabel('Phase / rad')
    elif mode == 'psd':
        if title is not None:
            ax.set_title(title)
        else:
            ax.set_title('Power Density Spectrum')
        ax.set_ylabel('dB / Hz')
    else:
        raise NameError("Invalid mode")
    if stem is False:
        ax.plot(freqs, result, linewidth=1.4)
    else:
        ax.stem(freqs, result, linewidth=1.4)
    ax.set_xlabel('f / Hz')
    ax.grid(True)
    ax.ticklabel_format(useOffset=False)
    return ax


def plot_tf(signal, fs, config='time+freq', **kwargs):
    """Subplot of Time and Frequency Domain.

    """
    fig, (ax1, ax2) = plt.subplots(2, 1)
    plt.subplots_adjust(hspace=0.6)
    if config == 'time+freq':
        plot_time(signal, fs, ax1)
        plot_freq(signal, fs, ax2, scale='db')
        ax2.set_xscale('log')
    elif config == 'mag+pha':
        plot_freq(signal, fs, ax1, scale='db')
        plot_freq(signal, fs, ax2, mode='phase')
    else:
        raise NameError("Invalid config")


def _spectral_helper(signal, fs, scale=None, mode=None, sides=None, **kwargs):

    result = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(len(signal), 1 / fs)

    if mode == 'psd':
        result = np.abs(result) ** 2 / (len(signal) * fs)
    if mode is None or mode == 'magnitude':
        result = 2 / len(signal) * np.abs(result)
    if mode == 'phase':
        result = np.angle(result)
        result = np.unwrap(result)
    if scale == 'db' and mode != 'phase':
        result = _db_calculation(result)
    elif mode == 'psd':
        result = result / 2
    return result, freqs


def _db_calculation(signal):
    return 20 * np.log10(np.abs(signal))


def _time_vector_onesided(signal, fs):
    return np.arange(len(signal)) / fs


def _time_vector_twosided(signal, fs):
    return np.linspace(-len(signal) // 2, len(signal) // 2, len(signal)) / fs
