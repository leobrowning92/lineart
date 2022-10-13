def xy_plane(edges):
    """trivial, removes z coord to 2d"""
    return edges[:, :, :-1]


EDGE_PROJECTIONS = {
    "xy_plane": xy_plane,
}
