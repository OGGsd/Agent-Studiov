import * as Form from "@radix-ui/react-form";
import { useContext, useState } from "react";
import AxieStudioLogo from "@/assets/AxieStudioLogo.svg?react";
import { useLoginUser } from "@/controllers/API/queries/auth";
// CustomLink removed - no signup functionality needed
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
      <div className="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-indigo-900 px-4">
        <div className="w-full max-w-md">
          {/* Login Card */}
          <div className="bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 p-8">

            {/* Logo and Header */}
            <div className="text-center mb-8">
              <AxieStudioLogo
                title="Axie Studio logo"
                className="mb-6 h-20 w-20 mx-auto drop-shadow-lg"
              />
              <div className="space-y-2">
                <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600 bg-clip-text text-transparent dark:from-indigo-400 dark:via-purple-400 dark:to-blue-400">
                  Axie Studio
                </h1>
                <p className="text-lg text-slate-600 dark:text-slate-300 font-medium">
                  Professional AI Platform
                </p>
                <p className="text-sm text-slate-500 dark:text-slate-400">
                  Sign in to access your workspace
                </p>
              </div>
            </div>
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
            {/* Login Button */}
            <div className="mt-8 w-full">
              <Form.Submit asChild>
                <Button className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold py-3 px-4 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105" type="submit">
                  Sign In to Axie Studio
                </Button>
              </Form.Submit>
            </div>

            {/* Footer */}
            <div className="mt-6 space-y-4 text-center">
              <div className="border-t border-slate-200 dark:border-slate-600 pt-4">
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Need an account? Contact sales for pre-configured access.
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-500 dark:text-slate-500">
                  Powered by Axie Studio • Professional AI Platform
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Form.Root>
  );
}
