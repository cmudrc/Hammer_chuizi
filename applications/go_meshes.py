#### generate dataset -- mesh
import numpy as np
import trimesh
import os.path as osp
import os
from pathlib import Path
import argparse
import json
import glob

from hammer import GeoReader
from hammer.utilities.plotting import plot_element_adding

data_dir = osp.join(Path.home(), 'data','hammer')
#data_dir = osp.join('/mnt/c/Users/jiang', 'data','hammer')

def go_meshes(args):
    #parameter_json_file = osp.join(data_dir, "base_20.json")
    parameter_json_file = osp.join(data_dir, args.mesh_parameters+'.json')
    mesh_para = json.load(open(parameter_json_file)) 

    dx = float(mesh_para["dx"])
    nx = float(mesh_para["nx"])
    Add_base = bool(mesh_para["Add_base"])
    num_samples = int(mesh_para["num_samples"])
    base_depth = float(mesh_para["base_depth"])

    geo_dir = osp.join(data_dir, "geo_models",args.geo_models)
    femfile_dir = osp.join(data_dir,"meshes",args.geo_models+'_'+args.mesh_parameters)
    #femfile_dir = osp.join(data_dir,"meshes","test")
    os.makedirs(femfile_dir, exist_ok=True)
    files = glob.glob(osp.join(femfile_dir, f'*'))
    for f in files:
        os.remove(f)
    
    Same_base_flag=False
    Same_base_flag=False
    geo_reader = GeoReader(dx,nx,Add_base,Same_base_flag)
    files = glob.glob(os.path.join(geo_dir, f'*.stl'))
    files.sort()
    files.sort()
    for i,f in enumerate(files):
        geo_reader.load_file(f)
        geo_reader.voxelize()
        geo_reader.extend_base(base_depth) 
        geo_reader.generate_part_toolpath('zigzag')
        geo_reader.generate_hexahedron_cells()
        geo_reader.sample_deposits(num_samples)
        save_file_path = osp.join(femfile_dir, Path(f).stem+".p")
        geo_reader.save_hex_mesh(save_file_path)
        print("Finished {:d} file!".format(i))
        # print(geo_reader._voxel_inds.shape)
        # bif = geo_reader.calculate_bif()
        # print(bif.shape)
        # if i == 0:
        #     #geo_reader.plot_fem_mesh()
        #     toolpath = geo_reader.get_toolpath()
        #     geo_reader.plot_part_toolpath(toolpath)
        # print(geo_reader._voxel_inds.shape)
        # bif = geo_reader.calculate_bif()
        # print(bif.shape)
        # if i == 0:
        #     #geo_reader.plot_fem_mesh()
        #     toolpath = geo_reader.get_toolpath()
        #     geo_reader.plot_part_toolpath(toolpath)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--geo_models", type=str, required=True)
    parser.add_argument("--mesh_parameters", type=str, required=True)
    args = parser.parse_args()    
    go_meshes(args)
