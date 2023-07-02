import numpy as np
import pandas as pd
import polyscope as ps
from Logger import Logger
from SampleFromMesh import readOBJ
from Gen_mesh import msh_to_obj

if __name__ == "__main__":
    # Logger
    logger = Logger()
    logger.launch()

    # Read Gmsh file
    msh_to_obj("../mesh.msh","../mesh.obj",logger)
    vertices, faces =  readOBJ("../mesh.obj", logger)

    # Read csv file
    solution = pd.read_csv("../result.csv").values
    p,uv,u,v = solution[:,3], solution[:,4], solution[:,5], solution[:,6]

    # Plot
    ps.init()
    ps_mesh = ps.register_surface_mesh('car',vertices,faces)
    ps_mesh.add_scalar_quantity("p",p,cmap="jet")
    ps_mesh.add_scalar_quantity("sqrt(u^2+v^2)",uv,cmap="jet")
    ps_mesh.add_scalar_quantity("u",u,cmap="jet")
    ps_mesh.add_scalar_quantity("v",v,cmap="jet")

    ps.show()