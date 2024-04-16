import Form from "../components/Form";
import NavigationBar from "../components/NavigationBar";

const Login = () => {
  return (
    <div>
      <NavigationBar />
      <Form route="api/v1.0/login" method="login" />
    </div>
  );
};

export default Login;
