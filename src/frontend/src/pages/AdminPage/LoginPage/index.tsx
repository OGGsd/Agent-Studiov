import { useContext, useState } from "react";
import AxieStudioLogo from "@/assets/AxieStudioLogo.svg?react";
import { useLoginUser } from "@/controllers/API/queries/auth";
import { Button } from "../../../components/ui/button";
import { Input } from "../../../components/ui/input";
import { SIGNIN_ERROR_ALERT } from "../../../constants/alerts_constants";
import { CONTROL_LOGIN_STATE } from "../../../constants/constants";
import { AuthContext } from "../../../contexts/authContext";
import useAlertStore from "../../../stores/alertStore";
import type { LoginType } from "../../../types/api";
import type {
  inputHandlerEventType,
  loginInputStateType,
} from "../../../types/components";

export default function LoginAdminPage() {
  const [inputState, setInputState] =
    useState<loginInputStateType>(CONTROL_LOGIN_STATE);
  const { login } = useContext(AuthContext);

  const { password, username } = inputState;
  const setErrorData = useAlertStore((state) => state.setErrorData);
  function handleInput({
    target: { name, value },
  }: inputHandlerEventType): void {
    setInputState((prev) => ({ ...prev, [name]: value }));
  }

  const { mutate } = useLoginUser();

  function signIn() {
    const user: LoginType = {
      username: username,
      password: password,
    };

    mutate(user, {
      onSuccess: (res) => {
        login(res.access_token, "login", res.refresh_token);
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
    <div className="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br from-slate-50 via-red-50 to-orange-100 dark:from-slate-900 dark:via-red-900/20 dark:to-orange-900/20 px-4">
      <div className="w-full max-w-md">
        {/* Admin Login Card */}
        <div className="bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm rounded-2xl shadow-2xl border border-red-200 dark:border-red-700 p-8">

          {/* Logo and Header */}
          <div className="text-center mb-8">
            <AxieStudioLogo
              title="Axie Studio logo"
              className="mb-6 h-20 w-20 mx-auto drop-shadow-lg"
            />
            <div className="space-y-2">
              <h1 className="text-3xl font-bold bg-gradient-to-r from-red-600 via-orange-600 to-amber-600 bg-clip-text text-transparent dark:from-red-400 dark:via-orange-400 dark:to-amber-400">
                Axie Studio
              </h1>
              <p className="text-lg text-slate-600 dark:text-slate-300 font-medium">
                Administrator Portal
              </p>
              <p className="text-sm text-red-600 dark:text-red-400 font-medium">
                🔐 Admin Access Required
              </p>
            </div>
          </div>

          {/* Admin Login Form */}
          <div className="space-y-6">
            <div className="w-full">
              <label className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2 block">
                Username <span className="text-red-500">*</span>
              </label>
              <Input
                onChange={({ target: { value } }) => {
                  handleInput({ target: { name: "username", value } });
                }}
                className="w-full px-4 py-3 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100"
                placeholder="Enter admin username"
              />
            </div>

            <div className="w-full">
              <label className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2 block">
                Password <span className="text-red-500">*</span>
              </label>
              <Input
                type="password"
                onChange={({ target: { value } }) => {
                  handleInput({ target: { name: "password", value } });
                }}
                className="w-full px-4 py-3 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100"
                placeholder="Enter admin password"
              />
            </div>

            {/* Admin Login Button */}
            <div className="mt-8 w-full">
              <Button
                onClick={() => {
                  signIn();
                }}
                className="w-full bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-semibold py-3 px-4 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
              >
                🔐 Admin Login
              </Button>
            </div>

            {/* Footer */}
            <div className="mt-6 text-center">
              <div className="border-t border-red-200 dark:border-red-600 pt-4">
                <p className="text-xs text-slate-500 dark:text-slate-500">
                  Axie Studio Administrator Portal • Restricted Access
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
