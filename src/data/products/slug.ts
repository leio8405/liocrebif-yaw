/**
 * 型号 → URL slug
 * 部分型号含空格（如 'LKF-Fiber Adhesive'），必须转成连字符才能生成合法 URL
 */
export function productSlug(model: string): string {
  return model.toLowerCase().replace(/\s+/g, '-');
}
