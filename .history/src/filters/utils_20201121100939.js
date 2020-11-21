export const getDownloadLink = siaLink => {
  if (siaLink.startsWith("sia://")) {
    return "https://siasky.net/" + siaLink.substring(5);
  } else {
    return siaLink;
  }
};

Object.defineProperty(String.prototype, 'hashCode', {
  value: function() {
    var hash = 0, i, chr;
    for (i = 0; i < this.length; i++) {
      chr   = this.charCodeAt(i);
      hash  = ((hash << 5) - hash) + chr;
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
  }
});

export const getColorForString = stringToHash => {
  var saturationArray = [0.35, 0.5, 0.65];
  var lightnessArray = [0.35, 0.5, 0.65];
  const hashResult = stringToHash.hashCode();
  console.log(hashResult);
  let hue = Math.abs((hashResult % 359.0) / 360.0);
  let saturationIndex = (hue*180) % (saturationArray.length-1) + 1
  let lightnessIndex = (hue*180) % (saturationArray.length-1) + 1
  return `hsl(${hue}, ${saturationArray[saturationIndex]}, ${lightnessArray[lightnessIndex]})`;
}