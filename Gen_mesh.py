"""
This script read a 2D point cloud, and generate a polygon mesh using Gmesh.
Note: 
1. The 2D point cloud is as a hole in the mesh generation.
2. The points of the 2D point cloud must be in order.
"""
import gmsh
import meshio
from Logger import Logger
import numpy as np

def readPointCloud(pcd_file, logger=None):
    # read a point cloud from .xyz file (x y z r g b)
    pcd = np.loadtxt(pcd_file)
    x, y, z = pcd[:,0], pcd[:,1], pcd[:,2]
    if logger:
        logger.info(f"read point cloud from {pcd_file} successfully!")

    return [x,y,z]

def boundingbox(x,y,x_Length=250,y_Length=100):
    # find the 2D bounding box of the points {(x,y)}, required length: x_Length * y_Length
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    x_offset = (x_Length - xmax + xmin) / 2
    y_offset = y_Length - ymax + ymin - 1
    # the four corner of the bounding box
    corners = [(xmin-x_offset,ymin-1), 
               (xmax+x_offset,ymin-1), 
               (xmax+x_offset,ymax+y_offset), 
               (xmin-x_offset,ymax+y_offset)]

    return corners

def msh_to_obj(msh_file, obj_file, logger=None):

    mesh = meshio.read(msh_file)
    
    vertices = []
    for point in mesh.points:
        vertices.append([point[0], point[1], point[2]])
        
    faces = []
    for cell in mesh.cells:
        if cell.type == 'triangle':
            for face in cell.data:
                faces.append([face[0], face[1], face[2]])
    
    with open(obj_file, 'w') as f:
        for vertex in vertices:
            f.write('v {} {} {}\n'.format(vertex[0], vertex[1], vertex[2]))

        for face in faces:
            f.write('f {} {} {}\n'.format(face[0]+1, face[1]+1, face[2]+1))
    
    if logger:
        logger.info(f"save {msh_file} to {obj_file}")

def addPolygon(x,y):
    # x: the vector/list of x coord, y: the vector/list of y coord
    point_ls = []
    for i in range(len(x)):
        point_ls.append(gmsh.model.occ.addPoint(x[i],y[i],0))
    
    line_ls = []
    for j in range(len(point_ls) - 1):
        line_ls.append(gmsh.model.occ.addLine(point_ls[j],point_ls[j+1]))
    line_ls.append(gmsh.model.occ.addLine(point_ls[-1],point_ls[0]))
    curve_loop = gmsh.model.occ.addCurveLoop(line_ls) # hole

    return curve_loop

def addShape(x,y):
    # x: the vector/list of x coord, y: the vector/list of y coord

    [P1,P2,P3,P4] = boundingbox(x,y) # four corners of bounding box
    wire = addPolygon([P1[0],P2[0],P3[0],P4[0]],[P1[1],P2[1],P3[1],P4[1]])
    hole = addPolygon(x,y) # inner hole

    shape = gmsh.model.occ.addPlaneSurface([wire,hole])

    return shape

if __name__ == "__main__":
    # Logger
    logger = Logger()
    logger.launch()

    # Initialize the Gmsh API
    gmsh.initialize()

    # Set the general terminal option to 1 to turn off interactive mode
    gmsh.option.setNumber("General.Terminal", 1)

    # Create a new model and set its dimension to 2 (for 2D geometry)
    model = gmsh.model
    model.add('my_model')

    # read points from file
    [x,y,z] = readPointCloud("../boundary.xyz", logger)

    # Add shape as a geometric entity
    shape = addShape(x,y)

    # Synchronize the model with Gmsh
    gmsh.model.occ.synchronize()

    # Generate the mesh
    model.mesh.generate(2)

    # Save the mesh to a Gmesh file
    gmsh.write('my_mesh.msh')

    # Finalize the Gmsh API
    gmsh.finalize()

    # msh to obj
    msh_to_obj('my_mesh.msh','my_mesh.obj', logger)