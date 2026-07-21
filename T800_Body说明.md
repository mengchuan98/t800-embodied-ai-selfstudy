# T800 机器人 Body（连杆）说明

| 序号 | Body 名称 | 中文含义 | 说明 |
|:---:|:---|:---|:---|
| 0000 | `world` | 世界坐标系 | MuJoCo 仿真的全局根节点，不代表机器人实体部件 |
| 0001 | `LINK_BASE` | 躯干底座 | 机器人底盘/骨盆，是整个机器人结构的根 Body |
| 0002 | `LINK_HIP_PITCH_L` | 左髋俯仰 | 左腿髋关节 Pitch 连杆，控制前后摆动 |
| 0003 | `LINK_HIP_ROLL_L` | 左髋横滚 | 左腿髋关节 Roll 连杆，控制左右侧摆 |
| 0004 | `LINK_HIP_YAW_L` | 左髋偏航 | 左腿髋关节 Yaw 连杆，控制绕竖直轴旋转 |
| 0005 | `LINK_KNEE_PITCH_L` | 左膝俯仰 | 左腿膝关节 Pitch 连杆，控制膝盖弯曲/伸直 |
| 0006 | `LINK_ANKLE_PITCH_L` | 左踝俯仰 | 左脚踝关节 Pitch 连杆，控制脚掌前后翻转 |
| 0007 | `LINK_ANKLE_ROLL_L` | 左踝横滚 | 左脚踝关节 Roll 连杆，控制脚掌左右翻转 |
| 0008 | `LINK_FOOT_L` | 左脚底板 | 左脚末端 Body，包含足底碰撞体 |
| 0009 | `LINK_HIP_PITCH_R` | 右髋俯仰 | 右腿髋关节 Pitch 连杆 |
| 0010 | `LINK_HIP_ROLL_R` | 右髋横滚 | 右腿髋关节 Roll 连杆 |
| 0011 | `LINK_HIP_YAW_R` | 右髋偏航 | 右腿髋关节 Yaw 连杆 |
| 0012 | `LINK_KNEE_PITCH_R` | 右膝俯仰 | 右腿膝关节 Pitch 连杆 |
| 0013 | `LINK_ANKLE_PITCH_R` | 右踝俯仰 | 右脚踝关节 Pitch 连杆 |
| 0014 | `LINK_ANKLE_ROLL_R` | 右踝横滚 | 右脚踝关节 Roll 连杆 |
| 0015 | `LINK_FOOT_R` | 右脚底板 | 右脚末端 Body，包含足底碰撞体 |
| 0016 | `LINK_WAIST_YAW` | 腰部偏航 | 腰部 Yaw 连杆，连接躯干上半身，控制上半身旋转 |
| 0017 | `LINK_SHOULDER_PITCH_L` | 左肩俯仰 | 左臂肩关节 Pitch 连杆，控制大臂前后摆动 |
| 0018 | `LINK_SHOULDER_ROLL_L` | 左肩横滚 | 左臂肩关节 Roll 连杆，控制大臂旋转 |
| 0019 | `LINK_SHOULDER_YAW_L` | 左肩偏航 | 左臂肩关节 Yaw 连杆，控制大臂外展/内收 |
| 0020 | `LINK_ELBOW_PITCH_L` | 左肘俯仰 | 左臂肘关节 Pitch 连杆，控制小臂弯曲/伸直 |
| 0021 | `LINK_ELBOW_YAW_L` | 左肘偏航 | 左臂肘关节 Yaw 连杆，控制小臂旋转 |
| 0022 | `LINK_WRIST_END_L` | 左手腕末端 | 左臂末端 Body，不含视觉几何体，仅作碰撞 |
| 0023 | `LINK_SHOULDER_PITCH_R` | 右肩俯仰 | 右臂肩关节 Pitch 连杆 |
| 0024 | `LINK_SHOULDER_ROLL_R` | 右肩横滚 | 右臂肩关节 Roll 连杆 |
| 0025 | `LINK_SHOULDER_YAW_R` | 右肩偏航 | 右臂肩关节 Yaw 连杆 |
| 0026 | `LINK_ELBOW_PITCH_R` | 右肘俯仰 | 右臂肘关节 Pitch 连杆 |
| 0027 | `LINK_ELBOW_YAW_R` | 右肘偏航 | 右臂肘关节 Yaw 连杆 |
| 0028 | `LINK_WRIST_END_R` | 右手腕末端 | 右臂末端 Body |
| 0029 | `LINK_HEAD_PITCH` | 头部俯仰 | 头部 Pitch 连杆，控制头部前后点头 |
| 0030 | `LINK_HEAD_YAW` | 头部偏航 | 头部 Yaw 连杆，控制头部左右转动 |

---

## 命名规则

| 缩写 | 全称 | 含义 |
|:---|:---|:---|
| `PITCH` | Pitch | 俯仰 — 绕水平轴（Y 轴）的前后旋转 |
| `ROLL` | Roll | 横滚 — 绕前后轴（X 轴）的左右旋转 |
| `YAW` | Yaw | 偏航 — 绕竖直轴（Z 轴）的水平旋转 |
| `_L` | Left | 左侧（机器人自身坐标系） |
| `_R` | Right | 右侧（机器人自身坐标系） |

---

## 层级结构

```
world
└── LINK_BASE                          ← 骨盆/底盘
    ├── LINK_HIP_PITCH_L               ← 左腿链
    │   └── LINK_HIP_ROLL_L
    │       └── LINK_HIP_YAW_L
    │           └── LINK_KNEE_PITCH_L
    │               └── LINK_ANKLE_PITCH_L
    │                   └── LINK_ANKLE_ROLL_L
    │                       └── LINK_FOOT_L
    ├── LINK_HIP_PITCH_R               ← 右腿链
    │   └── LINK_HIP_ROLL_R
    │       └── LINK_HIP_YAW_R
    │           └── LINK_KNEE_PITCH_R
    │               └── LINK_ANKLE_PITCH_R
    │                   └── LINK_ANKLE_ROLL_R
    │                       └── LINK_FOOT_R
    └── LINK_WAIST_YAW                 ← 腰部
        ├── LINK_SHOULDER_PITCH_L      ← 左臂链
        │   └── LINK_SHOULDER_ROLL_L
        │       └── LINK_SHOULDER_YAW_L
        │           └── LINK_ELBOW_PITCH_L
        │               └── LINK_ELBOW_YAW_L
        │                   └── LINK_WRIST_END_L
        ├── LINK_SHOULDER_PITCH_R      ← 右臂链
        │   └── LINK_SHOULDER_ROLL_R
        │       └── LINK_SHOULDER_YAW_R
        │           └── LINK_ELBOW_PITCH_R
        │               └── LINK_ELBOW_YAW_R
        │                   └── LINK_WRIST_END_R
        └── LINK_HEAD_PITCH            ← 头部链
            └── LINK_HEAD_YAW
```
