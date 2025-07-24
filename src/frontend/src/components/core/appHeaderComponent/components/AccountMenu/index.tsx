import { ForwardedIconComponent } from "@/components/common/genericIconComponent";
import { DOCS_URL } from "@/constants/constants";
import { useLogout, useGetUserProfileQuery } from "@/controllers/API/queries/auth";
import { CustomProfileIcon } from "@/customization/components/custom-profile-icon";
import { ENABLE_DATASTAX_LANGFLOW } from "@/customization/feature-flags";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import useAuthStore from "@/stores/authStore";
import { useDarkStore } from "@/stores/darkStore";
import { cn } from "@/utils/utils";
import {
  HeaderMenu,
  HeaderMenuItemButton,
  HeaderMenuItemLink,
  HeaderMenuItems,
  HeaderMenuToggle,
} from "../HeaderMenu";
import ThemeButtons from "../ThemeButtons";

export const AccountMenu = () => {
  const version = useDarkStore((state) => state.version);
  const latestVersion = useDarkStore((state) => state.latestVersion);
  const navigate = useCustomNavigate();
  const { mutate: mutationLogout } = useLogout();
  const { data: userProfile, isLoading: profileLoading } = useGetUserProfileQuery();

  const { isAdmin, autoLogin } = useAuthStore((state) => ({
    isAdmin: state.isAdmin,
    autoLogin: state.autoLogin,
  }));

  const handleLogout = () => {
    mutationLogout();
  };

  const isLatestVersion = version === latestVersion;

  return (
    <HeaderMenu>
      <HeaderMenuToggle>
        <div
          className="h-6 w-6 rounded-lg focus-visible:outline-0"
          data-testid="user-profile-settings"
        >
          <CustomProfileIcon />
        </div>
      </HeaderMenuToggle>
      <HeaderMenuItems position="right" classNameSize="w-[320px]">
        <div className="divide-y divide-foreground/10">
          {/* Your Plan Section */}
          <div className="px-4 py-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-semibold">Your Plan</span>
            </div>
            {profileLoading ? (
              <div className="text-xs text-muted-foreground">Loading...</div>
            ) : userProfile ? (
              <div className="space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">Tier:</span>
                  <span className="text-xs font-medium capitalize">{userProfile.tier}</span>
                </div>
                {userProfile.account_number && (
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">Account:</span>
                    <span className="text-xs font-medium">#{userProfile.account_number}</span>
                  </div>
                )}
                <div className="flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">Workflows:</span>
                  <span className="text-xs font-medium">
                    {userProfile.plan_info.usage.workflows_count}
                    {userProfile.plan_info.limits.max_workflows > 0
                      ? ` / ${userProfile.plan_info.limits.max_workflows}`
                      : " / Unlimited"}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">API Calls:</span>
                  <span className="text-xs font-medium">
                    {userProfile.plan_info.usage.api_calls_used_this_month.toLocaleString()} / {userProfile.plan_info.limits.max_api_calls_per_month.toLocaleString()}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">Storage:</span>
                  <span className="text-xs font-medium">
                    {userProfile.plan_info.usage.storage_used_gb.toFixed(2)} GB / {userProfile.plan_info.limits.max_storage_gb} GB
                  </span>
                </div>
              </div>
            ) : (
              <div className="text-xs text-muted-foreground">Unable to load plan info</div>
            )}
          </div>

          <div>
            <div className="h-[44px] items-center px-4 pt-3">
              <div className="flex items-center justify-between">
                <span
                  data-testid="menu_version_button"
                  id="menu_version_button"
                  className="text-sm"
                >
                  Version
                </span>
                <div
                  className={cn(
                    "float-right text-xs",
                    isLatestVersion && "text-accent-emerald-foreground",
                    !isLatestVersion && "text-accent-amber-foreground",
                  )}
                >
                  {version}{" "}
                  {isLatestVersion ? "(latest)" : "(update available)"}
                </div>
              </div>
            </div>
          </div>

          <div>
            <HeaderMenuItemButton
              onClick={() => {
                navigate("/settings");
              }}
            >
              <span
                data-testid="menu_settings_button"
                id="menu_settings_button"
              >
                Settings
              </span>
            </HeaderMenuItemButton>

            {isAdmin && !autoLogin && (
              <div>
                <HeaderMenuItemButton
                  onClick={() => {
                    navigate("/admin");
                  }}
                >
                  <span
                    data-testid="menu_admin_page_button"
                    id="menu_admin_page_button"
                  >
                    Admin Page
                  </span>
                </HeaderMenuItemButton>
              </div>
            )}
          </div>

          <div className="flex items-center justify-between px-4 py-[6.5px] text-sm">
            <span className="">Theme</span>
            <div className="relative top-[1px] float-right">
              <ThemeButtons />
            </div>
          </div>

          <div>
            <HeaderMenuItemButton onClick={handleLogout} icon="log-out">
              Logout
            </HeaderMenuItemButton>
          </div>
        </div>
      </HeaderMenuItems>
    </HeaderMenu>
  );
};
