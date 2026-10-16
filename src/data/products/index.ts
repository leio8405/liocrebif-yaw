// 产品分类汇总（自动生成）
import { fogGyros } from './fog';
import { memsGyros } from './mems-gyroscopes';
import { imus } from './imu';
import { insSystems } from './ins';
import { accelerometers } from './accelerometers';
import { devices } from './devices';
export type { Product } from './types';
export { fogGyros, memsGyros, imus, insSystems, accelerometers, devices };
export interface ProductCategory {
  slug: string;
  titleEn: string;
  titleZh: string;
  descEn: string;
  descZh: string;
  products: Product[];
}

export const productCategories: ProductCategory[] = [
  {
    slug: 'fog-gyroscopes',
    titleEn: 'Fiber Optic Gyroscopes',
    titleZh: '光纤陀螺系列',
    descEn: 'Single-axis to tri-axis FOG from industrial to navigation grade',
    descZh: '从工业级到导航级的单轴至三轴光纤陀螺',
    products: fogGyros,
  },
  {
    slug: 'mems-gyroscopes',
    titleEn: 'MEMS Gyroscopes',
    titleZh: 'MEMS 陀螺系列',
    descEn: 'MEMS gyro chips and multi-axis combinations',
    descZh: 'MEMS 陀螺芯片与多轴组合',
    products: memsGyros,
  },
  {
    slug: 'imu',
    titleEn: 'IMU & North Seekers',
    titleZh: 'IMU 与寻北仪',
    descEn: 'FOG & MEMS inertial measurement units and north seekers',
    descZh: '光纤与 MEMS 惯性测量单元及寻北仪',
    products: imus,
  },
  {
    slug: 'inertial-navigation-systems',
    titleEn: 'INS / GNSS Navigation',
    titleZh: 'INS 组合导航',
    descEn: 'Tactical-grade integrated navigation systems',
    descZh: '战术级组合导航系统',
    products: insSystems,
  },
  {
    slug: 'accelerometers',
    titleEn: 'Accelerometers',
    titleZh: '加速度计',
    descEn: 'Quartz and MEMS accelerometers',
    descZh: '石英与 MEMS 加速度计',
    products: accelerometers,
  },
  {
    slug: 'fiber-optic',
    titleEn: 'Fiber Devices & Equipment',
    titleZh: '光纤器件与设备',
    descEn: 'Fiber, components, winding machines and test equipment',
    descZh: '光纤器件、绕制与测试设备',
    products: devices,
  },
];
