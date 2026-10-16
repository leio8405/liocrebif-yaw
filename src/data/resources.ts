/**
 * Resources（长尾内容页）数据源
 * 每篇文章一个对象；正文 sections 用 HTML 字符串（内链指向产品详情页）
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
  readingTime: number; // 分钟
  tag: string;
  sections: ResourceSection[];
  faq: ResourceFaq[];
  relatedProducts: { model: string; href: string; caption: string }[];
  relatedCategory: { name: string; href: string };
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
  },
];

export function getResource(slug: string) {
  return resources.find((r) => r.slug === slug);
}
