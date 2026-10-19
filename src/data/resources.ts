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
    slug: 'gnss-denied-navigation-solutions',
    title: 'GNSS-Denied Navigation: 5 Approaches Compared',
    description:
      'When GNSS is jammed, spoofed or simply unavailable, five navigation approaches keep a platform on track. How pure inertial navigation, gyroscopic north finding, terrain-referenced, visual and magnetic navigation compare — and how to architect around an outage.',
    date: '2026-10-19',
    readingTime: 6,
    tag: 'Technology',
    sections: [
      {
        h2: 'Why GNSS-denied navigation is now a design requirement',
        html: `<p>Satellite positioning has stopped being something you can assume. Receivers are jammed around conflict zones, spoofed in contested airspace, and simply unreachable underground, underwater, indoors and between tall buildings. <strong>GNSS-denied navigation</strong> — keeping a valid position, velocity and attitude solution when satellites are unavailable or unreliable — has moved from a military niche to a standard requirement for UAVs, ground vehicles, marine platforms and drilling tools. This guide compares the five main ways to achieve <strong>navigation without GPS</strong>: pure inertial navigation, gyroscopic north finding, terrain-referenced navigation, visual navigation and magnetic navigation, and shows where each one earns its place.</p>`,
      },
      {
        h2: 'The five approaches at a glance',
        html: `<p>No single source solves every outage. In practice a resilient architecture layers several of them, with inertial sensors at the core. The table below summarizes what each approach contributes:</p>
<table class="w-full text-sm border-collapse">
  <thead>
    <tr class="border-b border-gray-300 text-left">
      <th class="py-2 pr-4 font-semibold">Approach</th>
      <th class="py-2 pr-4 font-semibold">What it provides</th>
      <th class="py-2 pr-4 font-semibold">External dependencies</th>
      <th class="py-2 pr-4 font-semibold">Typical fit</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Pure inertial (FOG/MEMS INS)</td><td class="py-2 pr-4">Continuous position, velocity and attitude by dead reckoning</td><td class="py-2 pr-4">None — fully self-contained, jam-immune</td><td class="py-2 pr-4">UAVs, vehicles, vessels, drilling tools</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Gyroscopic north finding</td><td class="py-2 pr-4">True heading from Earth rotation</td><td class="py-2 pr-4">None — passive measurement of Earth&#39;s spin</td><td class="py-2 pr-4">Pre-mission alignment, downhole and mining orientation</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Terrain-referenced navigation</td><td class="py-2 pr-4">Position updates by matching altitude profiles to a terrain database</td><td class="py-2 pr-4">Terrain relief, stored database</td><td class="py-2 pr-4">Low-altitude flight over mapped terrain</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Visual navigation (VIO)</td><td class="py-2 pr-4">Position and attitude from camera feature tracking</td><td class="py-2 pr-4">Light and visible texture</td><td class="py-2 pr-4">Indoor UAVs, inspection, last-mile delivery</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Magnetic anomaly navigation</td><td class="py-2 pr-4">Coarse position fixes by geomagnetic map matching</td><td class="py-2 pr-4">Regional magnetic maps; passive but low resolution</td><td class="py-2 pr-4">Long-endurance backup layer</td></tr>
  </tbody>
</table>`,
      },
      {
        h2: 'Pure inertial navigation: the backbone',
        html: `<p>An inertial navigation system integrates angular rate from gyroscopes and specific force from accelerometers to produce position, velocity and attitude at high update rate, with no transmissions and no dependency on any external station. That makes it the only approach that works everywhere, all the time — and also the one whose error grows with time, because every gyro bias integrates into attitude, and attitude error tilts the acceleration vector into the position solution.</p>
<p>Gyro grade is therefore the design lever. A <a href="/products/lkf-fsi301/" class="text-blue-700 underline">FOG-based INS such as the LKF-FSI301</a> uses closed-loop fiber optic gyroscopes with a bias stability of ≤0.03 °/h (10 s smoothing) and an Allan bias instability of ≤0.006 °/h, plus self north-seeking to ≤0.1° × secL — a specification class intended for long unaided stretches on UAVs, ground vehicles and marine platforms. MEMS-grade systems trade drift rate for size, weight and cost, and are the right backbone when outages are short or aiding sources are frequent.</p>`,
      },
      {
        h2: 'Gyroscopic north finding: absolute heading without a signal',
        html: `<p>Dead reckoning is only as good as its heading. A heading error of 0.1° displaces the estimated position by roughly 17 m over 10 km of travel — and a magnetic compass cannot deliver reliable heading near steel structures, drill strings, vehicles or ore bodies. A gyroscopic north finder solves this by sensing the horizontal component of Earth rotation, which points to true north with no dependency on any magnetic or radio source.</p>
<p>North finders come in FOG and MEMS flavors. A compact <a href="/products/lkf-msn300/" class="text-blue-700 underline">MEMS north finder such as the LKF-MSN300</a> delivers self north-seeking accuracy of ≤1° × secL in a Φ31.8 × 85 mm, 145 g package drawing ≤2 W, rated from −40 to +120 °C — small and frugal enough to ride inside downhole surveying instruments and mining equipment, where satellites have never been an option and magnetic compasses have never worked.</p>`,
      },
      {
        h2: 'Aiding layers: terrain, vision and magnetics',
        html: `<p>The remaining three approaches do not replace inertial navigation; they bound its drift by supplying occasional absolute fixes:</p>
<ul class="list-disc pl-5 space-y-2">
<li><strong>Terrain-referenced navigation (TRN)</strong> compares a radar or lidar altitude profile with a stored terrain database. It gives solid position updates over rolling terrain at low altitude, but degrades over flat sea or featureless plains.</li>
<li><strong>Visual navigation</strong> tracks camera features to estimate motion (visual-inertial odometry). It is lightweight and works indoors and underground where nothing else does — provided there is light and texture — and it drifts without loop closures or absolute references.</li>
<li><strong>Magnetic anomaly navigation</strong> matches measured geomagnetic fields against maps. It is fully passive and unjammable, but coarse and region-dependent; it serves as a low-rate backup layer rather than a primary source.</li>
</ul>
<p>Each of these feeds updates to the INS filter, resetting accumulated drift while the inertial core carries the solution between fixes.</p>`,
      },
      {
        h2: 'Matching the approach to your outage profile',
        html: `<ul class="list-disc pl-5 space-y-2">
<li><strong>Outages of seconds to a couple of minutes</strong> (urban canyons, brief jamming): a tactical MEMS INS coasts through with negligible error; heavy sensors are unnecessary.</li>
<li><strong>Outages of tens of minutes to hours</strong> (contested airspace, sea crossings): navigation-grade FOG INS is the backbone — bias stability in the hundredths of a degree per hour is what buys the endurance.</li>
<li><strong>No GNSS, ever</strong> (underground, downhole, indoor): gyroscopic north finding for heading, plus dead reckoning or external aiding. A MEMS north finder makes this affordable enough for routine single-point surveying.</li>
<li><strong>Low altitude over mapped terrain</strong>: FOG INS plus terrain-referenced updates.</li>
</ul>
<p>The common thread: the longer and more frequent the outage, the more the architecture converges on a high-grade inertial core, with the other techniques supplying corrections around it.</p>`,
      },
      {
        h2: 'Designing a GNSS-denied architecture',
        html: `<p>There is no single answer to <strong>GPS jamming and signal loss</strong> — there is an error budget, an outage profile and an operating environment, and an architecture that matches them. Explore our <a href="/products/inertial-navigation-systems/" class="text-blue-700 underline">INS / GNSS combined navigation systems</a> to compare the FOG and MEMS options side by side, or share your platform, mission duration and expected outage conditions — our engineers will help you pick the sensor grade and aiding combination that closes the budget.</p>`,
      },
    ],
    faq: [
      {
        q: 'How long can an INS operate without GNSS before position errors grow unacceptable?',
        a: 'It depends almost entirely on gyro grade. With a constant gyro bias, position error grows roughly with the cube of time, so a navigation-grade system with 0.01–0.1 °/h-class gyros holds a useful solution for hours where a consumer MEMS unit drifts out within minutes. The practical answer comes from your own error budget: define the maximum acceptable position error for the mission, then work backward to the bias stability the gyro needs.',
      },
      {
        q: 'Why does heading accuracy matter more than anything else in GNSS-denied dead reckoning?',
        a: 'Because heading error acts on the full distance traveled: a heading error of 0.1° displaces the dead-reckoned position by about 17 m over 10 km, even with a perfect speed measurement. Heading is also the hardest quantity to obtain without satellites — magnetic compasses are distorted by nearby steel and current-carrying structures, which is why gyroscopic north finding is the standard answer underground and near machinery.',
      },
      {
        q: 'Can a MEMS north finder really find true north underground?',
        a: 'Yes. A north finder does not listen for signals; it measures the rotation of the Earth itself, so soil, rock and depth are irrelevant. That is exactly why MEMS north finders such as the LKF-MSN300 are used for mine orientation, oil-well surveying and pipeline work, where GNSS is unavailable and magnetic compasses are unusable near drill strings and ore bodies.',
      },
    ],
    relatedProducts: [
      { model: 'LKF-FSI301', href: '/products/lkf-fsi301/', caption: 'FOG/GNSS combined inertial navigation system' },
      { model: 'LKF-MSN300', href: '/products/lkf-msn300/', caption: 'High-precision MEMS north finder' },
    ],
    relatedCategory: { name: 'INS / GNSS Navigation', href: '/products/inertial-navigation-systems/' },
  },
  {
    slug: 'what-is-angle-random-walk',
    title: 'What Is Angle Random Walk (ARW) in IMU Datasheets?',
    description:
      'Angle random walk (ARW) in degrees per root-hour is the white-noise figure on every IMU datasheet. What the unit means, how it differs from bias stability, and how each drives navigation error on different timescales.',
    date: '2026-10-18',
    readingTime: 6,
    tag: 'Technology',
    sections: [
      {
        h2: 'The noise number that sets your short-term precision',
        html: `<p>On any IMU or gyroscope datasheet, <strong>angle random walk</strong> (ARW) is usually the second number after bias stability — and the most frequently misread one. Quoted in degrees per root-hour (°/√h), it describes the pure white noise at the gyro output: the error that remains no matter how carefully the sensor is calibrated. This guide explains what the ARW unit actually means, how <strong>angle random walk</strong> relates to gyro bias stability, how each one drives navigation error on a different timescale, and how to read the ARW row on a real spec table — using the three accuracy grades of a production FOG as a worked example.</p>`,
      },
      {
        h2: 'What degrees per root-hour actually means',
        html: `<p>ARW is the angular-error equivalent of white noise. If the gyro output noise were perfectly white — uncorrelated from sample to sample — then averaging reduces it in a very specific way: the standard deviation of the accumulated angle error grows with the <strong>square root of time</strong>, not linearly:</p>
<p><strong>σ(t) = ARW × √t</strong> (t in hours)</p>
<p>That square root is where the odd unit comes from, and it has two practical consequences:</p>
<ul class="list-disc pl-5 space-y-2">
<li><strong>Averaging pays diminishing returns.</strong> Doubling the averaging time improves the noise-limited angle by a factor of √2 (about 41%), not 2×.</li>
<li><strong>Short-time behavior is noise-dominated.</strong> Over one second, a 0.005 °/√h gyro contributes roughly 0.005/60 ≈ 0.0001° of noise-induced angle uncertainty — small in isolation, but exactly what an alignment filter has to average out before the navigation solution converges.</li>
</ul>`,
      },
      {
        h2: 'ARW vs bias stability: two different limits',
        html: `<p>ARW and bias stability are often confused because both are quoted in "degrees, hours" units. They describe physically different error processes, and each dominates on a different timescale:</p>
<table class="w-full text-sm border-collapse">
  <thead>
    <tr class="border-b border-gray-300 text-left">
      <th class="py-2 pr-4 font-semibold">Parameter</th>
      <th class="py-2 pr-4 font-semibold">Angle Random Walk</th>
      <th class="py-2 pr-4 font-semibold">Bias Stability</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Physical origin</td><td class="py-2 pr-4">White noise at the sensor output</td><td class="py-2 pr-4">Slowly varying residual offset</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Units</td><td class="py-2 pr-4">°/√h</td><td class="py-2 pr-4">°/h</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Attitude error growth</td><td class="py-2 pr-4">Proportional to √t</td><td class="py-2 pr-4">Proportional to t</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">On the Allan curve</td><td class="py-2 pr-4">The −1/2 slope region</td><td class="py-2 pr-4">The flat minimum</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Dominates</td><td class="py-2 pr-4">Short smoothing, alignment convergence, attitude jitter</td><td class="py-2 pr-4">Long unaided navigation drift</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Derivable from the other</td><td class="py-2 pr-4">No — independent processes</td><td class="py-2 pr-4">No</td></tr>
  </tbody>
</table>`,
      },
      {
        h2: 'Where ARW lives on the Allan deviation curve',
        html: `<p>The Allan deviation plot of a stationary gyro output shows both numbers at once. At short cluster times the curve falls with a −1/2 slope: read the value of that sloped line at t = 1 s and you have the ARW. As cluster time grows, the curve flattens and reaches a minimum — that minimum is the bias instability, and the datasheet "bias stability" figure (typically 1σ over a 10 s or 100 s smoothing interval) is taken near the bottom of the curve.</p>
<p>This is also why the two numbers cannot be converted into each other: they are two regions of one error curve, shaped by different physical processes — detector and photon noise on one side, slow drift of the electronics and optical path on the other.</p>`,
      },
      {
        h2: 'How ARW drives error in your system',
        html: `<p>Because the two error terms grow at different rates, which one matters depends on your timescale. A useful rule: <strong>bias error (B × t) equals random-walk error (N × √t) at t = (N/B)² hours</strong> — before that crossover ARW dominates, after it bias does.</p>
<p>Worked example with datasheet values. The <a href="/products/lkf-fs60/" class="text-blue-700 underline">LKF-FS60 single-axis FOG</a> ships in three accuracy grades — ARW ≤0.02 / ≤0.01 / ≤0.005 °/√h against bias stability ≤0.20 / ≤0.10 / ≤0.05 °/h (1σ, 10 s). For the highest grade:</p>
<ul class="list-disc pl-5 space-y-2">
<li><strong>At 1 second:</strong> noise contributes roughly 0.0001° of angle uncertainty — what the navigation filter averages through during initial alignment.</li>
<li><strong>At 1 hour unaided:</strong> the random-walk term contributes only ≤0.005°, while bias contributes up to ≤0.05° — bias is now the dominant error by an order of magnitude.</li>
<li><strong>Crossover:</strong> (N/B)² = (0.005/0.05)² = 0.01 h ≈ 36 s. Beyond about half a minute, improving bias helps the mission more than improving ARW.</li>
</ul>
<p>For gimbal and antenna stabilization the picture flips: the platform never integrates for minutes, so the <strong>short-term noise</strong> is what appears as line-of-sight jitter — and a lower-ARW grade is worth the premium even at equal bias.</p>`,
      },
      {
        h2: 'How to read the ARW row on a datasheet',
        html: `<ul class="list-disc pl-5 space-y-2">
<li><strong>Check the unit as printed.</strong> °/√h and °/√hr are the same quantity; a plain °/h in an ARW row is a typo and changes the number's meaning entirely.</li>
<li><strong>Read grade columns together.</strong> One model family usually spans several grades. On the FS60 table, ARW and bias stability scale together across grades — if a datasheet pairs a very low ARW with a poor bias (or the reverse) with no explanation, ask for the Allan plot.</li>
<li><strong>Note the test conditions.</strong> ARW is conventionally a room-temperature figure on a stable mount; vibration converts directly into extra noise, so a vibrating platform can easily see several times the datasheet ARW.</li>
<li><strong>Match the number to the job.</strong> For GNSS-aided navigation with long outages, bias stability sets the drift budget. For alignment speed, attitude hold and stabilization loops, ARW sets the noise floor. Compare both against the mission, not just the headline grade.</li>
</ul>`,
      },
      {
        h2: 'Choosing a gyro by its noise numbers',
        html: `<p>ARW tells you how quiet the sensor is; bias stability tells you how far it drifts. Reading them as one curve — noise at short times, drift at long times — turns two cryptic datasheet rows into a concrete error budget for your platform. If you are comparing grades for a stabilization or navigation task, the <a href="/products/lkf-fs60/" class="text-blue-700 underline">LKF-FS60 FOG series</a> documents ARW and bias stability side by side for all three grades, and our <a href="/products/imu/" class="text-blue-700 underline">IMU and north seeker lineup</a> covers the range from tactical MEMS to navigation-grade FOG. Share your error budget and platform profile, and our engineers will help match the grade to the mission.</p>`,
      },
    ],
    faq: [
      {
        q: 'Why is angle random walk quoted per root-hour instead of per hour?',
        a: 'Because the error it describes grows with the square root of time, not linearly. Averaging an angle random walk of N °/√h over t hours leaves N × √t degrees of uncertainty. The √h in the unit encodes that growth law, so the noise contribution at any averaging time can be computed directly.',
      },
      {
        q: 'Can I convert ARW to bias stability (or the other way)?',
        a: 'No. They characterize different, independent error processes: white noise versus slowly varying offset. Two gyros can share the same ARW and differ by an order of magnitude in bias stability. Both appear on the same Allan deviation curve, but in different regions of it.',
      },
      {
        q: 'What ARW value is good enough for my application?',
        a: 'Start from the shortest decision time your system cares about. Stabilization loops and alignment filters operate on the noise floor and reward low ARW directly. For long GNSS-denied navigation, bias stability dominates the drift budget and ARW matters mainly for how fast the solution converges after startup.',
      },
    ],
    relatedProducts: [
      { model: 'LKF-FS60', href: '/products/lkf-fs60/', caption: 'Single-axis medium-high precision FOG' },
    ],
    relatedCategory: { name: 'IMU & North Seekers', href: '/products/imu/' },
  },
  {
    slug: 'tactical-vs-navigation-grade-imu',
    title: 'Tactical vs Navigation-Grade IMU: What the Spec Numbers Mean',
    description:
      'Gyro bias stability is the single number that separates tactical-grade from navigation-grade IMUs. How to read the datasheet figures, and how to work backward from a drift budget to the right accuracy class.',
    date: '2026-10-17',
    readingTime: 6,
    tag: 'Technology',
    sections: [
      {
        h2: 'One number draws the line',
        html: `<p>When engineers compare inertial sensors, the conversation quickly reaches for shorthand: <strong>tactical grade IMU</strong> or <strong>navigation grade IMU</strong>. The line between the two <strong>IMU accuracy classes</strong> is drawn by a single datasheet figure — gyro bias stability, quoted in degrees per hour. A tactical-grade device drifts at roughly 1–10 °/h; a navigation-grade device drifts at 0.01–0.1 °/h. That order-of-magnitude gap decides which platforms each class can serve, and it is the first number to check. This guide explains what the classes actually mean, why bias stability dominates the error budget, and how to work backward from your mission's drift tolerance to the right class of sensor.</p>`,
      },
      {
        h2: 'What separates the two classes',
        html: `<p>Bias stability is not the only difference, but it drives most of the others. A navigation-grade gyro needs a long, precisely wound fiber coil and low-noise optics; a tactical-grade gyro can be a microscopic silicon structure etched by the thousands on a wafer. Everything in the table below follows from that choice of sensing technology:</p>
<table class="w-full text-sm border-collapse">
  <thead>
    <tr class="border-b border-gray-300 text-left">
      <th class="py-2 pr-4 font-semibold">Parameter</th>
      <th class="py-2 pr-4 font-semibold">Tactical-Grade IMU</th>
      <th class="py-2 pr-4 font-semibold">Navigation-Grade IMU</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Gyro bias stability</td><td class="py-2 pr-4">1–10 °/h</td><td class="py-2 pr-4">0.01–0.1 °/h</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Typical technology</td><td class="py-2 pr-4">MEMS vibrating gyro</td><td class="py-2 pr-4">Fiber optic gyroscope (FOG)</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Angle random walk</td><td class="py-2 pr-4">0.1–0.5 °/√h</td><td class="py-2 pr-4">0.005–0.02 °/√h</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Typical weight</td><td class="py-2 pr-4">Tens of grams</td><td class="py-2 pr-4">150 g – 3.5 kg</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Power</td><td class="py-2 pr-4">0.5–1.5 W</td><td class="py-2 pr-4">2–10 W</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Shock survival</td><td class="py-2 pr-4">500–1,000 g+</td><td class="py-2 pr-4">Moderate</td></tr>
    <tr class="border-b border-gray-200"><td class="py-2 pr-4">Typical platforms</td><td class="py-2 pr-4">Small UAVs, gimbals, munitions</td><td class="py-2 pr-4">Marine INS, long-endurance UAV, GNSS-denied military</td></tr>
  </tbody>
</table>`,
      },
      {
        h2: 'Why bias stability dominates the error budget',
        html: `<p>In a pure-inertial solution, the navigation filter integrates gyro output twice to produce attitude and position. Any residual bias — the constant offset left after the gyro's own noise is averaged out — is integrated along with the real rotation. The consequence is simple and unforgiving: <strong>attitude error grows linearly with time multiplied by bias</strong>.</p>
<p>A gyro with 10 °/h of bias stability that runs unaided for one minute can accumulate up to about 0.17° of attitude error; after ten minutes, 1.7°. A 0.03 °/h FOG running for a full hour accumulates just 0.03°. As the unaided interval stretches from minutes to hours, the two classes stop being comparable — which is why bias stability, not range or bandwidth, is the figure that defines the class.</p>`,
      },
      {
        h2: 'Which class fits which platform',
        html: `<ul class="list-disc pl-5 space-y-2">
<li><strong>Small multirotors and delivery drones.</strong> Continuous GNSS, short missions — a tactical MEMS IMU is the right class, and every gram counts.</li>
<li><strong>Electro-optical gimbals and SatCom-on-the-Move.</strong> Stabilization needs low noise and fast response more than long-term drift performance; tactical MEMS, or a single medium-precision FOG on the critical axis.</li>
<li><strong>Medium and long-endurance fixed-wing UAVs.</strong> Long sorties with periodic GNSS loss call for a FOG-based INS.</li>
<li><strong>Marine vessels and security platforms.</strong> Hours of operation, jamming assumed — navigation-grade FOG INS is the baseline.</li>
</ul>`,
      },
      {
        h2: 'Working backward from a drift budget',
        html: `<p>The practical selection method runs in the opposite direction: estimate what your mission can tolerate, then pick the class that stays inside it. Three questions do the job:</p>
<p><strong>1. How long can you run without GNSS?</strong> Multiply the longest expected unaided interval by the candidate's bias stability to get worst-case attitude drift. If a 10 °/h tactical device exceeds your budget in five minutes, you are shopping for FOG.</p>
<p><strong>2. How much SWaP can you spend?</strong> A micro MEMS unit like the <a href="/products/lkf-msu105/" class="text-blue-700 underline">LKF-MSU105</a> — ≤10 °/h bias stability, ≤0.5 W, 41.5 × 35.5 × 9.5 mm — fits a hand-launched UAV; with RTK corrections it holds 0.02 m + 1 ppm positioning. A FOG-based unit needs grams and watts the platform may not have.</p>
<p><strong>3. Does one axis carry the requirement?</strong> A single-axis FOG like the <a href="/products/lkf-fs60/" class="text-blue-700 underline">LKF-FS60</a> (bias stability grades from ≤0.20 down to ≤0.05 °/h at 1σ, 150 g) can upgrade the critical axis of an otherwise MEMS system at a fraction of a full FOG IMU's cost.</p>
<p>When the budget demands hours of unaided navigation, a FOG INS such as the <a href="/products/lkf-fsi301/" class="text-blue-700 underline">LKF-FSI301</a> — ≤0.03 °/h bias stability with ≤0.1° secL self north-seeking — is the class that closes the mission.</p>`,
      },
      {
        h2: 'From class to part number',
        html: `<p>Accuracy classes are a language, not a shopping list. Once you know which class your drift budget points to, the remaining datasheet lines — random walk, scale factor, vibration, temperature — narrow the field within that class. If you are mapping a requirement to a specific sensor, our <a href="/products/imu/" class="text-blue-700 underline">IMU and north seeker lineup</a> covers both classes, from 41.5 g-class MEMS units to 0.03 °/h FOG navigation systems, and our engineers can review a drift budget against your platform profile before you commit.</p>`,
      },
    ],
    faq: [
      {
        q: 'Can a MEMS IMU be navigation-grade?',
        a: 'Not in the strict sense. The best current MEMS devices reach tactical-class bias stability with excellent Allan bias instability, but their pure-inertial drift over hours remains far beyond what a navigation-grade FOG achieves. With continuous RTK-aided GNSS, however, a tactical MEMS IMU delivers navigation-quality position — the class distinction applies to unaided performance.',
      },
      {
        q: 'Does the accuracy class still matter if GNSS is always available?',
        a: 'For position, less so — GNSS corrections dominate. It still matters for attitude during outages: jamming, tunnels, foliage and urban canyons all interrupt satellites, and the higher the IMU class, the longer the solution stays trustworthy through the gap.',
      },
      {
        q: 'Which datasheet lines should I actually compare?',
        a: 'Start with gyro bias stability (note the smoothing interval and sigma convention — many datasheets quote 1σ over a 10 s average), then Allan bias instability, angle random walk, and the test conditions behind the numbers — full-temperature figures tell you more about field behavior than room-temperature ones.',
      },
    ],
    relatedProducts: [
      { model: 'LKF-MSU105', href: '/products/lkf-msu105/', caption: 'Micro MEMS integrated navigation system' },
      { model: 'LKF-FS60', href: '/products/lkf-fs60/', caption: 'Single-axis medium-high precision FOG' },
      { model: 'LKF-FSI301', href: '/products/lkf-fsi301/', caption: 'Fiber optical integrated navigation system' },
    ],
    relatedCategory: { name: 'IMU & North Seekers', href: '/products/imu/' },
  },
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
