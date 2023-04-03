"""
TS-SS similarity. reference from github.
https://github.com/taki0112/Vector_Similarity/blob/master/python/TS_SS/tss_ss_vectorized.py

"""
import math
import torch


def cos_sim(v):
    v_inner = inner_product(v)
    v_size = vec_size(v)
    v_cos = v_inner / torch.mm(v_size, v_size.t())
    return v_cos


def vec_size(v):
    return v.norm(dim=-1, keepdim=True)


def inner_product(v):
    return torch.mm(v, v.t())


def euclidean_dist(v, eps=1e-10):
    v_norm = (v ** 2).sum(-1, keepdim=True)
    dist = v_norm + v_norm.t() - 2.0 * torch.mm(v, v.t())
    dist = torch.sqrt(torch.abs(dist) + eps)
    return dist


def theta(v, eps=1e-5):
    v_cos = cos_sim(v).clamp(-1. + eps, 1. - eps)
    x = torch.acos(v_cos) + math.radians(10)
    return x


def triangle(v):
    theta_ = theta(v)
    theta_rad = theta_ * math.pi / 180.
    vs = vec_size(v)
    x = (vs.mm(vs.t())) * torch.sin(theta_rad)
    return x / 2.


def magnitude_dif(v):
    vs = vec_size(v)
    return (vs - vs.t()).abs()


def sector(v):
    ed = euclidean_dist(v)
    md = magnitude_dif(v)
    sec = math.pi * torch.pow((ed + md), 2) * theta(v) / 360.
    return sec


def ts_ss(v):
    vector = torch.tensor(v)
    tri = triangle(vector)
    sec = sector(vector)
    return tri * sec
