// 产品数据类型定义（全站唯一来源：src/data/products/ 目录）

export interface SpecRow {
  k: string;   // 参数名（中文）
  kEn: string; // 参数名（英文）
  v: string[];   // 参数值（中文站显示）
  vEn: string[]; // 参数值（英文站显示）
}

export interface SpecTable {
  headers: string[];      // 列头（单型号两列表 = ['项目','技术指标']）
  rows: SpecRow[];
}

export interface Product {
  model: string;        // 型号，如 'LKF-FS60'
  tagEn: string;        // 分类标签（英文）
  tagZh: string;        // 分类标签（中文）
  nameEn: string;       // 产品名称（英文）
  nameZh: string;       // 产品名称（中文）
  descEn?: string;      // 产品描述（英文）
  descZh?: string;      // 产品描述（中文）
  specTable?: SpecTable; // 完整参数表（详情页渲染）
  appsEn?: string[];    // 应用领域标签（英文）
  appsZh?: string[];    // 应用领域标签（中文）
  image?: string;       // 产品图片地址（可留空）
  shortEn?: string;     // 产品总览页显示的短名称（英文，可留空）
  shortZh?: string;     // 产品总览页显示的短名称（中文，可留空）
  subEn?: string;       // 产品总览页显示的副标题（英文，可留空）
  subZh?: string;       // 产品总览页显示的副标题（中文，可留空）
}
