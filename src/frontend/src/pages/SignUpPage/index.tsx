import { useEffect } from "react";
import AxieStudioLogo from "@/assets/AxieStudioLogo.svg?react";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import { Button } from "../../components/ui/button";

export default function SignUp(): JSX.Element {
  const navigate = useCustomNavigate();

  // Redirect to login page immediately - signup disabled for commercial accounts
  useEffect(() => {
    navigate("/login");
  }, [navigate]);

  // Show a message while redirecting
  return (
    <div className="flex h-screen w-full flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="flex w-96 flex-col items-center justify-center gap-4 rounded-lg bg-white p-8 shadow-xl border border-slate-200">
        <AxieStudioLogo
          title="Axie Studio logo"
          className="h-16 w-16"
        />
        <span className="text-2xl font-bold text-slate-800">
          Axie Studio
        </span>
        <div className="text-center">
          <p className="text-lg text-slate-600 mb-4">
            Account Registration Disabled
          </p>
          <p className="text-sm text-slate-500 mb-6">
            We use pre-configured commercial accounts only. Contact sales for access.
          </p>
          <Button
            onClick={() => navigate("/login")}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white"
          >
            Go to Login
          </Button>
        </div>
      </div>
    </div>
  );
}
