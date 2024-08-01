import pickle
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import os
import math

with open('render_poses.pkl', 'rb') as f:
    render_poses = pickle.load(f)

with open('poses.pkl', 'rb') as f:
    poses = pickle.load(f)

with open('image_notes.pkl', 'rb') as f:
    image_notes = pickle.load(f)


def weighted_average_frequency(viewer_pos, image_positions, image_notes, epsilon=1e-6, influence_factor=1):
    distances = np.linalg.norm(image_positions - viewer_pos, axis=1)
    weights = 1 / (np.sqrt(distances) + (epsilon))

    leftmost_idx = np.argmin(image_positions[:, 0])
    rightmost_idx = np.argmax(image_positions[:, 0])
    
    weights[leftmost_idx] *= influence_factor
    weights[rightmost_idx] *= influence_factor
    
    note_frequencies = {'A': 440.00, 'A#': 466.16, 'B': 493.88, 'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00, 'G#': 415.30, '0': 0.00}
    frequencies = np.array([note_frequencies[image_notes[i]] for i in range(len(image_notes))])
    weighted_freq = np.sum(weights * frequencies) / np.sum(weights)
    return weighted_freq

if not os.path.exists('temp_sounds'):
    os.makedirs('temp_sounds')


image_notes = ['0'] * len(image_notes)
image_notes[np.argmin(render_poses[:, 0, -1])] = 'G#'
image_notes[np.argmax(render_poses[:, 0, -1])] = 'A'

print('Generating sounds...')
sound_segments = []
for i, pose in enumerate(render_poses):
    print(f'Generating sound for frame {i}')
    viewer_pos = pose[:3, -1]
    image_positions = poses[:, :3, -1]

    average_frequency = weighted_average_frequency(viewer_pos, image_positions, image_notes)
    print(f'Average frequency {average_frequency} for frame {i}')
    sine_wave = Sine(average_frequency)

    sound = sine_wave.to_audio_segment(duration=180)
    sound_segments.append(sound)

print(f"Number of sound segments: {len(sound_segments)}")


print('Combining sound segments...')
combined_sounds = sound_segments[0]
for sound in sound_segments[1:]:
    combined_sounds = combined_sounds.append(sound, crossfade=50)
for sound in sound_segments[1:]:
    combined_sounds = combined_sounds.append(sound, crossfade=50)

combined_duration = combined_sounds.duration_seconds
print(f"Combined sound duration: {combined_duration} seconds")

output_mp3 = 'combined_sounds.mp3'
combined_sounds.export(output_mp3, format='mp3')
print(f'Sound generation complete. Saved to {output_mp3}')
