import { en } from './translations/en';
import { zh } from './translations/zh';

const translations = { en, zh } as const;

export const languages = {
  en: 'English',
  zh: '中文',
};

export const defaultLang = 'en';

export type Lang = keyof typeof translations;

export function getLangFromUrl(url: URL): Lang {
  const [, lang] = url.pathname.split('/');
  if (lang in translations) return lang as Lang;
  return defaultLang;
}

export function useTranslations(lang: Lang) {
  return function t(key: string): string {
    return translations[lang][key as keyof typeof translations[Lang]] || translations[defaultLang][key as keyof typeof translations[Lang]] || key;
  };
}

export function translatePath(path: string, lang: Lang): string {
  // 外部链接原样返回
  if (/^https?:\/\//.test(path)) return path;
  // Remove existing /zh prefix if any
  let cleanPath = path.replace(/^\/zh/, '') || '/';
  // 页面路由统一补尾斜杠：canonical 带斜杠，少补会让每次抓取多一跳 308
  if (!cleanPath.endsWith('/')) cleanPath += '/';
  if (lang === defaultLang) return cleanPath;
  return `/zh${cleanPath}`;
}
