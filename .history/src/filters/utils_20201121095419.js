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

export const strHash = stringToHash => {
  result = UInt64(5381);
  buf = toUTF8Array(stringToHash);
  for (var b in buf) {
    result = 127 * (result & 0x00ffffffffffffff) + UInt64(b);
  }
  return result;
}

export const getColorForString = stringToHash => {
  var saturationArray = [0.35, 0.5, 0.65];
  var lightnessArray = [0.35, 0.5, 0.65];
  const hash = strHash(stringToHash);
  let hue = (hash % 359) / 360.0;
  let saturationIndex = Int(hue*180) % (saturationArray.count-1) + 1
  let lightnessIndex = Int(hue*180) % (saturationArray.count-1) + 1
  return hsl(hue, saturationArray[saturationIndex], lightnessArray[lightnessIndex])
}