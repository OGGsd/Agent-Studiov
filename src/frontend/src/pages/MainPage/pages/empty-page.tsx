import { ExternalLink } from "lucide-react";
import { FaDiscord, FaGithub } from "react-icons/fa";
import { useShallow } from "zustand/react/shallow";
import logoDarkPng from "@/assets/logo_dark.png";
import logoLightPng from "@/assets/logo_light.png";
import { ForwardedIconComponent } from "@/components/common/genericIconComponent";
import CardsWrapComponent from "@/components/core/cardsWrapComponent";
import { Button } from "@/components/ui/button";
import { DotBackgroundDemo } from "@/components/ui/dot-background";
import { DISCORD_URL, GITHUB_URL } from "@/constants/constants";
import { useGetUserData, useUpdateUser } from "@/controllers/API/queries/auth";
import useAuthStore from "@/stores/authStore";
import { useDarkStore } from "@/stores/darkStore";
import { useFolderStore } from "@/stores/foldersStore";
import { formatNumber } from "@/utils/utils";
import useFileDrop from "../hooks/use-on-file-drop";

const EMPTY_PAGE_TITLE = "Welcome to Axie Studio";
const EMPTY_PAGE_DESCRIPTION = "Build powerful AI agents and workflows with ease";
const EMPTY_PAGE_SUBTITLE = "The professional platform for creating, deploying, and managing AI-powered solutions";
const EMPTY_PAGE_FEATURES = [
  "🤖 AI Agent Builder",
  "🔗 Workflow Automation",
  "📊 Analytics Dashboard",
  "🚀 One-Click Deployment"
];
const EMPTY_PAGE_DRAG_AND_DROP_TEXT =
  "Already have a flow? Drag and drop to upload.";
const EMPTY_PAGE_FOLDER_DESCRIPTION = "Empty folder";
const EMPTY_PAGE_CREATE_FIRST_FLOW_BUTTON_TEXT = "Create Your First Agent";

const EXTERNAL_LINK_ICON_CLASS =
  "absolute right-6 top-[35px] h-4 w-4 shrink-0 translate-x-0 opacity-0 transition-all duration-300 group-hover:translate-x-1 group-hover:opacity-100";

