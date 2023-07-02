import numpy as np
import igl
import random
from tqdm import tqdm
from Parallel import Parallel
from Logger import Logger

def readOff(off_file, logger = None):
    # Read an off file
    if off_file[-4:] != ".off":
        logger.error(f"{off_file} is not an off file.")
        exit()
    vertices, faces, _ = igl.read_off(off_file)
    if logger:
        logger.info(f"read {off_file} successfully!")
        logger.info(f"n_vertices = {vertices.shape[0]},  n_faces = {faces.shape[0]}")
    return vertices, faces

def readOBJ(obj_file, logger = None):
    # Read an obj file
    if obj_file[-4:] != ".obj":
        logger.error(f"{obj_file} is not an obj file.")
        exit()
    vertices, _, _, faces, _, _ = igl.read_obj(obj_file)
    if logger:
        logger.info(f"read {obj_file} successfully!")
        logger.info(f"n_vertices = {vertices.shape[0]},  n_faces = {faces.shape[0]}")
    return vertices, faces

def saveXYZ(xyz_file, points_ls, logger = None):
    # Save points into a xyz file
    if xyz_file[-4:] != ".xyz":
        logger.error(f"{xyz_file} is not a xyz file.")
        exit()
    points = np.asarray(points_ls)
    np.savetxt(xyz_file, points)
    if logger:
        logger.info(f"points are saved to {xyz_file}")

def faceArea(vertices, faces):
    # Compute the area of each face
    dbl_area = igl.doublearea(vertices, faces)
    return dbl_area / 2.0

def sampleFromTriangle(point_1, point_2, point_3, sample_points):
    # Sample points from a triangle [p1,p2,p3]
    points_ls = []
    for i in range(sample_points):
        a = random.uniform(0,1)
        b = random.uniform(0,1)
        c = random.uniform(0,1)
        a, b, c  = a / (a + b + c), b / (a + b + c), c / (a + b + c)
        points_ls.append(a * point_1 + b * point_2 + c * point_3)
    return points_ls

def sampleFromMesh(vertices, faces, logger = None, sample_points = 1e5):
    # Sample points from the mesh
    face_areas = faceArea(vertices, faces)
    sum_area = np.sum(face_areas) # Sum of face areas
    weights = face_areas / sum_area
    face_samples = np.round(weights * sample_points).astype(int) # Samples of each face
    points_ls = []
    # Parallel computation
    variable = []
    for i in range(face_samples.shape[0]):
        #logger.info(f"[{i/face_samples.shape[0]*100}%] \
        #            sample {face_samples[i]} points from face {i+1}.")
        variable.append([vertices[faces[i][0],:],
                    vertices[faces[i][1],:],
                    vertices[faces[i][2],:],
                    face_samples[i]])
    parallel = Parallel(variable,sampleFromTriangle)
    points = parallel.launch()
    points_ls = [item for sublist in points for item in sublist]
    if logger:
        logger.info(f"sample {len(points_ls)} points overall")
    return points_ls

if __name__ == "__main__":
    logger = Logger()
    logger.launch()
    vertices, faces = readOff("car/train/car_0001.off", logger)
    points_ls = sampleFromMesh(vertices, faces, logger)
    saveXYZ("points.xyz",points_ls, logger)