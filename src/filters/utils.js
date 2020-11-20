export const getDownloadLink = siaLink => {
  if (siaLink.startsWith("sia://")) {
    return "https://siasky.net/" + siaLink.substring(5);
  } else {
    return siaLink;
  }
};
