// ============================================================
//  产品数据 —— 全站产品信息的唯一来源
// ============================================================
//  想更新产品？只改这个文件，不用碰其他任何页面。
//  每个产品的英文和中文内容并排放在一起，一起改，不会漏。
//
//  改完三步发布：
//    1. npm run dev   本地预览确认效果（localhost:4321）
//    2. npm run build 构建
//    3. git push      推送后网站自动更新
//
//  新增一个产品 = 复制一段 { ... } 改内容，加在对应分类的数组里。
//  删掉一个产品 = 删掉对应的 { ... } 整段。
//
//  图片：image 填网络地址，或把图片文件放到 public/images/products/
//  文件夹，然后写 '/images/products/图片文件名.png'。
//  没有图片就删掉 image 行，会自动显示 emoji 占位图标。
// ============================================================

export interface Product {
  model: string;        // 型号，如 'LKF-FS60'
  tagEn: string;        // 分类标签（英文）
  tagZh: string;        // 分类标签（中文）
  nameEn: string;       // 产品名称（英文）
  nameZh: string;       // 产品名称（中文）
  descEn: string;       // 产品描述（英文）
  descZh: string;       // 产品描述（中文）
  specs?: string;       // 规格参数，如 '6×6×3 cm | RS-422 输出'（可留空）
  includesEn?: string;  // 配置清单说明（英文，可留空）
  includesZh?: string;  // 配置清单说明（中文，可留空）
  appsEn: string[];     // 应用领域标签（英文）
  appsZh: string[];     // 应用领域标签（中文）
  image?: string;       // 产品图片地址（可留空，留空显示 emoji）
  emoji?: string;       // 没有图片时的占位图标（可留空）
  shortEn?: string;     // 产品总览页显示的短名称（英文，可留空）
  shortZh?: string;     // 产品总览页显示的短名称（中文，可留空）
  subEn?: string;       // 产品总览页显示的副标题（英文，可留空）
  subZh?: string;       // 产品总览页显示的副标题（中文，可留空）
}

// ------------------------------------------------------------
//  分类一：陀螺仪系统（Gyroscope Systems）
// ------------------------------------------------------------
export const gyroscopes: Product[] = [
  {
    model: 'LKF-FS60',
    tagEn: 'FOG Gyro',
    tagZh: 'FOG 陀螺仪',
    nameEn: 'Single Axis Medium-High Precision FOG',
    nameZh: '单轴中高精度光纤陀螺仪 (FOG)',
    descEn: 'Miniaturized closed-loop FOG with 135μm thin PM fiber technology. Compact, fast start-up, RS-422 output.',
    descZh: '采用 135μm 细径保偏 (PM) 光纤技术的小型化闭环 FOG。结构紧凑、启动快速、RS-422 输出。',
    specs: '6×6×3 cm | RS-422 Digital Output',
    appsEn: ['Electro-optical Pod', 'Flight Control', 'Platform Stabilizer', 'Light UAV'],
    appsZh: ['光电吊舱', '飞行控制', '平台稳定', '轻型无人机'],
    image: 'https://cowork-storage-public-cdn.lx.netease.com/lxbg/2024/10/30/b17433d3ad3d413380bbdb2ed6a5c43e.png',
    shortEn: 'Medium-High Precision FOG',
    shortZh: '中高精度 FOG',
  },
  {
    model: 'LKF-FS50A/X',
    tagEn: 'FOG Gyro',
    tagZh: 'FOG 陀螺仪',
    nameEn: 'Single Axis Medium-Low Precision FOG',
    nameZh: '单轴中低精度光纤陀螺仪 (FOG)',
    descEn: 'Compact closed-loop FOG with breakthrough miniaturized design. 135μm thin PM fiber technology reduces coil size. Pure solid-state, high reliability, ideal for medium-low precision inertial navigation and control applications.',
    descZh: '紧凑型闭环 FOG，采用突破性的小型化设计。135μm 细径保偏光纤技术缩小了光纤环体积。纯固态、高可靠，适用于中低精度惯性导航与控制应用。',
    specs: '5×5×3.65 cm | RS-422 Digital Output',
    appsEn: ['Optical Platform', 'Satcom on the Move', 'IMU', 'Light UAV'],
    appsZh: ['光学平台', '动中通卫星通信', 'IMU', '轻型无人机'],
    image: 'https://cowork-storage-public-cdn.lx.netease.com/lxbg/2024/11/26/86c40da8a47542398ab60942bda42052.png',
    shortEn: 'Medium-Low Precision FOG',
    shortZh: '中低精度 FOG',
  },
  {
    model: 'LKF-F3X90',
    tagEn: 'FOG IMU',
    tagZh: 'FOG IMU',
    nameEn: 'Three-Axis High Precision FOG IMU',
    nameZh: '三轴高精度 FOG 惯性测量单元 (IMU)',
    descEn: 'Navigation-grade tri-axis FOG inertial measurement unit for missile guidance and attitude control. Pure solid-state design, high engineering maturity, cost-effective. Full digital RS-422 output.',
    descZh: '导航级三轴 FOG 惯性测量单元，用于导弹制导与姿态控制。纯固态设计，工程成熟度高，性价比优异。全数字 RS-422 输出。',
    specs: '9×9×7.8 cm | RS-422 Output',
    appsEn: ['Missile Navigation', 'Guided Bombs', 'Attitude Control', 'Navigation Guidance'],
    appsZh: ['导弹导航', '制导炸弹', '姿态控制', '导航制导'],
    image: 'https://cowork-storage-public-cdn.lx.netease.com/lxbg/2024/10/31/615113fbaf064eb197b770d9ec6da6e2.png',
    shortEn: 'Tri-Axis High Precision FOG',
    shortZh: '三轴高精度 FOG',
  },
  {
    model: 'LKF-MBG100A',
    tagEn: 'MEMS Gyro',
    tagZh: 'MEMS 陀螺仪',
    nameEn: 'Dual Axis MEMS Gyro Combination',
    nameZh: '双轴 MEMS 陀螺仪组合',
    descEn: 'High-bandwidth, low-latency, low-noise dual-axis MEMS gyro for servo stabilization. 100% localized components. In-situ replacement for flexure gyros. 4KHz sampling, -40°C to +80°C calibrated.',
    descZh: '高带宽、低延迟、低噪声的双轴 MEMS 陀螺仪，用于伺服稳定。元器件 100% 国产化。可直接替换挠性陀螺仪。4KHz 采样，-40°C 至 +80°C 全温标定。',
    specs: '21.5×21.5×28 cm | 4KHz Sampling',
    appsEn: ['Guide Head Stabilization', 'Optoelectronic Pod', 'Servo Control', 'Stable Platforms'],
    appsZh: ['导引头稳定', '光电吊舱', '伺服控制', '稳定平台'],
    image: 'https://cowork-storage-public-cdn.lx.netease.com/lxbg/2024/11/06/6c238c1a6a44426ab7d576c702361d3a.png',
    shortEn: 'Dual Axis MEMS Gyro',
    shortZh: '双轴 MEMS 陀螺仪',
  },
];

