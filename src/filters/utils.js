export const getWavDownloadFromProxy = siaLink => {
  if (siaLink.startsWith("sia://")) {
    return "https://dev.cloudloop.io/download?skylink=" + siaLink;
  } else {
    return siaLink;
  }
};

export const getGenericSkynetDownloadLink = siaLink => {
  if (siaLink.startsWith("sia://")) {
    return "https://siasky.net/" + siaLink.substring(5);
  } else {
    return siaLink;
  }
};

export const sessionViewFilter = session_raw => {
    session_raw.picture = getGenericSkynetDownloadLink(session_raw.picture);
    session_raw.private = session_raw.private === "true";
    return session_raw;
}

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

function hslToHex(h, s, l) {
  h /= 360;
  s /= 100;
  l /= 100;
  let r, g, b;
  if (s === 0) {
    r = g = b = l; // achromatic
  } else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    };
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1 / 3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1 / 3);
  }
  const toHex = x => {
    const hex = Math.round(x * 255).toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  };
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

export const getColorForString = stringToHash => {
  var saturationArray = [35, 50, 65];
  var lightnessArray = [35, 50, 65];
  const hashResult = stringToHash.hashCode();
  let hue = Math.abs(hashResult % 359.0);
  let saturationIndex = (hue*180) % (saturationArray.length-1) + 1
  let lightnessIndex = (hue*180) % (saturationArray.length-1) + 1
  return hslToHex(hue, saturationArray[saturationIndex], lightnessArray[lightnessIndex]);
}

