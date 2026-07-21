"""加载 t800.xml 并打印所有关节信息，格式如下：

[000] <unnamed_0> | type=mjJNT_FREE | qposadr=0 | dofadr=0
[001] J00_HIP_PITCH_L | type=mjJNT_HINGE | qposadr=7 | dofadr=6
...
"""

import os

import mujoco

XML_PATH = os.path.join(os.path.dirname(__file__), "t800.xml")
model = mujoco.MjModel.from_xml_path(XML_PATH)

JOINT_TYPE = {
    0: "mjJNT_FREE",
    1: "mjJNT_BALL",
    2: "mjJNT_SLIDE",
    3: "mjJNT_HINGE",
}

print(f"关节数量: {model.njnt}")
for i in range(model.njnt):
    name = model.joint(i).name
    if not name:
        name = f"<unnamed_{i}>"

    jtype = JOINT_TYPE.get(model.jnt_type[i].item(), "UNKNOWN")
    qposadr = model.jnt_qposadr[i].item()
    dofadr = model.jnt_dofadr[i].item()

    print(f"[{i:03d}] {name} | type={jtype} | qposadr={qposadr} | dofadr={dofadr}")
