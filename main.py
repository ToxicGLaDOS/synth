#!/usr/bin/env python
import wave, math

SAMPLE_RATE = 44100
CHANNELS = 2
SAMPLE_WIDTH = 2
VOLUME_RATIO = 1/4

def get_sample_triangle(t, freq):
    if (2 * t * freq) % 2 < 1:
        return get_sample_sawtooth(2 * t, freq)
    else:
        return -get_sample_sawtooth(2 * t, freq)

def get_sample_square(t, freq):
    if (t * freq) % 1 < .5:
        return 1
    else:
        return -1

def get_sample_sawtooth(t, freq):
    return 2 * ((t * freq) % 1) - 1

def get_sample_sine(t, freq):
    return math.sin(2 * math.pi * t * freq)

# Converts a sample from -1-1 space to
# a list of 0-255 ints which when concatanated
# as bytes will produce value equal to the sample
# in the 0-(256^SAMPLE_WIDTH) space.
#
# Essentially, it takes -1-1 and turns that into the
# values you need to add to the bytearray to play that
# sample
def sample_to_ints(sample: float) -> list[int]:
    # This gets us one byte per SAMPLE_WIDTH (at most)
    sample *= (2**8)**SAMPLE_WIDTH/2
    sample *= VOLUME_RATIO
    sample = int(sample)
    sample_bytes = sample.to_bytes(SAMPLE_WIDTH, byteorder='little', signed=True)
    sample_ints = list(sample_bytes)
    return sample_ints

def divide_chunks(l: list, n: int):
    if len(l) % n != 0:
        raise ValueError(f"Can't break into evenly sized chunks len={len(l)} n={n}")
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def join_channels(left, right):
    joined = []
    for l_sample, r_sample in zip(divide_chunks(left, SAMPLE_WIDTH), divide_chunks(right, SAMPLE_WIDTH)):
        joined.extend(l_sample)
        joined.extend(r_sample)
    
    return joined

def main():
    with wave.open("test.wav", 'wb') as out_file:
        out_file.setframerate(SAMPLE_RATE)
        out_file.setnchannels(CHANNELS)
        out_file.setsampwidth(SAMPLE_WIDTH)

        left_samples = []
        for x in range(SAMPLE_RATE * 10):
            t = x / SAMPLE_RATE
            sample = (get_sample_sine(t, 440))
            sample_ints = sample_to_ints(sample)
            left_samples.extend(sample_ints)

        #right_samples = sample_to_ints(0) * len(left_samples)
        samples = join_channels(left_samples, left_samples)
        ba = bytearray(samples)
        out_file.writeframes(ba)


if __name__ == "__main__":
    main()