// ------------------------------------------------------------
//  分类二：光纤系统（Fiber Optic Systems）
// ------------------------------------------------------------
export const fiberOptic: Product[] = [
  {
    model: 'LKF-RH16',
    tagEn: 'Core Equipment',
    tagZh: '核心设备',
    nameEn: 'Multi-Pole Fiber Coil Winding Machine',
    nameZh: '多极光纤环绕丝机',
    descEn: 'Multi-pole winding system with automatic glue coating. Real-time display of winding parameters.',
    descZh: '多极缠绕系统，配备自动涂胶功能。实时显示缠绕参数。',
    includesEn: 'Includes: fiber take-up, laying and pay-off devices, tension sensing, coil skeleton fixing spindle, fiber guiding, automatic gluing, industrial control computer + display, HD camera system, 2× standard rewinding spools.',
    includesZh: '包含：光纤收丝、排丝与放线装置，张力传感，光纤环骨架固定主轴，光纤导向，自动涂胶，工控机 + 显示屏，高清摄像系统，2 个标准复绕盘。',
    appsEn: ['Quadrupole Winding', 'Octupole Winding', 'Automatic Glue Coating', 'Precision Fiber Laying'],
    appsZh: ['四极缠绕', '八极缠绕', '自动涂胶', '精密排纤'],
    image: 'https://cowork-storage-public-cdn.lx.netease.com/lxbg/2024/11/01/7c8932c0c3be441e86c1435ed082538f.jpg',
    shortEn: 'Multi-Pole Coil Winding Machine',
    shortZh: '多极光纤环绕丝机',
  },
  {
    model: 'FOG Series',
    tagEn: 'FOG Components',
    tagZh: 'FOG 元器件',
    nameEn: 'Fiber Optic Gyroscope Components',
    nameZh: '光纤陀螺仪 (FOG) 元器件',
    descEn: 'Complete range of FOG optical sub-assemblies and components including PM fiber coils, optical chips, couplers, and source modules. All manufactured in-house with proprietary thin-fiber (135μm) technology for miniaturized FOG solutions.',
    descZh: '全系列 FOG 光学组件与元器件，包括保偏 (PM) 光纤环、光学芯片、耦合器及光源模块。全部采用自主细径光纤 (135μm) 技术在内部制造，助力 FOG 小型化。',
    appsEn: ['PM Fiber Coils', 'Optical Chips', 'Couplers', 'Source Modules'],
    appsZh: ['保偏光纤环', '光学芯片', '耦合器', '光源模块'],
    image: 'https://cowork-storage-public-cdn.lx.netease.com/lxbg/2024/11/20/7e6da8cb18ee42ef9a6a429da5cc97a4.png',
    shortEn: 'FOG Components',
    shortZh: 'FOG 元器件',
  },
  {
    model: 'Calibration Series',
    tagEn: 'Calibration',
    tagZh: '标定',
    nameEn: 'Measuring & Calibration Equipment',
    nameZh: '测量与标定设备',
    descEn: 'Precision turntables, rate tables, and environmental testing equipment for FOG and MEMS sensor calibration. Production-grade instruments ensuring every device meets specified performance parameters.',
    descZh: '用于 FOG 与 MEMS 传感器标定的精密转台、速率转台及环境测试设备。量产级仪器，确保每台设备均达到规定性能参数。',
    appsEn: ['Rate Tables', 'Precision Turntables', 'Environmental Testing', 'Sensor Calibration'],
    appsZh: ['速率转台', '精密转台', '环境测试', '传感器标定'],
    emoji: '📐',
    shortEn: 'Measuring & Calibration Equipment',
    shortZh: '测量与标定设备',
  },
];

