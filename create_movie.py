import numpy as np
from matplotlib import pyplot as plt
import cv2
import argparse

def generate_movie(filepath, output_name):
    # Read the test sequence file
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Parse the qubits and initial positions
    qubit_ids = lines[1].split()
    initial_positions = [eval(pos) for pos in lines[3].split()]

    spacing = 50

    width = 640
    height = 480
    fps = 60
    duration_multiplier = 1  # Adjust the speed of movement

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_out = cv2.VideoWriter(output_name, fourcc, fps, (width, height))

    # Function to draw each frame
    def draw_frame(positions):
        plt.clf()
        plt.xlim(0, width)
        plt.ylim(0, height)

        # Draw black dots at specified positions
        for pos in positions:
            plt.scatter(spacing*pos[0]+spacing, height - (spacing*pos[1]+spacing), color='black', marker=".")

        # Convert the plot to an image
        plt.axis('off')
        plt.gcf().canvas.draw()
        img = np.array(plt.gcf().canvas.renderer._renderer)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        return img

    # Function to parse move commands and update positions
    def draw_movement(curr_positions, move_command, qubits_list):
        move_args = move_command.split()
        qubits_affected = qubits_list.split()
        dx, dy = float(move_args[1]), float(move_args[2]) #total distance to be moved
        duration = float(move_args[3][:-1]) * duration_multiplier  # Remove 's' and multiply duration
        num_frames = int(duration * fps)
        for i in range(0,num_frames):
            curr_positions = [(pos[0] + dx/num_frames, pos[1] + dy/num_frames) if qubit_ids[i] in qubits_affected else pos for i,pos in enumerate(curr_positions)]
            video_out.write(draw_frame(curr_positions))
        return curr_positions

    # Extract move commands and update positions accordingly
    positions = initial_positions
    for i in range(4,len(lines)):
        if lines[i].startswith('move'):
            positions = draw_movement(positions, lines[i], lines[i+1])
            i = i+1
        elif lines[i].startswith('wait'):
            duration = float(lines[i].split()[1][:-1]) * duration_multiplier  # Remove 's' and multiply duration
            num_frames = int(duration * fps)
            for _ in range(num_frames):
                video_out.write(draw_frame(positions))

    # Release VideoWriter and close plot
    video_out.release()
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="outputs a movie corresponding to a neutral atom movement sequence")
    parser.add_argument('filepath', type=str, help='filepath to movement sequence')
    parser.add_argument('output_name', type=str, nargs='?', const='output.mp4', default='output.mp4', help='name of output file')
    args = parser.parse_args()
    generate_movie(args.filepath, args.output_name)