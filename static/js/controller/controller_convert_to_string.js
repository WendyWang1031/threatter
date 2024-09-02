export function stringifyObjectValues(data) {
  if (Array.isArray(data)) {
    return data.map((item) => stringifyObjectValues(item));
  } else if (data !== null && typeof data === "object") {
    const newObj = {};
    for (const key in data) {
      if (data.hasOwnProperty(key)) {
        newObj[key] = stringifyObjectValues(data[key]);
      }
    }
    return newObj;
  } else if (data === null) {
    return null;
  } else {
    return String(data);
  }
}
