/**
 * Weather helper utilities
 */

import PhSun from '~icons/ph/sun-duotone';
import PhCloudSun from '~icons/ph/cloud-sun-duotone';
import PhCloud from '~icons/ph/cloud-duotone';
import PhCloudFog from '~icons/ph/cloud-fog-duotone';
import PhCloudRain from '~icons/ph/cloud-rain-duotone';
import PhCloudSnow from '~icons/ph/cloud-snow-duotone';
import PhCloudLightning from '~icons/ph/cloud-lightning-duotone';
import PhMoon from '~icons/ph/moon-duotone';
import PhCloudMoon from '~icons/ph/cloud-moon-duotone';
import PhDrop from '~icons/ph/drop-duotone';
import PhSnowflake from '~icons/ph/snowflake-duotone';
import weatherDescriptions from './descriptions.json';

/**
 * Map WMO weather codes to human-readable descriptions
 * @param {number} code - WMO weather code
 * @param {boolean} isDay - Whether it's daytime (defaults to true)
 * @returns {string} Weather description
 */
export function getWeatherDescription(code, isDay = true) {
	const timeOfDay = isDay ? 'day' : 'night';
	const description = weatherDescriptions[code]?.[timeOfDay]?.description;
	return description || 'Unknown';
}

/**
 * Get weather icon component based on WMO weather code
 * @param {number} code - WMO weather code
 * @param {boolean} isDay - Whether it's daytime (defaults to true)
 * @returns {Component} Svelte icon component
 */
export function getWeatherIcon(code, isDay = true) {
	// Clear sky (0, 1)
	if (code === 0 || code === 1) {
		return isDay ? PhSun : PhMoon;
	}

	// Partly cloudy (2)
	if (code === 2) {
		return isDay ? PhCloudSun : PhCloudMoon;
	}

	// Cloudy (3)
	if (code === 3) {
		return PhCloud;
	}

	// Fog (45, 48)
	if (code === 45 || code === 48) {
		return PhCloudFog;
	}

	// Drizzle (51, 53, 55, 56, 57)
	if (code >= 51 && code <= 57) {
		return PhDrop;
	}

	// Rain (61, 63, 65, 66, 67)
	if (code >= 61 && code <= 67) {
		return PhCloudRain;
	}

	// Snow (71, 73, 75, 77)
	if (code >= 71 && code <= 77) {
		return PhSnowflake;
	}

	// Rain showers (80, 81, 82)
	if (code >= 80 && code <= 82) {
		return PhCloudRain;
	}

	// Snow showers (85, 86)
	if (code === 85 || code === 86) {
		return PhCloudSnow;
	}

	// Thunderstorm (95, 96, 99)
	if (code >= 95 && code <= 99) {
		return PhCloudLightning;
	}

	// Default fallback
	return PhCloud;
}

/**
 * Get weather icon color based on WMO weather code
 * @param {number} code - WMO weather code
 * @returns {string} CSS color variable name
 */
export function getWeatherIconColor(code) {
	// Clear sky (0, 1) - Sun/Moon
	if (code === 0 || code === 1) {
		return 'var(--yellow-2)'; // Yellow for sun
	}

	// Partly cloudy (2) - CloudSun/CloudMoon
	if (code === 2) {
		return 'var(--yellow-1)'; // Light yellow for partly cloudy
	}

	// Cloudy (3) - Cloud
	if (code === 3) {
		return 'var(--txt-4)'; // Light gray for clouds
	}

	// Fog (45, 48) - CloudFog
	if (code === 45 || code === 48) {
		return 'var(--txt-4)'; // Light gray for fog
	}

	// Drizzle (51, 53, 55, 56, 57) - Drop
	if (code >= 51 && code <= 57) {
		return 'var(--blue-2)'; // Blue for drizzle
	}

	// Rain (61, 63, 65, 66, 67) - CloudRain
	if (code >= 61 && code <= 67) {
		return 'var(--blue-2)'; // Blue for rain
	}

	// Snow (71, 73, 75, 77) - Snowflake
	if (code >= 71 && code <= 77) {
		return 'var(--blue-1)'; // Light blue for snow
	}

	// Rain showers (80, 81, 82) - CloudRain
	if (code >= 80 && code <= 82) {
		return 'var(--blue-2)'; // Blue for rain showers
	}

	// Snow showers (85, 86) - CloudSnow
	if (code === 85 || code === 86) {
		return 'var(--blue-1)'; // Light blue for snow showers
	}

	// Thunderstorm (95, 96, 99) - CloudLightning
	if (code >= 95 && code <= 99) {
		return 'var(--txt-4)'; // Light gray for thunderstorms
	}

	// Default fallback
	return 'var(--txt-4)'; // Light gray for unknown conditions
}

/**
 * Get day of week from date string
 * @param {string} dateString - Date in YYYY-MM-DD format
 * @returns {string} Abbreviated day of week
 */
export function getDayOfWeek(dateString) {
	const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
	const date = new Date(dateString);
	return days[date.getDay()];
}
