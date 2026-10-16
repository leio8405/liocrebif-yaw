/**
 * Resources（长尾内容页）数据源
 * 每篇文章一个对象；正文 sections 用 HTML 字符串（内链指向产品详情页）
 * zh 字段可选：有 zh 的文章生成中文版页面，没有则仅英文
 * 新增文章 = 复制一段对象改内容，页面自动生成
 */

export interface ResourceSection {
  h2: string;
  html: string;
}

export interface ResourceFaq {
  q: string;
  a: string;
}

export interface ResourceArticle {
  slug: string;
  title: string;
  description: string;
  date: string;
  readingTime: number;
  tag: string;
  sections: ResourceSection[];
  faq: ResourceFaq[];
  relatedProducts: { model: string; href: string; caption: string }[];
  relatedCategory: { name: string; href: string };
  zh?: {
    title: string;
    description: string;
    sections: ResourceSection[];
    faq: ResourceFaq[];
    caption: string;
  };
}

export const resources: ResourceArticle[] = [
  {
    slug: 'fog-vs-mems-imu',
    title: 'FOG vs MEMS IMU: How to Choose the Right Inertial Sensor',
    description:
      'Fiber optic gyroscopes and MEMS inertial sensors solve the same problem at very different points on the cost-performance curve. A practical framework for choosing between them.',
    date: '2026-10-16',
    readingTime: 6,
    tag: 'Technology',
    sections: [
      {
        h2: 'Two technologies, one decision',
        html: `<p>When engineers specify an inertial measurement unit (IMU), the first decision is almost always the sensing technology: fiber optic gyroscope (FOG) or micro-electro-mechanical system (MEMS). Both measure angular rate on three axes, and both feed the same navigation filters — but they sit at very different points on the trade-off curve between precision, size, power and cost.</p>
<p>Choose wrong, and you either overspend on performance you will never use, or ship a system that drifts in the field. This guide walks through how each technology works, where each excels, and a practical framework for choosing between them.</p>`,
      },
      {
        h2: 'How a fiber optic gyroscope works',
        html: `<p>A FOG measures rotation using the <strong>Sagnac effect</strong>: light from a source travels in both directions around a coil of polarization-maintaining fiber, and rotation of the coil shifts the interference pattern between the two counter-propagating beams. The shift is proportional to angular velocity — measured optically, with no moving parts.</p>
<p>Because there is no spinning rotor or vibrating structure, a FOG is a truly solid-state sensor: nothing wears out, performance is largely insensitive to vibration and mounting orientation, and long-term bias stability is excellent. Modern FOGs use thin polarization-maintaining fiber (135 μm or less) to shrink the coil, which is why navigation-grade performance now fits in surprisingly compact packages.</p>`,
      },
      {
        h2: 'How a MEMS gyroscope works',
        html: `<p>A MEMS gyroscope instead measures the <strong>Coriolis force</strong> acting on a microscopic vibrating structure. The sensing element is etched from silicon in wafer batches, which makes MEMS devices small, light, low-power and inexpensive at volume.</p>
<p>Precision has improved dramatically over the past decade — tactical-grade MEMS gyros now reach bias stability figures that were reserved for FOGs fifteen years ago, and their mechanical robustness (surviving shocks above 1,000 g) opens applications no optical sensor can touch. But at the high-accuracy end, physics still favors the optical approach.</p>`,
      },
      {
        h2: 'Head-to-head comparison',
        html: `<p>Representative figures for current production devices in each class:</p>
<table class="w-full text-sm border-collapse">
  <thead>
    <tr class="border-b border-gray-300 text-left">
      <th class="py-2 pr-4 font-semibold">Parameter</th>
      <th class="py-2 pr-4 font-semibold">FOG IMU</th>
      <th class="py-2 pr-4 font-semibold">MEMS IMU</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Gyro bias stability</td><td class="py-2 pr-4">0.01–0.1 °/h</td><td class="py-2 pr-4">1–10 °/h</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Typical weight</td><td class="py-2 pr-4">150 g – 3.5 kg</td><td class="py-2 pr-4">50 g class</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Power</td><td class="py-2 pr-4">2–10 W</td><td class="py-2 pr-4">0.5–1.5 W</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Shock survival</td><td class="py-2 pr-4">Moderate</td><td class="py-2 pr-4">1,000 g+</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Service life</td><td class="py-2 pr-4">20+ years, no wear-out</td><td class="py-2 pr-4">Long, degrades with vibration dose</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Relative cost</td><td class="py-2 pr-4">Higher</td><td class="py-2 pr-4">Lower</td></tr>
  </tbody>
</table>`,
      },
      {
        h2: 'Where a FOG wins',
        html: `<ul class="list-disc pl-5 space-y-2">
<li><strong>Navigation-grade accuracy.</strong> Bias stability at the 0.05 °/h level keeps dead-reckoning error acceptable over long GNSS-denied stretches.</li>
<li><strong>Long missions without GNSS.</strong> The slower the drift, the longer the platform can operate between absolute position fixes.</li>
<li><strong>Vibration-heavy optical platforms.</strong> No moving mass means no vibration-rectified error on gimbal-stabilized payloads.</li>
<li><strong>Long service life.</strong> Nothing wears out — important for systems expected to stay in service for decades.</li>
</ul>`,
      },
      {
        h2: 'Where a MEMS wins',
        html: `<ul class="list-disc pl-5 space-y-2">
<li><strong>SWaP-constrained platforms.</strong> Small UAVs, gimbals and handheld systems where every gram and milliamp matters.</li>
<li><strong>Battery-powered systems.</strong> Sub-watt power budgets that a FOG cannot meet.</li>
<li><strong>High-shock environments.</strong> Munitions, launchers and ejection scenarios in excess of 1,000 g.</li>
<li><strong>Cost-sensitive volume production.</strong> When a few degrees per hour is genuinely good enough.</li>
</ul>`,
      },
      {
        h2: 'A practical decision framework',
        html: `<p>Three questions settle most selections:</p>
<p><strong>1. What drift can your mission tolerate?</strong> Estimate the dead-reckoning error budget over the longest GNSS-denied segment. If a tactical MEMS IMU (around 10 °/h bias stability) drifts beyond it, you are in FOG territory.</p>
<p><strong>2. What size, weight and power do you have?</strong> A FOG needs more of all three. If your platform cannot afford 2 W or a 150 g-class sensor, MEMS decides itself.</p>
<p><strong>3. What is the environment?</strong> Sustained high shock favors MEMS; sustained vibration with a demanding stability budget favors FOG.</p>
<p>For example, a medium-precision FOG with 0.05 °/h bias stability suits electro-optical pods, flight control and platform stabilization — see our <a href="/products/lkf-fs60/" class="text-blue-700 underline">single-axis FOG LKF-FS60</a>. A GNSS-aided tactical MEMS IMU at the 10 °/h class fits small UAV navigation — see the <a href="/products/lkf-msu105/" class="text-blue-700 underline">LKF-MSU105 integrated navigation system</a>.</p>`,
      },
    ],
    faq: [
      {
        q: 'Can MEMS replace FOG in navigation systems?',
        a: 'With RTK-aided GNSS and short GNSS-denied segments, tactical MEMS IMUs handle many navigation tasks that previously required FOG. For long pure-inertial stretches or navigation-grade accuracy, FOG remains the default choice.',
      },
      {
        q: 'Are fiber optic gyroscopes affected by magnetic fields?',
        a: 'FOGs have no magnetically sensitive moving mass, and their magnetic sensitivity is typically specified below 0.5 °/h/G — negligible for most platforms.',
      },
      {
        q: 'What does "bias stability" mean?',
        a: 'It is the residual constant offset in the gyro output after averaging out noise, usually quoted in degrees per hour at 1σ over a 10 s or 100 s smoothing interval. It is the primary factor that determines how fast a pure-inertial solution drifts.',
      },
    ],
    relatedProducts: [
      { model: 'LKF-FS60', href: '/products/lkf-fs60/', caption: 'Single-axis medium-high precision FOG' },
      { model: 'LKF-MSU105', href: '/products/lkf-msu105/', caption: 'Micro MEMS integrated navigation system' },
    ],
    relatedCategory: { name: 'IMU & North Seekers', href: '/products/imu/' },
    zh: {
      title: '光纤陀螺 vs MEMS IMU：如何选择合适的惯性传感器',
      description: '光纤陀螺与 MEMS 惯性传感器在精度、体积、功耗与成本的权衡曲线上处于完全不同的位置。本文给出一套实用的选型框架。',
      sections: [
        {
          h2: '两种技术，一个决策',
          html: `<p>工程师在选型惯性测量单元（IMU）时，第一个决策几乎总是敏感技术路线：光纤陀螺（FOG）还是微机电系统（MEMS）。两者都测量三轴角速度，都为相同的导航滤波器提供数据——但它们在精度、体积、功耗与成本的权衡曲线上处于完全不同的位置。</p>
<p>选错了，你要么为永远用不到的性能多花成本，要么让系统在现场使用中漂移超差。本文介绍两种技术的工作原理、各自的优势场景，以及一套实用的选型框架。</p>`,
        },
        {
          h2: '光纤陀螺的工作原理',
          html: `<p>FOG 基于<strong>萨格纳克效应（Sagnac effect）</strong>测量旋转：光源发出的光沿保偏光纤线圈双向传播，线圈旋转会使两束反向传播光的干涉条纹发生偏移，偏移量与角速度成正比——以光学方式测量，没有任何运动部件。</p>
<p>由于没有旋转转子或振动结构，FOG 是真正的固态传感器：无磨损、性能对振动和安装方位不敏感、长期零偏稳定性优异。现代 FOG 采用细径保偏光纤（135 μm 及以下）缩小线圈体积，这也是导航级性能如今能装进紧凑封装的原因。</p>`,
        },
        {
          h2: 'MEMS 陀螺的工作原理',
          html: `<p>MEMS 陀螺则通过测量作用于微型振动结构上的<strong>科里奥利力</strong>来感知旋转。敏感元件以晶圆批量工艺从硅片上刻蚀而来，因此 MEMS 器件体积小、重量轻、功耗低、批量成本低。</p>
<p>过去十年 MEMS 精度大幅提升——战术级 MEMS 陀螺的零偏稳定性已达到十五年前 FOG 的水平，其机械鲁棒性（可承受 1,000 g 以上冲击）更是打开了光学传感器无法进入的应用。但在高精度端，物理规律仍偏向光学方案。</p>`,
        },
        {
          h2: '正面对比',
          html: `<p>两类现役器件的代表性指标：</p>
<table class="w-full text-sm border-collapse">
  <thead>
    <tr class="border-b border-gray-300 text-left">
      <th class="py-2 pr-4 font-semibold">参数</th>
      <th class="py-2 pr-4 font-semibold">FOG IMU</th>
      <th class="py-2 pr-4 font-semibold">MEMS IMU</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">陀螺零偏稳定性</td><td class="py-2 pr-4">0.01–0.1 °/h</td><td class="py-2 pr-4">1–10 °/h</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">典型重量</td><td class="py-2 pr-4">150 g – 3.5 kg</td><td class="py-2 pr-4">50 g 级</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">功耗</td><td class="py-2 pr-4">2–10 W</td><td class="py-2 pr-4">0.5–1.5 W</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">抗冲击</td><td class="py-2 pr-4">中等</td><td class="py-2 pr-4">1,000 g+</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">使用寿命</td><td class="py-2 pr-4">20 年以上，无磨损</td><td class="py-2 pr-4">较长，随振动剂量退化</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">相对成本</td><td class="py-2 pr-4">较高</td><td class="py-2 pr-4">较低</td></tr>
  </tbody>
</table>`,
        },
        {
          h2: 'FOG 的优势场景',
          html: `<ul class="list-disc pl-5 space-y-2">
<li><strong>导航级精度。</strong>0.05 °/h 级零偏稳定性让长距离 GNSS 拒止段的航位推算误差保持在可接受范围。</li>
<li><strong>无 GNSS 长航时任务。</strong>漂移越慢，两次绝对位置修正之间的作业时间越长。</li>
<li><strong>强振动光学平台。</strong>无运动质量，稳定云台载荷上不存在振动整流误差。</li>
<li><strong>长服役寿命。</strong>无磨损——对需要服役数十年的系统尤为重要。</li>
</ul>`,
        },
        {
          h2: 'MEMS 的优势场景',
          html: `<ul class="list-disc pl-5 space-y-2">
<li><strong>SWaP 受限平台。</strong>小型无人机、吊舱与手持系统——每一克、每一毫安都很关键。</li>
<li><strong>电池供电系统。</strong>FOG 无法满足的亚瓦级功耗预算。</li>
<li><strong>高冲击环境。</strong>弹药、发射装置与弹射等超过 1,000 g 的场景。</li>
<li><strong>成本敏感的批量生产。</strong>当每小时几度确实够用时。</li>
</ul>`,
        },
        {
          h2: '实用选型框架',
          html: `<p>三个问题可以解决大多数选型：</p>
<p><strong>1. 你的任务能容忍多大漂移？</strong>估算最长 GNSS 拒止段的航位推算误差预算。如果战术级 MEMS IMU（约 10 °/h 零偏稳定性）的漂移超出预算，就需要 FOG。</p>
<p><strong>2. 你有多少体积、重量和功耗？</strong>FOG 三项需求都更高。如果平台承受不了 2 W 或 150 g 级传感器，MEMS 是必然选择。</p>
<p><strong>3. 环境如何？</strong>持续高冲击偏向 MEMS；稳定预算苛刻的持续振动环境偏向 FOG。</p>
<p>例如：0.05 °/h 零偏稳定性的中精度 FOG 适合光电吊舱、飞行控制与平台稳定——见我们的<a href="/zh/products/lkf-fs60/" class="text-blue-700 underline">单轴 FOG LKF-FS60</a>；10 °/h 级 GNSS 辅助战术 MEMS IMU 适合小型无人机导航——见 <a href="/zh/products/lkf-msu105/" class="text-blue-700 underline">LKF-MSU105 组合导航系统</a>。</p>`,
        },
      ],
      faq: [
        {
          q: 'MEMS 能在导航系统中取代 FOG 吗？',
          a: '在 RTK 辅助 GNSS、GNSS 拒止段较短的条件下，战术级 MEMS IMU 可以胜任许多过去需要 FOG 的导航任务。但对于长纯惯导航段或导航级精度要求，FOG 仍是默认选择。',
        },
        {
          q: '光纤陀螺会受磁场影响吗？',
          a: 'FOG 没有对磁场敏感的运动质量，其磁场敏感度通常标定为低于 0.5 °/h/G——对大多数平台可以忽略。',
        },
        {
          q: '"零偏稳定性"是什么意思？',
          a: '它是陀螺输出在噪声平均后的残余常值偏移，通常以 1σ、10 s 或 100 s 平滑区间下的每小时度数表示。它决定了纯惯导解算漂移速度，是首要指标。',
        },
      ],
      caption: '单轴中高精度光纤陀螺仪',
    },
  },
  {
    slug: 'how-fiber-optic-gyroscope-works',
    title: 'How a Fiber Optic Gyroscope Works: From Sagnac Effect to Navigation-Grade Sensing',
    description:
      'The physics and engineering behind fiber optic gyroscopes: the Sagnac effect, the optical readout chain, why thin polarization-maintaining fiber matters, and what bias stability really tells you.',
    date: '2026-10-16',
    readingTime: 7,
    tag: 'Technology',
    sections: [
      {
        h2: 'Measuring rotation with light',
        html: `<p>A fiber optic gyroscope (FOG) answers a deceptively simple question — "is this platform rotating, and how fast?" — using nothing but light and physics. No spinning rotor, no vibrating proof mass, no bearings. Understanding how it achieves navigation-grade accuracy from a coil of optical fiber explains both why FOGs dominate high-precision inertial navigation and why they keep getting smaller.</p>`,
      },
      {
        h2: 'The Sagnac effect',
        html: `<p>The principle was demonstrated by Georges Sagnac in 1913. Split a beam of light and send both halves around a closed loop in opposite directions, then rotate the loop: the beam travelling "with" the rotation covers its path in slightly more time than the beam travelling "against" it. The resulting phase difference between the two beams is proportional to the rotation rate.</p>
<p>In a FOG, the loop is a coil of polarization-maintaining (PM) fiber — often hundreds of meters or kilometers of it, wound into a compact package. More fiber length means more accumulated phase shift, which is why coil design is central to FOG performance.</p>`,
      },
      {
        h2: 'The optical readout chain',
        html: `<p>A complete FOG is an integrated optical system with five key elements:</p>
<ul class="list-disc pl-5 space-y-2">
<li><strong>Light source</strong> — typically a superluminescent diode (SLD) or fiber source, chosen for its short coherence length and low phase noise.</li>
<li><strong>Source coupler</strong> — splits the light into the two counter-propagating waves.</li>
<li><strong>PM fiber coil</strong> — the sensing element, where the Sagnac phase shift accumulates.</li>
<li><strong>Integrated optics modulator (Y-junction / MIOC)</strong> — applies a phase modulation bias and closes the control loop, converting the tiny Sagnac signal into a measurable, linear output.</li>
<li><strong>Detector and transimpedance amplifier</strong> — converts the returning interference signal into a digital reading.</li>
</ul>
<p>Every element must preserve polarization and minimize back-reflection, which is why FOG manufacturers tend to produce their own fiber, couplers and integrated optics in-house rather than sourcing them like commodity parts.</p>`,
      },
      {
        h2: 'Why thin fiber matters',
        html: `<p>The industry trend over the last decade has been toward thinner polarization-maintaining fiber — 135 μm and below, versus the classical 250 μm cladding. Thinner fiber allows more turns in the same coil volume, which directly increases the Sagnac sensitivity, while reducing the coil mass that would otherwise limit dynamic performance.</p>
<p>Producing reliable thin PM fiber at volume requires proprietary coating and winding processes; it is one of the main technical barriers between assemblers and true FOG manufacturers.</p>`,
      },
      {
        h2: 'What "bias stability" really measures',
        html: `<p>The single most important datasheet number for a FOG is <strong>bias stability</strong>, usually quoted in degrees per hour at 1σ over a 10 s or 100 s smoothing interval. It represents how much the gyro's zero point wanders after all noise is averaged out — and therefore how fast a pure-inertial solution drifts.</p>
<p>Practical reference points: industrial-grade FOGs sit around 0.2–1 °/h; medium-high precision devices reach 0.05–0.1 °/h; navigation-grade instruments reach 0.01 °/h or below. Each order of magnitude typically expands the range of missions the sensor can support.</p>`,
      },
      {
        h2: 'Why engineers choose FOG',
        html: `<ul class="list-disc pl-5 space-y-2">
<li>No moving parts — nothing to wear out or mechanically fatigue.</li>
<li>Instant start-up compared with spinning-mass gyroscopes.</li>
<li>Insensitivity to magnetic fields and acceleration (no g-sensitivity from moving mass).</li>
<li>Excellent scale-factor linearity across the full dynamic range.</li>
</ul>
<p>These properties are why FOGs remain the default choice for electro-optical payloads, platform stabilization, surveying systems and any application where navigation must survive without GNSS.</p>`,
      },
    ],
    faq: [
      {
        q: 'Why does a FOG need such a long fiber coil?',
        a: 'The Sagnac phase shift is proportional to the enclosed area of the light path. More fiber turns mean more area and higher sensitivity, which is why coil design (fiber length, diameter and winding precision) defines the accuracy class of the instrument.',
      },
      {
        q: 'What limits FOG accuracy?',
        a: 'The main limits are shot noise at the detector, polarization crosstalk in the coil, and small time-varying errors in the electronics. These are all engineering-managed rather than fundamental — which is why bias stability keeps improving with each generation of fiber and electronics.',
      },
      {
        q: 'Do FOGs wear out?',
        a: 'No. A FOG has no bearings or moving mass, so there is no mechanical wear mechanism. Long-term drift comes from component aging, which is characterized at calibration and compensated in the navigation algorithm.',
      },
    ],
    relatedProducts: [
      { model: 'LKF-FS60', href: '/products/lkf-fs60/', caption: 'Single-axis medium-high precision FOG' },
      { model: 'LKF-FSI301', href: '/products/lkf-fsi301/', caption: 'Fiber optical integrated navigation system' },
    ],
    relatedCategory: { name: 'Fiber Optic Gyroscopes', href: '/products/fog-gyroscopes/' },
  },
  {
    slug: 'north-seeker-vs-gnss-heading',
    title: 'North Seeker vs GNSS Heading: When GPS Isn\'t Enough',
    description:
      'GNSS dual-antenna heading and gyroscopic north seeking solve the same problem with opposite failure modes. A practical comparison for platform engineers choosing between them.',
    date: '2026-10-16',
    readingTime: 6,
    tag: 'Application',
    sections: [
      {
        h2: 'Heading is harder than position',
        html: `<p>Modern GNSS receivers give you position to within centimeters — but heading is a different story. A single antenna tells you where you are, not which way you are pointing. For platform orientation, weapon-line-of-sight stabilization, antenna pointing or drilling orientation, you need true heading — and the two dominant ways to get it, GNSS dual-antenna systems and gyroscopic north seekers, fail in exactly opposite conditions.</p>`,
      },
      {
        h2: 'How GNSS dual-antenna heading works',
        html: `<p>A dual-antenna GNSS receiver measures the carrier-phase difference between two antennas separated by a known baseline, and derives heading from that vector. Performance depends on baseline length and sky visibility: with a clean sky and a meter-class baseline, heading accuracy of 0.1–0.2° is achievable, and RTK corrections tighten position to centimeters.</p>
<p>The failure modes follow directly: blocked or reflected satellite signals (urban canyons, tree canopy, mines, tunnels), multipath around large metal structures, and — critically — <strong>jamming and spoofing</strong>, which are no longer hypothetical in many operating regions.</p>`,
      },
      {
        h2: 'How a gyroscopic north seeker works',
        html: `<p>A MEMS north seeker measures the component of <strong>Earth\'s rotation</strong> sensed by its gyroscopes. Because the planet rotates at a known rate (15.04°/h), a gyroscope on a stationary platform can determine true north from that signal alone — no satellites, no baseline, no external infrastructure. High-precision MEMS north seekers reach 0.1–0.5° (1σ) heading accuracy while stationary, and maintain orientation through short GNSS-denied periods via inertial propagation.</p>
<p>The limitation is the mirror image: a north seeker determines orientation, not position, and its accuracy applies when the platform is relatively static or moving slowly. Long-duration mobile operation still needs GNSS or another absolute reference for position.</p>`,
      },
      {
        h2: 'Head-to-head comparison',
        html: `<table class="w-full text-sm border-collapse">
  <thead>
    <tr class="border-b border-gray-300 text-left">
      <th class="py-2 pr-4 font-semibold">Parameter</th>
      <th class="py-2 pr-4 font-semibold">GNSS Dual-Antenna</th>
      <th class="py-2 pr-4 font-semibold">MEMS North Seeker</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Heading source</td><td class="py-2 pr-4">Satellite carrier phase</td><td class="py-2 pr-4">Earth rotation (gyroscopic)</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Typical accuracy</td><td class="py-2 pr-4">0.1–0.2° (clean sky)</td><td class="py-2 pr-4">0.1–0.5° (1σ, static)</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Works indoors / underground</td><td class="py-2 pr-4">No</td><td class="py-2 pr-4">Yes (static)</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Jamming / spoofing immunity</td><td class="py-2 pr-4">None</td><td class="py-2 pr-4">Immune</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Moving platform</td><td class="py-2 pr-4">Yes (continuous)</td><td class="py-2 pr-4">Static / low dynamics</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Position</td><td class="py-2 pr-4">Yes (cm with RTK)</td><td class="py-2 pr-4">No (heading only)</td></tr>
  </tbody>
</table>`,
      },
      {
        h2: 'In practice: the two work together',
        html: `<p>In most real systems the answer is not either/or — it is a hybrid. A typical architecture uses a MEMS integrated navigation system (gyroscope + accelerometer + GNSS) for continuous position and attitude, with a north-seeking mode for initial alignment before the platform moves, and pure-inertial propagation through short GNSS outages.</p>
<p>This is exactly how modern MEMS-based navigation units are designed: the GNSS receiver provides absolute position and heading corrections when available, while the inertial sensors bridge the gaps — in tunnels, under bridges, in valleys, and in jammed environments.</p>`,
      },
      {
        h2: 'Choosing for your application',
        html: `<ul class="list-disc pl-5 space-y-2">
<li><strong>Mining, tunnels, drilling orientation.</strong> No sky, no GNSS — a north seeker (or a navigation unit with north-seeking mode) is the only option.</li>
<li><strong>Antenna and payload stabilization.</strong> Jamming immunity and gimbal-mounted sensors favor inertial heading.</li>
<li><strong>Open-sky vehicles with continuous GNSS.</strong> Dual-antenna GNSS heading is simple and effective — paired with a MEMS IMU for attitude continuity.</li>
<li><strong>Military and security platforms.</strong> Assume GNSS will be denied at some point; inertial north-finding is the resilient baseline.</li>
</ul>`,
      },
    ],
    faq: [
      {
        q: 'Does a MEMS north seeker work indoors?',
        a: 'Yes — when stationary. It senses Earth\'s rotation, which is present everywhere. That is why north seekers are used in mines, tunnels and indoor surveying where satellites cannot reach.',
      },
      {
        q: 'What does "secL" mean in heading accuracy?',
        a: 'It is the secant of the local latitude. Gyroscopic north-finding accuracy degrades toward the poles because the vertical component of Earth\'s rotation shrinks; at mid latitudes the effect is modest.',
      },
      {
        q: 'Can a north seeker replace GNSS completely?',
        a: 'For heading, yes — it is fully independent of satellites. For position, no: a north seeker determines orientation only. Practical systems combine both, using inertial sensors to bridge GNSS outages.',
      },
    ],
    relatedProducts: [
      { model: 'LKF-MSN300', href: '/products/lkf-msn300/', caption: 'High-precision MEMS north seeker' },
      { model: 'LKF-MSU105', href: '/products/lkf-msu105/', caption: 'Micro MEMS integrated navigation system' },
    ],
    relatedCategory: { name: 'IMU & North Seekers', href: '/products/imu/' },
  },
];

export function getResource(slug: string) {
  return resources.find((r) => r.slug === slug);
}
