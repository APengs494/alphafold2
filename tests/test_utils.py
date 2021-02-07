import torch
import numpy as np
from alphafold2_pytorch.utils import *

def test_center_distogram_median():
    distogram = torch.randn(1, 128, 128, 37)
    distances, weights = center_distogram_torch(distogram, center = 'median')
    assert True

def test_masks():
    seqs = torch.randint(20, size=(2, 50))
    # cloud point mask
    cloud_masks = scn_cloud_mask(seqs, boolean=True)
    # atom masking
    N_mask, CA_mask = scn_backbone_mask(seqs, boolean = True, l_aa = 3)
    assert True

def test_mds_and_mirrors():
    distogram = torch.randn(1, 32*3, 32*3, 37)

    distances, weights = center_distogram_torch(distogram)

    # masks
    masker  = torch.arange(distogram.shape[1]) % 3
    N_mask  = (masker==0).bool()
    CA_mask = (masker==1).bool()
    coords_3d, _ = MDScaling(distances, 
        weights = weights,
        iters = 50, 
        fix_mirror = 2,
        N_mask = N_mask,
        CA_mask = CA_mask,
        C_mask = None
    )
    assert coords_3d.shape == (3, 128), 'coordinates must be of the right shape after MDS'

def test_nerf_and_dihedral():
    # create points
    a = torch.tensor([1,2,3]).float()
    b = torch.tensor([1,4,5]).float()
    c = torch.tensor([1,4,7]).float()
    d = torch.tensor([1,8,8]).float()
    # calculate internal references
    v1 = (b-a).numpy()
    v2 = (c-b).numpy()
    v3 = (d-c).numpy()
    # get angles
    theta = np.arccos( np.dot(v2, v3) / \
                      (np.linalg.norm(v2) * np.linalg.norm(v3) )) 

    normal_p  = np.cross(v1, v2) 
    normal_p_ = np.cross(v2, v3)
    chi = np.arccos( np.dot(normal_p, normal_p_) / \
                    (np.linalg.norm(normal_p) * np.linalg.norm(normal_p_) ))
    # get length:
    l = torch.tensor(np.linalg.norm(v3))
    theta = torch.tensor(theta)
    chi = torch.tensor(chi)
    # reconstruct
    assert nerf_torch(a, b, c, l, theta, chi) == d
    assert get_dihedral_torch(a, b, c, d).item() == chi

def test_sidechain_container():
    bb = torch.randn(2, 137*3, 3)
    proto_3d = sidechain_container(bb, place_oxygen=True)
    assert list(proto_3d.shape) == [2, 137, 14, 3]

def test_kabsch():
    a  = torch.randn(3, 8)
    b  = torch.randn(3, 8) 
    a_ = Kabsch(a,b)
    assert a.shape == a_.shape

def test_tmscore():
    a = torch.randn(2, 3, 8)
    b = torch.randn(2, 3, 8)
    out = TMscore(a, b)
    assert True

def test_gdt():
    a = torch.randn(1, 3, 8)
    b = torch.randn(1, 3, 8)
    GDT(a, b, weights = 1)
    assert True

