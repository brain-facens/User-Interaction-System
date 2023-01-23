import sys
import os

header = "# .PCD v.7 - Point Cloud Data file format\n\
VERSION .7\n\
FIELDS x y z rgb\n\
SIZE 4 4 4 1\n\
TYPE F F F F\n\
COUNT 1 1 1 1\n\
WIDTH XXXX\n\
HEIGHT 1\n\
VIEWPOINT 0 0 0 1 0 0 0\n\
POINTS XXXX\n\
DATA ascii"

def convertionOfPlyToPcd(ply_file, pcd_file):
    input_file = open(ply_file)
    out = pcd_file
    output = open(out, 'w')
    write_points = False
    points_counter = 0
    nr_points = 0
    for s in input_file.readlines():
        if s.find("element vertex") != -1:
            nr_points = int(s.split(" ")[2].rstrip().lstrip())
            new_header = header.replace("XXXX", str(nr_points))
            output.write(new_header)
            output.write("\n")
        if s.find("end_header") != -1:
            write_points = True
            continue
        if write_points and points_counter < nr_points:
            points_counter = points_counter + 1
            output.write(" ".join(s.split(" ", 4)[:4]))
            output.write("\n")
    input_file.close()
    output.close()

if __name__ == "__main__":
    # We request the path to the script, if it's not found - exit
    if sys.argv[0] == "":
        sys.exit(1)
    # PLY file - We convert this format to PCD format
    ply_file = sys.argv[1]
    # PCD file - generated from PLY file
    pcd_file = sys.argv[2]

    # Function which converts .ply format files to .pcd files
    convertionOfPlyToPcd(ply_file, pcd_file)