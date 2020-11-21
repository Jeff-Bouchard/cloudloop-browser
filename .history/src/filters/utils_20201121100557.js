export const getDownloadLink = siaLink => {
  if (siaLink.startsWith("sia://")) {
    return "https://siasky.net/" + siaLink.substring(5);
  } else {
    return siaLink;
  }
};

function hash(obj) {

  var cache = [];

  function sanitize(obj) {
    if (obj === null) { return obj; }
    if (['undefined', 'boolean', 'number', 'string', 'function'].indexOf(typeof(obj)) >= 0) { return obj; }
    if (typeof(obj)==='object') {
      var keys = Object.keys(obj).sort(),
          values = [];
      for(var i=0; i<keys.length; i++){
        var value = obj[keys[i]];
        if (cache.indexOf(value) === -1) {
          values.push(sanitize(value));
          cache.push(value);
        } else {
          values.push('[ Previously hashed object ]');
        }
      }
      return [keys, values];
    }
  }

  return JSON.stringify(sanitize(obj));

}

export const getColorForString = stringToHash => {
  var saturationArray = [0.35, 0.5, 0.65];
  var lightnessArray = [0.35, 0.5, 0.65];
  const hashResult = hash(stringToHash);
  console.log(hashResult);
  let hue = (hashResult % 359.0) / 360.0;
  let saturationIndex = (hue*180) % (saturationArray.count-1) + 1
  let lightnessIndex = (hue*180) % (saturationArray.count-1) + 1
  return `hsl(${hue}, ${saturationArray[saturationIndex]}, ${lightnessArray[lightnessIndex]})`;
}