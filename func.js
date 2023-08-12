const GetYearMonth = (timestamp) => {
	let date = new Date(timestamp);
	let year = date.getFullYear();
	let month = date.getMonth() + 1;
	return `${year}年${month}月`;
};

const urlToToObj = (url) => {
	const obj = {};
	if (url) {
		const params = url.split('&');
		params.map(item => obj[item.split("=")[0]] = item.split("=")[1]);
	}
	return obj;
}

const getOptions = (options) => {
	return options.map((item, index) => ({
		value: index,
		text: item
	}))
}

const cleanEmpty = (object) => {
	for (let i of Object.keys(object)) {
		if (object[i] === "") object[i] = null
	}
	return object
}

export {
	GetYearMonth,
	urlToToObj,
	getOptions,
	cleanEmpty
}