const GetYearMonth = (timestamp) => {
    let date = new Date(timestamp);
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    return `${year}年${month}月`;
};

const GetFullTime = (timestamp) => {
    let date = new Date(timestamp);
    return date.toISOString().substring(0, 19).replace("T", " ");
};

export { GetYearMonth, GetFullTime };
