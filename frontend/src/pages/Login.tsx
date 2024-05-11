import { Helmet } from "react-helmet";
import Form from "../components/Form";
import NavigationBar from "../components/NavigationBar";

const Login = () => {
  return (
    <>
    <Helmet>
      <title>Login</title>
    </Helmet>
    <div>
      <NavigationBar />
      <Form route="api/v1.0/login" method="login" />
    </div>
    </>
  );
};

export default Login;
