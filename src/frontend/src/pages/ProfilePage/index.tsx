import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { User, Settings, CreditCard, BarChart3, Shield } from "lucide-react";
import useAlertStore from "@/stores/alertStore";

interface ProfileData {
  id: string;
  username: string;
  tier: string;
  account_number: number;
  is_active: boolean;
  created_at: string;
  last_login_at?: string;
  plan_info: {
    tier: string;
    usage: {
      workflows: { current: number; limit: number; percentage: number };
      api_calls: { current: number; limit: number; percentage: number };
      storage: { current_gb: number; limit_gb: number; percentage: number };
    };
    limits: {
      max_workflows: number;
      max_api_calls_per_month: number;
      max_storage_gb: number;
      support_level: string;
      price_per_month: number;
    };
  };
}

const TIER_COLORS = {
  starter: "bg-blue-100 text-blue-800",
  professional: "bg-purple-100 text-purple-800",
  enterprise: "bg-gold-100 text-gold-800"
};

const TIER_NAMES = {
  starter: "Starter",
  professional: "Professional", 
  enterprise: "Enterprise"
};

export default function ProfilePage() {
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editForm, setEditForm] = useState({ username: "", password: "", confirmPassword: "" });
  const [updating, setUpdating] = useState(false);
  
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const setErrorData = useAlertStore((state) => state.setErrorData);

  // Mock data - replace with actual API calls
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      const mockProfile: ProfileData = {
        id: "user-123",
        username: "starter001@axiestudio.se",
        tier: "starter",
        account_number: 1001,
        is_active: true,
        created_at: "2025-01-15T10:00:00Z",
        last_login_at: "2025-01-24T08:30:00Z",
        plan_info: {
          tier: "starter",
          usage: {
            workflows: { current: 12, limit: 50, percentage: 24 },
            api_calls: { current: 1250, limit: 5000, percentage: 25 },
            storage: { current_gb: 0.3, limit_gb: 1, percentage: 30 }
          },
          limits: {
            max_workflows: 50,
            max_api_calls_per_month: 5000,
            max_storage_gb: 1,
            support_level: "Email",
            price_per_month: 29
          }
        }
      };

      setProfile(mockProfile);
      setEditForm({ username: mockProfile.username, password: "", confirmPassword: "" });
      setLoading(false);
    }, 1000);
  }, []);

  // TODO: Replace mock data with real API calls
  // useEffect(() => {
  //   const fetchProfileData = async () => {
  //     try {
  //       const profileResponse = await fetch('/api/v1/profile', {
  //         headers: {
  //           'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
  //           'Content-Type': 'application/json'
  //         }
  //       });
  //
  //       if (!profileResponse.ok) throw new Error('Failed to fetch profile');
  //       const profileData = await profileResponse.json();
  //
  //       const usageResponse = await fetch('/api/v1/profile/usage', {
  //         headers: {
  //           'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
  //           'Content-Type': 'application/json'
  //         }
  //       });
  //
  //       if (!usageResponse.ok) throw new Error('Failed to fetch usage data');
  //       const usageData = await usageResponse.json();
  //
  //       const combinedProfile: ProfileData = {
  //         id: profileData.id,
  //         username: profileData.username,
  //         tier: profileData.tier,
  //         account_number: profileData.account_number,
  //         is_active: profileData.is_active,
  //         created_at: profileData.created_at,
  //         last_login_at: profileData.last_login_at,
  //         plan_info: usageData
  //       };
  //
  //       setProfile(combinedProfile);
  //       setEditForm({ username: combinedProfile.username, password: "", confirmPassword: "" });
  //       setLoading(false);
  //     } catch (error) {
  //       console.error('Error fetching profile data:', error);
  //       setLoading(false);
  //     }
  //   };
  //   fetchProfileData();
  // }, []);

  const handleEditProfile = () => {
    setIsEditModalOpen(true);
  };

  const handleSaveProfile = async () => {
    if (editForm.password && editForm.password !== editForm.confirmPassword) {
      setErrorData({
        title: "Password Mismatch",
        list: ["Passwords do not match"]
      });
      return;
    }

    setUpdating(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Update profile
      if (profile) {
        setProfile({
          ...profile,
          username: editForm.username
        });
      }
      
      setSuccessData({
        title: "Profile Updated",
      });
      
      setIsEditModalOpen(false);
    } catch (error) {
      setErrorData({
        title: "Update Failed",
        list: ["Failed to update profile"]
      });
    } finally {
      setUpdating(false);
    }
  };

  const getUsageColor = (percentage: number) => {
    if (percentage >= 90) return "bg-red-500";
    if (percentage >= 75) return "bg-yellow-500";
    return "bg-green-500";
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading profile...</div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg text-red-600">Failed to load profile</div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Profile & Plan</h1>
          <p className="text-gray-600">Manage your account and view usage</p>
        </div>
        <Button onClick={handleEditProfile} className="flex items-center gap-2">
          <Settings className="w-4 h-4" />
          Edit Profile
        </Button>
      </div>

      {/* Profile Info */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="w-5 h-5" />
            Account Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label className="text-sm font-medium text-gray-600">Username</Label>
              <div className="text-lg">{profile.username}</div>
            </div>
            <div>
              <Label className="text-sm font-medium text-gray-600">Account Number</Label>
              <div className="text-lg">#{profile.account_number}</div>
            </div>
            <div>
              <Label className="text-sm font-medium text-gray-600">Plan</Label>
              <div className="flex items-center gap-2">
                <Badge className={TIER_COLORS[profile.tier as keyof typeof TIER_COLORS]}>
                  {TIER_NAMES[profile.tier as keyof typeof TIER_NAMES]}
                </Badge>
                <span className="text-sm text-gray-600">
                  ${profile.plan_info.limits.price_per_month}/month
                </span>
              </div>
            </div>
            <div>
              <Label className="text-sm font-medium text-gray-600">Status</Label>
              <div className="flex items-center gap-2">
                <Badge variant={profile.is_active ? "default" : "secondary"}>
                  {profile.is_active ? "Active" : "Inactive"}
                </Badge>
              </div>
            </div>
            <div>
              <Label className="text-sm font-medium text-gray-600">Member Since</Label>
              <div className="text-lg">
                {new Date(profile.created_at).toLocaleDateString()}
              </div>
            </div>
            <div>
              <Label className="text-sm font-medium text-gray-600">Last Login</Label>
              <div className="text-lg">
                {profile.last_login_at 
                  ? new Date(profile.last_login_at).toLocaleDateString()
                  : "Never"
                }
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Usage Statistics */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5" />
            Usage & Limits
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Workflows */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <Label className="text-sm font-medium">Workflows</Label>
              <span className="text-sm text-gray-600">
                {profile.plan_info.usage.workflows.current} / {
                  profile.plan_info.usage.workflows.limit === -1 
                    ? "Unlimited" 
                    : profile.plan_info.usage.workflows.limit
                }
              </span>
            </div>
            <Progress 
              value={profile.plan_info.usage.workflows.percentage} 
              className="h-2"
            />
          </div>

          {/* API Calls */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <Label className="text-sm font-medium">API Calls (This Month)</Label>
              <span className="text-sm text-gray-600">
                {profile.plan_info.usage.api_calls.current.toLocaleString()} / {profile.plan_info.usage.api_calls.limit.toLocaleString()}
              </span>
            </div>
            <Progress 
              value={profile.plan_info.usage.api_calls.percentage} 
              className="h-2"
            />
          </div>

          {/* Storage */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <Label className="text-sm font-medium">Storage</Label>
              <span className="text-sm text-gray-600">
                {profile.plan_info.usage.storage.current_gb.toFixed(2)}GB / {profile.plan_info.usage.storage.limit_gb}GB
              </span>
            </div>
            <Progress 
              value={profile.plan_info.usage.storage.percentage} 
              className="h-2"
            />
          </div>
        </CardContent>
      </Card>

      {/* Plan Details */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CreditCard className="w-5 h-5" />
            Plan Details
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label className="text-sm font-medium text-gray-600">Support Level</Label>
              <div className="text-lg flex items-center gap-2">
                <Shield className="w-4 h-4" />
                {profile.plan_info.limits.support_level}
              </div>
            </div>
            <div>
              <Label className="text-sm font-medium text-gray-600">Monthly Price</Label>
              <div className="text-lg font-semibold text-green-600">
                ${profile.plan_info.limits.price_per_month}/month
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Edit Profile Modal */}
      <Dialog open={isEditModalOpen} onOpenChange={setIsEditModalOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Edit Profile</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                value={editForm.username}
                onChange={(e) => setEditForm(prev => ({ ...prev, username: e.target.value }))}
                placeholder="Enter new username"
              />
            </div>
            
            <div>
              <Label htmlFor="password">New Password (optional)</Label>
              <Input
                id="password"
                type="password"
                value={editForm.password}
                onChange={(e) => setEditForm(prev => ({ ...prev, password: e.target.value }))}
                placeholder="Enter new password"
              />
            </div>

            <div>
              <Label htmlFor="confirmPassword">Confirm Password</Label>
              <Input
                id="confirmPassword"
                type="password"
                value={editForm.confirmPassword}
                onChange={(e) => setEditForm(prev => ({ ...prev, confirmPassword: e.target.value }))}
                placeholder="Confirm new password"
              />
            </div>

            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setIsEditModalOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleSaveProfile} disabled={updating}>
                {updating ? "Saving..." : "Save Changes"}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
