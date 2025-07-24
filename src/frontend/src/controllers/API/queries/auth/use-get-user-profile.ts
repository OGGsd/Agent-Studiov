import type { useQueryFunctionType } from "../../../../types/api";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

export interface UserProfileResponse {
  id: string;
  username: string;
  tier: string;
  account_number: number | null;
  is_active: boolean;
  created_at: string;
  last_login_at: string | null;
  plan_info: {
    limits: {
      max_workflows: number;
      max_api_calls_per_month: number;
      max_storage_gb: number;
      support_level: string;
      price_per_month: number;
    };
    usage: {
      workflows_count: number;
      api_calls_used_this_month: number;
      storage_used_gb: number;
    };
  };
}

export const useGetUserProfileQuery: useQueryFunctionType<
  undefined,
  UserProfileResponse
> = (options) => {
  const { query } = UseRequestProcessor();

  const getUserProfileFn = async (): Promise<UserProfileResponse> => {
    const response = await api.get<UserProfileResponse>(`${getURL("PROFILE")}`);
    return response.data;
  };

  const queryResult = query(["useGetUserProfile"], getUserProfileFn, {
    refetchOnWindowFocus: false,
    ...options,
  });

  return queryResult;
};
