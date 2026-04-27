import { ClipLoader } from "react-spinners";

const override = {
  display: "block",
  margin: "0 auto",
  borderColor: "purple",
};

const SmallSpinner = () => {
  return (
    <ClipLoader
      cssOverride={override}
      size={25}
      aria-label="Loading Spinner"
      data-testid="loader"
    />
  );
};

export default SmallSpinner;