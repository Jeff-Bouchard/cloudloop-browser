export const getDownloadLink = siaLink => {
  if (siaLink.startsWith("sia://")) {
    return "https://siasky.net/" + siaLink.substring(5);
  } else {
    return siaLink;
  }
};

function toUTF8Array(str) {
  var utf8 = [];
  for (var i=0; i < str.length; i++) {
      var charcode = str.charCodeAt(i);
      if (charcode < 0x80) utf8.push(charcode);
      else if (charcode < 0x800) {
          utf8.push(0xc0 | (charcode >> 6), 
                    0x80 | (charcode & 0x3f));
      }
      else if (charcode < 0xd800 || charcode >= 0xe000) {
          utf8.push(0xe0 | (charcode >> 12), 
                    0x80 | ((charcode>>6) & 0x3f), 
                    0x80 | (charcode & 0x3f));
      }
      // surrogate pair
      else {
          i++;
          // UTF-16 encodes 0x10000-0x10FFFF by
          // subtracting 0x10000 and splitting the
          // 20 bits of 0x0-0xFFFFF into two halves
          charcode = 0x10000 + (((charcode & 0x3ff)<<10)
                    | (str.charCodeAt(i) & 0x3ff));
          utf8.push(0xf0 | (charcode >>18), 
                    0x80 | ((charcode>>12) & 0x3f), 
                    0x80 | ((charcode>>6) & 0x3f), 
                    0x80 | (charcode & 0x3f));
      }
  }
  return utf8;
}

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
  let hue = (hashResult % 359) / 360.0;
  let saturationIndex = (hue*180) % (saturationArray.count-1) + 1
  let lightnessIndex = (hue*180) % (saturationArray.count-1) + 1
  return `hsl(${hue}, ${saturationArray[saturationIndex]}, ${lightnessArray[lightnessIndex]})`;
}