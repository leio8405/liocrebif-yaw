/**
 * 型号 → URL slug
 * - 部分型号含空格（如 'LKF-Fiber Adhesive'）→ 空格转连字符
 * - 同型号多规格产品（如 LKF-PM 下的绕环光纤 / 波导光纤 / 光子晶体光纤）
 *   通过产品自身的 slug 字段区分路由
 */
interface SlugSource {
  model: string;
  slug?: string;
}

export function productSlug(p: SlugSource): string {
  if (p.slug) return p.slug;
  return p.model.toLowerCase().replace(/\s+/g, '-');
}
