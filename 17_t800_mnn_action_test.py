from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
POLICY_FILE = ROOT / "policy" / "t800_260318_150533_60000.mnn"
OBS_SIZE = 1083
ACTION_SIZE = 22


class MnnBridge:
    def __init__(self):
        try:
            import MNN  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "当前 Python 环境里没有 MNN。请先在 t800 的 conda 环境里安装 MNN，再运行这个脚本。"
            ) from exc

        if not POLICY_FILE.exists():
            raise FileNotFoundError(POLICY_FILE)

        self.MNN = MNN
        self.net = MNN.Interpreter(str(POLICY_FILE))
        self.session = self.net.createSession()
        self.input_tensor = self.net.getSessionInput(self.session)
        self.output_tensor = self.net.getSessionOutput(self.session)

    def infer(self, obs):
        obs = np.asarray(obs, dtype=np.float32).reshape(1, -1)
        if obs.shape[1] != OBS_SIZE:
            raise ValueError(f"obs 维度应为 {OBS_SIZE}，当前是 {obs.shape[1]}")

        MNN = self.MNN
        host_input = MNN.Tensor(
            self.input_tensor.getShape(),
            MNN.Halide_Type_Float,
            obs,
            MNN.Tensor_DimensionType_Caffe,
        )
        self.input_tensor.copyFrom(host_input)
        self.net.runSession(self.session)

        output_shape = self.output_tensor.getShape()
        host_output = MNN.Tensor(
            output_shape,
            MNN.Halide_Type_Float,
            np.zeros(output_shape, dtype=np.float32),
            MNN.Tensor_DimensionType_Caffe,
        )
        self.output_tensor.copyToHostTensor(host_output)

        action = np.asarray(host_output.getData(), dtype=np.float32).reshape(-1)
        if action.size != ACTION_SIZE:
            raise ValueError(f"action 维度应为 {ACTION_SIZE}，当前是 {action.size}")
        return action

    def close(self):
        pass


bridge = MnnBridge()

try:
    # 1083 = 72 * 15 + 3
    # 这里先用全 0 的假 observation 做推理测试。
    obs = np.zeros(OBS_SIZE, dtype=np.float32)

    action = bridge.infer(obs)

    print("policy file:", POLICY_FILE.name)
    print("obs size:", obs.size)
    print("MNN action size:", action.size)
    print("first 6 actions:", action[:6].round(4).tolist())
finally:
    bridge.close()