export const EmptyPageCommunity = ({
  setOpenModal,
}: {
  setOpenModal: (open: boolean) => void;
}) => {
  const handleFileDrop = useFileDrop(undefined);
  const folders = useFolderStore((state) => state.folders);
  const userData = useAuthStore(useShallow((state) => state.userData));
  const stars: number | undefined = useDarkStore((state) => state.stars);
  const discordCount: number = useDarkStore((state) => state.discordCount);
  const { mutate: updateUser } = useUpdateUser();
  const { mutate: mutateLoggedUser } = useGetUserData();

  const handleUserTrack = (key: string) => () => {
    const optins = userData?.optins ?? {};
    optins[key] = true;
    updateUser(
      {
        user_id: userData?.id!,
        user: { optins },
      },
      {
        onSuccess: () => {
          mutateLoggedUser({});
        },
      },
    );
  };

  return (
    <DotBackgroundDemo>
      <CardsWrapComponent
        dragMessage={`Drop your flows or components here`}
        onFileDrop={handleFileDrop}
      >
        <div className="m-0 h-full w-full bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-indigo-900 p-0">
          <div className="z-50 flex h-full w-full flex-col items-center justify-center gap-8 px-4">

            {/* Hero Section */}
            <div className="z-50 flex flex-col items-center gap-6 max-w-4xl text-center">

              {/* Logo */}
              <div className="z-50 mb-4">
                <div className="dark:hidden">
                  <img
                    src={logoLightPng}
                    alt="Axie Studio Logo"
                    data-testid="empty_page_logo_light"
                    className="h-20 w-20 mx-auto drop-shadow-lg"
                  />
                </div>
                <div className="hidden dark:block">
                  <img
                    src={logoDarkPng}
                    alt="Axie Studio Logo"
                    data-testid="empty_page_logo_dark"
                    className="h-20 w-20 mx-auto drop-shadow-lg"
                  />
                </div>
              </div>

              {/* Main Title */}
              <div className="space-y-4">
                <h1
                  data-testid="mainpage_title"
                  className="z-50 text-center font-bold text-5xl bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600 bg-clip-text text-transparent dark:from-indigo-400 dark:via-purple-400 dark:to-blue-400"
                >
                  {folders?.length > 1 ? "Empty Folder" : EMPTY_PAGE_TITLE}
                </h1>

                <p
                  data-testid="empty_page_description"
                  className="z-50 text-xl text-slate-600 dark:text-slate-300 font-medium max-w-2xl mx-auto"
                >
                  {folders?.length > 1
                    ? EMPTY_PAGE_FOLDER_DESCRIPTION
                    : EMPTY_PAGE_DESCRIPTION}
                </p>

                {folders?.length <= 1 && (
                  <p className="z-50 text-lg text-slate-500 dark:text-slate-400 max-w-3xl mx-auto">
                    {EMPTY_PAGE_SUBTITLE}
                  </p>
                )}
              </div>

              {/* Features Grid */}
              {folders?.length <= 1 && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 mb-8">
                  {EMPTY_PAGE_FEATURES.map((feature, index) => (
                    <div
                      key={index}
                      className="bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm rounded-lg p-4 border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-md transition-all duration-200"
                    >
                      <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                        {feature}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col gap-6 items-center justify-center max-w-2xl w-full">

              {/* Main CTA */}
              <Button
                onClick={() => setOpenModal(true)}
                className="w-full sm:w-auto bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold py-3 px-8 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
                data-testid="new_project_btn_empty_page"
              >
                <ForwardedIconComponent name="Plus" className="mr-2 h-5 w-5" />
                {EMPTY_PAGE_CREATE_FIRST_FLOW_BUTTON_TEXT}
              </Button>

              {/* Tier-Specific Login Options */}
              {folders?.length <= 1 && (
                <div className="w-full space-y-4">
                  <div className="text-center">
                    <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
                      Access your account by tier:
                    </p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    {/* Starter Login */}
                    <Button
                      variant="outline"
                      onClick={() => window.location.href = '/login'}
                      className="w-full border-green-200 text-green-700 hover:bg-green-50 dark:border-green-700 dark:text-green-400 dark:hover:bg-green-900/20 font-medium py-2 px-4 rounded-lg transition-all duration-200"
                    >
                      <ForwardedIconComponent name="Zap" className="mr-2 h-4 w-4" />
                      Starter Login
                    </Button>

                    {/* Professional Login */}
                    <Button
                      variant="outline"
                      onClick={() => window.location.href = '/login'}
                      className="w-full border-blue-200 text-blue-700 hover:bg-blue-50 dark:border-blue-700 dark:text-blue-400 dark:hover:bg-blue-900/20 font-medium py-2 px-4 rounded-lg transition-all duration-200"
                    >
                      <ForwardedIconComponent name="Star" className="mr-2 h-4 w-4" />
                      Professional Login
                    </Button>

                    {/* Enterprise Login */}
                    <Button
                      variant="outline"
                      onClick={() => window.location.href = '/login'}
                      className="w-full border-purple-200 text-purple-700 hover:bg-purple-50 dark:border-purple-700 dark:text-purple-400 dark:hover:bg-purple-900/20 font-medium py-2 px-4 rounded-lg transition-all duration-200"
                    >
                      <ForwardedIconComponent name="Crown" className="mr-2 h-4 w-4" />
                      Enterprise Login
                    </Button>
                  </div>

                  {/* Admin Access */}
                  <div className="text-center pt-4 border-t border-slate-200 dark:border-slate-700">
                    <Button
                      variant="outline"
                      onClick={() => window.location.href = '/login/admin'}
                      className="border-red-200 text-red-700 hover:bg-red-50 dark:border-red-700 dark:text-red-400 dark:hover:bg-red-900/20 font-medium py-2 px-4 rounded-lg transition-all duration-200"
                    >
                      <ForwardedIconComponent name="Shield" className="mr-2 h-4 w-4" />
                      🔐 Administrator Access
                    </Button>
                  </div>
                </div>
              )}
            </div>

            {/* Drag and Drop Hint */}
            <div className="mt-8 text-center">
              <p
                data-testid="empty_page_drag_and_drop_text"
                className="text-sm text-slate-500 dark:text-slate-400 bg-white/50 dark:bg-slate-800/50 backdrop-blur-sm rounded-full px-4 py-2 border border-slate-200 dark:border-slate-700"
              >
                💡 {EMPTY_PAGE_DRAG_AND_DROP_TEXT}
              </p>
            </div>

            {/* Footer */}
            <div className="mt-auto mb-8 text-center">
              <p className="text-xs text-slate-400 dark:text-slate-500">
                Powered by Axie Studio • Professional AI Workflow Platform
              </p>
            </div>
          </div>
        </div>
      </CardsWrapComponent>
    </DotBackgroundDemo>
  );
};

export default EmptyPageCommunity;
