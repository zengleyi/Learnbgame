
class Chunks:
    class Version3:

        class Hoppe:
            HEADER = 0x1
            VERT_SPLITS	= 0x2
            FIX_FACES = 0x3

        TEXTURE = 0x2
        TEXTURE_L = 0x3
        CHILD_REFS = 0x5
        BBOX = 0x6
        VERTICES = 0x7
        INDICES = 0x8
        LODDATA = 0x9
        VCONTAINER = 0xa
        BSPHERE = 0xb
        CHILDREN_L = 0xc
        S_BONE_NAMES = 0xd
        S_MOTIONS = 0xe
        DPATCH = 0xf
        LODS = 0x10
        CHILDREN = 0x11
        S_SMPARAMS = 0x12
        ICONTAINER = 0x13
        S_SMPARAMS_NEW = 0x14
        LODDEF2 = 0x15
        TREEDEF2 = 0x16
        S_IKDATA_0 = 0x17
        S_USERDATA = 0x18
        S_IKDATA = 0x19
        S_MOTIONS_NEW = 0x1a
        S_DESC = 0x1b
        S_IKDATA_2 = 0x1C
        S_MOTION_REFS = 0x1D

    HEADER = 0x1
    TEXTURE = 0x2
    VERTICES = 0x3
    INDICES = 0x4
    VCONTAINER = 0x7
    ICONTAINER = 0x8
    SWIDATA = 0x6
    CHILDREN = 0x9
    CHILDREN_L = 0xa
    LODDEF2 = 0xb
    TREEDEF2 = 0xc
    S_BONE_NAMES = 0xd
    S_SMPARAMS = 0xf
    S_IKDATA = 0x10
    S_USERDATA = 0x11
    DESC = 0x12
    S_MOTION_REFS_0 = 0x13
    SWICONTAINER = 0x14
    GCONTAINER = 0x15
    FASTPATH = 0x16


# model types
NORMAL = 'NORMAL'
HIERRARHY = 'HIERRARHY'
PROGRESSIVE = 'PROGRESSIVE'
SKELETON_ANIM = 'SKELETON_ANIM'
SKELETON_GEOMDEF_PM = 'SKELETON_GEOMDEF_PM'
SKELETON_GEOMDEF_ST = 'SKELETON_GEOMDEF_ST'
LOD = 'LOD'
TREE_ST = 'TREE_ST'
PARTICLE_EFFECT = 'PARTICLE_EFFECT'
PARTICLE_GROUP = 'PARTICLE_GROUP'
SKELETON_RIGID = 'SKELETON_RIGID'
TREE_PM = 'TREE_PM'

model_types = {
    0x0: NORMAL,
    0x1: HIERRARHY,
    0x2: PROGRESSIVE,
    0x3: SKELETON_ANIM,
    0x4: SKELETON_GEOMDEF_PM,
    0x5: SKELETON_GEOMDEF_ST,
    0x6: LOD,
    0x7: TREE_ST,
    0x8: PARTICLE_EFFECT,
    0x9: PARTICLE_GROUP,
    0xa: SKELETON_RIGID,
    0xb: TREE_PM
}

# vertex formats
OGF_VERTEXFORMAT_FVF = 0x112
OGF4_VERTEXFORMAT_FVF_1L = 0x12071980
OGF4_VERTEXFORMAT_FVF_2L = 0x240e3300
OGF4_VERTEXFORMAT_FVF_NL = 0x36154c80
