/** @param {number} ms */
export const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Traverse the DOM upwards and checks the computed styles
 * of each element is passes. Compares the value of the
 * requested property with the passed value and returns
 * the element if the value is a match
 *
 * @param   {HTMLElement|null} element Element to start from.
 * @param   {string} property CSS property to research.
 * @param   {string} value Value to compare CSS property value with.
 * @returns {HTMLElement|null}
 */
export const findParentWithCSS = (element, property, value) => {
	element = element?.parentElement || null;
	while (element !== null) {
		const style = window.getComputedStyle(element);
		const propValue = style.getPropertyValue(property);
		if (propValue === value) {
			return element;
		}
		element = element.parentElement;
	}
	return null;
};
