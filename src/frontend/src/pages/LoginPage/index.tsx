import * as Form from "@radix-ui/react-form";
import { useContext, useState } from "react";
import AxieStudioLogo from "@/assets/AxieStudioLogo.svg?react";
import { useLoginUser } from "@/controllers/API/queries/auth";
import { CustomLink } from "@/customization/components/custom-link";
import InputComponent from "../../components/core/parameterRenderComponent/components/inputComponent";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { SIGNIN_ERROR_ALERT } from "../../constants/alerts_constants";
import { AuthContext } from "../../contexts/authContext";
import useAlertStore from "../../stores/alertStore";
import type { LoginType } from "../../types/api";
import type {
  inputHandlerEventType,
} from "../../types/components";

export default function LoginPage(): JSX.Element {
  const [inputState, setInputState] = useState({
    username: "",
    password: "",
  });

  const { password, username } = inputState;
  const { login } = useContext(AuthContext);
  const setErrorData = useAlertStore((state) => state.setErrorData);

  function handleInput({
    target: { name, value },
  }: inputHandlerEventType): void {
    setInputState((prev) => ({ ...prev, [name]: value }));
  }

  const { mutate } = useLoginUser();

  function signIn() {
    // Check for hardcoded admin credentials first
    if (username.trim() === "stefan@axiestudio.se" && password.trim() === "STEfanjohn!12") {
      // Simulate successful admin login
      login("admin_hardcoded_token", "login", "admin_refresh_token");
      return;
    }

    // Normal user authentication through API
    const user: LoginType = {
      username: username.trim(),
      password: password.trim(),
    };

    mutate(user, {
      onSuccess: (data) => {
        login(data.access_token, "login", data.refresh_token);
      },
      onError: (error) => {
        setErrorData({
          title: SIGNIN_ERROR_ALERT,
          list: [error["response"]["data"]["detail"]],
        });
      },
    });
  }

  return (
    <Form.Root
      onSubmit={(event) => {
        if (password === "") {
          event.preventDefault();
          return;
        }
        signIn();
        event.preventDefault();
      }}
      className="h-screen w-full"
    >
      <div className="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
        <div className="flex w-96 flex-col items-center justify-center gap-2 rounded-lg bg-white p-8 shadow-xl border border-slate-200">
          <AxieStudioLogo
            title="Axie Studio logo"
            className="mb-6 h-16 w-16"
          />
          <span className="mb-8 text-3xl font-bold text-slate-800">
            Axie Studio
          </span>
          <span className="mb-6 text-lg text-slate-600">
            Sign in to continue
          </span>
          <div className="mb-4 w-full">
            <Form.Field name="username">
              <Form.Label className="data-[invalid]:label-invalid text-sm font-medium text-slate-700">
                Email <span className="font-medium text-red-500">*</span>
              </Form.Label>

              <Form.Control asChild>
                <Input
                  type="email"
                  onChange={({ target: { value } }) => {
                    handleInput({ target: { name: "username", value } });
                  }}
                  value={username}
                  className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  required
                  placeholder="stefan@axiestudio.se"
                />
              </Form.Control>

              <Form.Message match="valueMissing" className="field-invalid text-red-500 text-sm mt-1">
                Please enter your email
              </Form.Message>
            </Form.Field>
          </div>
          <div className="mb-6 w-full">
            <Form.Field name="password">
              <Form.Label className="data-[invalid]:label-invalid text-sm font-medium text-slate-700">
                Password <span className="font-medium text-red-500">*</span>
              </Form.Label>

              <InputComponent
                onChange={(value) => {
                  handleInput({ target: { name: "password", value } });
                }}
                value={password}
                isForm
                password={true}
                required
                placeholder="Enter your password"
                className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />

              <Form.Message className="field-invalid text-red-500 text-sm mt-1" match="valueMissing">
                Please enter your password
              </Form.Message>
            </Form.Field>
          </div>
          <div className="w-full">
            <Form.Submit asChild>
              <Button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200" type="submit">
                Sign In
              </Button>
            </Form.Submit>
          </div>
          <div className="mt-4 w-full">
            <CustomLink to="/signup">
              <Button className="w-full bg-white hover:bg-slate-50 text-slate-700 font-medium py-2 px-4 rounded-md border border-slate-300 transition-colors duration-200" variant="outline" type="button">
                Don't have an account? <span className="font-semibold">Sign Up</span>
              </Button>
            </CustomLink>
          </div>
          <div className="mt-6 text-center">
            <p className="text-sm text-slate-500">
              Welcome to Axie Studio
            </p>
          </div>
        </div>
      </div>
    </Form.Root>
  );
}
