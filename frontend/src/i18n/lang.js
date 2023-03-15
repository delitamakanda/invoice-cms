import { createI18n } from 'vue-i18n';
import en from '@/i18n/en.json';

const defaultLocale = 'en';

const languages = {
    en: en,
}

const messages = Object.assign(languages);

export const i18n = createI18n({
    legacy: false,
    locale: defaultLocale,
    fallbackLocale: 'en',
    messages,
});