// ------------------------------------------------------------
//  分类三：惯性导航系统（Inertial Navigation Systems）
// ------------------------------------------------------------
export const inertialNavigation: Product[] = [
  {
    model: 'LKF-FS300',
    tagEn: 'FOG INS',
    tagZh: 'FOG INS',
    nameEn: 'Fiber Optical Integrated Navigation System',
    nameZh: '光纤组合导航系统',
    descEn: 'Tactical-grade FOG-based GNSS/INS with self-alignment and RTK navigation for aircraft, ships, and UAVs.',
    descZh: '基于 FOG 的战术级 GNSS/INS 组合导航系统，具备自对准和 RTK 导航功能，适用于飞机、舰船和无人机 (UAV)。',
    specs: '21.2×15.5×12.5 cm',
    appsEn: ['Aircraft Navigation', 'UAV/Vehicle/Ship', 'Attitude Reference'],
    appsZh: ['飞机导航', '无人机/车辆/舰船', '姿态参考'],
    image: 'https://cowork-storage-public-cdn.lx.netease.com/lxbg/2024/11/01/9916fd75af594a13b9785080e2784c4c.png',
    shortEn: 'FOG Integrated Navigation System',
    shortZh: 'FOG 组合导航系统',
    subEn: 'Tactical-grade GNSS/INS',
    subZh: '战术级 GNSS/INS',
  },
  {
    model: 'LKF-MG300K',
    tagEn: 'North Seeker',
    tagZh: '寻北仪',
    nameEn: 'Microminiature MEMS North Seeker',
    nameZh: '微小型 MEMS 寻北仪',
    descEn: 'Six-axis MEMS inertial sensor combo for north-seeking, navigation and attitude control. Full temperature compensation (-45°C to +80°C), 4KHz high-speed sampling, vibration-resistant sealed design.',
    descZh: '六轴 MEMS 惯性传感器组合，用于寻北、导航和姿态控制。全温补偿 (-45°C 至 +80°C)，4KHz 高速采样，抗振密封设计。',
    specs: '4.7×4.7×3.15 cm',
    appsEn: ['North Seeking', 'Drilling Systems', 'Vehicle/Vessel Attitude', 'Satcom on-the-Move'],
    appsZh: ['寻北', '钻探系统', '车辆/舰船姿态', '动中通卫星通信'],
    image: 'https://cowork-storage-public-cdn.lx.netease.com/lxbg/2024/11/07/d6d76718798c4d3896e8cad69a483aca.png',
    shortEn: 'Microminiature MEMS North Seeker',
    shortZh: '微小型 MEMS 寻北仪',
    subEn: 'GPS-independent heading',
    subZh: '不依赖 GPS 的航向测量',
  },
  {
    model: 'LKF-MG204B',
    tagEn: 'MEMS IMU',
    tagZh: 'MEMS IMU',
    nameEn: 'Medium Precision MEMS Inertial Measurement Unit',
    nameZh: '中精度 MEMS 惯性测量单元 (IMU)',
    descEn: 'Six-axis MEMS inertial attitude system with full-temperature calibration. In-situ replacement for STIM300. 1KHz sampling, sealed design for harsh environments. High-performance gyro + accelerometer integration.',
    descZh: '六轴 MEMS 惯性姿态系统，全温标定。可直接替换 STIM300。1KHz 采样，严苛环境密封设计。高性能陀螺仪 + 加速度计集成。',
    specs: '4.48×3.86×2.15 cm',
    appsEn: ['UAV Attitude Reference', 'Mobile Mapping', 'Missile Flight Control', 'Radar Stabilization'],
    appsZh: ['无人机姿态参考', '移动测绘', '导弹飞行控制', '雷达稳定'],
    image: 'https://cowork-storage-public-cdn.lx.netease.com/lxbg/2024/11/07/03e2fdf743744e00b8f04cec5c8a1cc2.png',
    shortEn: 'Medium Precision MEMS IMU',
    shortZh: '中精度 MEMS IMU',
    subEn: 'STIM300 in-situ replacement',
    subZh: '可直接替换 STIM300',
  },
];

// ------------------------------------------------------------
//  产品总览页（/products）用的分类数据
//  按顺序展示三大产品线，products 指向上面对应的数组
// ------------------------------------------------------------
export const productCategories = [
  {
    slug: 'inertial-navigation-systems',
    products: inertialNavigation,
  },
  {
    slug: 'gyroscopes',
    products: gyroscopes,
  },
  {
    slug: 'fiber-optic',
    products: fiberOptic,
  },
];
