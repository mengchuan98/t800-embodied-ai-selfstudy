"""18_t800_mnn_walk.py
用 MNN 策略网络推理，控制 T800 向前行走（教学最小化版）。

每个仿真步的流程：
  1) 采集机器人本体感知 -> 拼成 1083 维观测 obs
  2) MNN 推理 -> 22 维动作 action
  3) 把 action 当作 PD 目标算 ctrl（限幅）-> mj_step 推进

参考：17 号脚本（MNN 推理封装）、12 号脚本（PD 控制循环）。
"""

import math
import time
from pathlib import Path

import numpy as np
import mujoco
import mujoco.viewer


XML_PATH = Path(__file__).resolve().parent / "t800.xml"
POLICY_FILE = Path(__file__).resolve().parent / "policy" / "t800_260318_150533_60000.mnn"

OBS_SIZE, ACTION_SIZE = 1083, 22
FRAME, HISTORY = 72, 15            # 观测 = 15 帧 × 72 维 + 3 维命令
KP, KD = 5.0, 2 * math.sqrt(5.0)   # PD 增益（同 12 号脚本）
CMD_VX = 0.5                       # 期望前进速度 (m/s)，作为观测里的命令分量


# ---------- MNN 推理封装（精简自 17 号脚本）----------
class MnnPolicy:
    def __init__(self, path):
        import MNN
        self.MNN = MNN
        self.net = MNN.Interpreter(str(path))
        self.sess = self.net.createSession()
        self.inp = self.net.getSessionInput(self.sess)
        self.out = self.net.getSessionOutput(self.sess)

    def act(self, obs):
        obs = np.asarray(obs, np.float32).reshape(1, -1)
        MNN = self.MNN
        hi = MNN.Tensor(self.inp.getShape(), MNN.Halide_Type_Float, obs, MNN.Tensor_DimensionType_Caffe)
        self.inp.copyFrom(hi)
        self.net.runSession(self.sess)
        shape = self.out.getShape()
        ho = MNN.Tensor(shape, MNN.Halide_Type_Float, np.zeros(shape, np.float32), MNN.Tensor_DimensionType_Caffe)
        self.out.copyToHostTensor(ho)
        return np.asarray(ho.getData(), np.float32).reshape(-1)


# ---------- 把当前状态编码成 1083 维观测 ----------
def build_obs(model, data, base_id):
    # 单帧 72 维：25 个受控关节的 qpos/qvel + base 姿态/速度，余下补 0 凑 72
    qpos_list, qvel_list = [], []
    for aid in range(model.nu):
        jid = int(model.actuator_trnid[aid, 0])
        qpos_list.append(float(data.qpos[int(model.jnt_qposadr[jid])]))
        qvel_list.append(float(data.qvel[int(model.jnt_dofadr[jid])]))
    frame = np.concatenate([
        qpos_list,                                   # 25
        qvel_list,                                   # 25
        data.xquat[base_id],                         # 4  base 朝向(四元数)
        data.qvel[3:6],                              # 3  base 角速度
        data.qvel[0:3],                              # 3  base 线速度
    ])
    if frame.size < FRAME:
        frame = np.pad(frame, (0, FRAME - frame.size))
    else:
        frame = frame[:FRAME]
    # 15 帧历史（教学版：用当前帧重复堆叠；真实部署应维护滚动历史缓冲）
    obs = np.tile(frame, HISTORY)
    # 3 维命令：前进 / 横移 / 转向
    return np.concatenate([obs, [CMD_VX, 0.0, 0.0]])


def main():
    model = mujoco.MjModel.from_xml_path(str(XML_PATH))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)

    base_id = model.body("LINK_BASE").id
    qpos0 = data.qpos.copy()
    policy = MnnPolicy(POLICY_FILE)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        print(f"MNN 策略控制：T800 向前行走（obs={OBS_SIZE}, action={ACTION_SIZE}），关闭窗口结束")
        while viewer.is_running():
            obs = build_obs(model, data, base_id)
            action = policy.act(obs)                            # 推理得 22 维动作

            for aid in range(model.nu):
                jid = int(model.actuator_trnid[aid, 0])
                if int(model.jnt_type[jid]) not in (
                    mujoco.mjtJoint.mjJNT_HINGE, mujoco.mjtJoint.mjJNT_SLIDE
                ):
                    continue
                adr = int(model.jnt_qposadr[jid])
                dof = int(model.jnt_dofadr[jid])
                # 前 22 个关节用策略输出（相对默认姿态的偏移）做目标；其余保持初始姿态
                q_des = qpos0[adr] + float(action[aid]) if aid < ACTION_SIZE else qpos0[adr]
                u = KP * (q_des - float(data.qpos[adr])) - KD * float(data.qvel[dof])
                if int(model.actuator_ctrllimited[aid]):
                    lo, hi = model.actuator_ctrlrange[aid]
                    u = max(lo, min(hi, u))
                data.ctrl[aid] = u

            mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(model.opt.timestep)


if __name__ == "__main__":
    main()
