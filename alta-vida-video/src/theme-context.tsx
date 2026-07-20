import {createContext, useContext} from 'react';
import type {Theme} from './theme';

const ThemeContext = createContext<Theme | null>(null);

export const ThemeProvider = ThemeContext.Provider;

export const useTheme = (): Theme => {
	const ctx = useContext(ThemeContext);
	if (!ctx) {
		throw new Error('useTheme() debe usarse dentro de <ThemeProvider value={...}>');
	}
	return ctx;
};
