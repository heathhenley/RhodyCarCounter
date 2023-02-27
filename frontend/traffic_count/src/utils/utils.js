export const  cameraNameToAWSLink = (name) => {
  let aws = "https://rhodycarcounter.s3.amazonaws.com/";
  return aws + name.toLowerCase().replace('/', '_') + ".jpg";
}
