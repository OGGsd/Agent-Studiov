import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Search, Edit, Trash2, Download, Upload, Plus, Eye } from "lucide-react";

interface Account {
  id: string;
  username: string;
  tier: 'starter' | 'professional' | 'enterprise';
  account_number: number;
  is_active: boolean;
  api_calls_used_this_month: number;
  storage_used_gb: number;
  workflow_count: number;
  created_at: string;
  last_login_at?: string;
}

interface TierLimits {
  max_workflows: number;
  max_api_calls_per_month: number;
  max_storage_gb: number;
  price_per_month: number;
}

const TIER_LIMITS: Record<string, TierLimits> = {
  starter: { max_workflows: 50, max_api_calls_per_month: 5000, max_storage_gb: 1, price_per_month: 29 },
  professional: { max_workflows: 200, max_api_calls_per_month: 25000, max_storage_gb: 10, price_per_month: 79 },
  enterprise: { max_workflows: -1, max_api_calls_per_month: 100000, max_storage_gb: 50, price_per_month: 199 }
};

const TIER_COLORS = {
  starter: "bg-blue-100 text-blue-800",
  professional: "bg-purple-100 text-purple-800", 
  enterprise: "bg-gold-100 text-gold-800"
};

export default function AccountsPage() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [filteredAccounts, setFilteredAccounts] = useState<Account[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [tierFilter, setTierFilter] = useState<string>("all");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  // Mock data - replace with actual API calls
  useEffect(() => {
    // Simulate loading accounts from API
    const mockAccounts: Account[] = [];
    
    // Generate sample data for demonstration
    const tiers = ['starter', 'professional', 'enterprise'];
    for (let i = 1; i <= 30; i++) {
      const tier = tiers[Math.floor(Math.random() * tiers.length)] as 'starter' | 'professional' | 'enterprise';
      mockAccounts.push({
        id: `account-${i}`,
        username: `${tier}${String(i).padStart(3, '0')}@axiestudio.se`,
        tier,
        account_number: 1000 + i,
        is_active: Math.random() > 0.2,
        api_calls_used_this_month: Math.floor(Math.random() * TIER_LIMITS[tier].max_api_calls_per_month * 0.8),
        storage_used_gb: Math.random() * TIER_LIMITS[tier].max_storage_gb * 0.6,
        workflow_count: Math.floor(Math.random() * (TIER_LIMITS[tier].max_workflows === -1 ? 100 : TIER_LIMITS[tier].max_workflows) * 0.4),
        created_at: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
        last_login_at: Math.random() > 0.3 ? new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString() : undefined
      });
    }
    
    setAccounts(mockAccounts);
    setFilteredAccounts(mockAccounts);
    setLoading(false);
  }, []);

  // Filter accounts based on search and filters
  useEffect(() => {
    let filtered = accounts;

    if (searchTerm) {
      filtered = filtered.filter(account => 
        account.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
        account.account_number.toString().includes(searchTerm)
      );
    }

    if (tierFilter !== "all") {
      filtered = filtered.filter(account => account.tier === tierFilter);
    }

    if (statusFilter !== "all") {
      filtered = filtered.filter(account => 
        statusFilter === "active" ? account.is_active : !account.is_active
      );
    }

    setFilteredAccounts(filtered);
  }, [accounts, searchTerm, tierFilter, statusFilter]);

  const handleEditAccount = (account: Account) => {
    setSelectedAccount(account);
    setIsEditModalOpen(true);
  };

  const handleSaveAccount = (updatedAccount: Account) => {
    setAccounts(prev => prev.map(acc => 
      acc.id === updatedAccount.id ? updatedAccount : acc
    ));
    setIsEditModalOpen(false);
    setSelectedAccount(null);
  };

  const handleDeleteAccount = (accountId: string) => {
    if (confirm("Are you sure you want to delete this account?")) {
      setAccounts(prev => prev.filter(acc => acc.id !== accountId));
    }
  };

  const handleExportCSV = () => {
    // Create CSV content
    const headers = ["username", "tier", "account_number", "is_active", "api_calls_used_this_month", "storage_used_gb", "workflow_count"];
    const csvContent = [
      headers.join(","),
      ...filteredAccounts.map(account => [
        account.username,
        account.tier,
        account.account_number,
        account.is_active,
        account.api_calls_used_this_month,
        account.storage_used_gb,
        account.workflow_count
      ].join(","))
    ].join("\n");

    // Download CSV
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `axie_studio_accounts_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const handleImportCSV = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".csv";
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const csv = e.target?.result as string;
          // Parse CSV and update accounts
          console.log("CSV imported:", csv);
          alert("CSV import functionality would be implemented here");
        };
        reader.readAsText(file);
      }
    };
    input.click();
  };

  const handleImportAccounts = async () => {
    if (confirm("This will import all 600 pre-configured accounts. Continue?")) {
      try {
        // Call API to import accounts
        alert("Account import functionality would be implemented here");
      } catch (error) {
        alert("Failed to import accounts");
      }
    }
  };

  const getUsagePercentage = (used: number, max: number) => {
    if (max === -1) return 0; // Unlimited
    return Math.min((used / max) * 100, 100);
  };

  const getTierStats = () => {
    const stats = {
      total: accounts.length,
      active: accounts.filter(acc => acc.is_active).length,
      starter: accounts.filter(acc => acc.tier === 'starter').length,
      professional: accounts.filter(acc => acc.tier === 'professional').length,
      enterprise: accounts.filter(acc => acc.tier === 'enterprise').length,
      potential_revenue: accounts.reduce((sum, acc) => sum + TIER_LIMITS[acc.tier].price_per_month, 0)
    };
    return stats;
  };

  const stats = getTierStats();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading accounts...</div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Account Management</h1>
          <p className="text-gray-600">Manage your 600 pre-configured Axie Studio accounts</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="flex items-center gap-2" onClick={handleExportCSV}>
            <Download className="w-4 h-4" />
            Export CSV
          </Button>
          <Button variant="outline" className="flex items-center gap-2" onClick={handleImportCSV}>
            <Upload className="w-4 h-4" />
            Import CSV
          </Button>
          <Button variant="primary" className="flex items-center gap-2" onClick={handleImportAccounts}>
            <Plus className="w-4 h-4" />
            Import All Accounts
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total Accounts</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
            <p className="text-xs text-gray-600">{stats.active} active</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Potential Revenue</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${stats.potential_revenue.toLocaleString()}</div>
            <p className="text-xs text-gray-600">per month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Tier Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-1">
              <div className="flex justify-between text-sm">
                <span>Starter:</span>
                <span>{stats.starter}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Professional:</span>
                <span>{stats.professional}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Enterprise:</span>
                <span>{stats.enterprise}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Active Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{Math.round((stats.active / stats.total) * 100)}%</div>
            <p className="text-xs text-gray-600">{stats.active} of {stats.total}</p>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-4 items-center">
        <div className="relative flex-1 min-w-64">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Search by username or account number..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        
        <Select value={tierFilter} onValueChange={setTierFilter}>
          <SelectTrigger className="w-40">
            <SelectValue placeholder="Filter by tier" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Tiers</SelectItem>
            <SelectItem value="starter">Starter</SelectItem>
            <SelectItem value="professional">Professional</SelectItem>
            <SelectItem value="enterprise">Enterprise</SelectItem>
          </SelectContent>
        </Select>

        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-40">
            <SelectValue placeholder="Filter by status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="inactive">Inactive</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Accounts Table */}
      <Card>
        <CardHeader>
          <CardTitle>Accounts ({filteredAccounts.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Account</TableHead>
                <TableHead>Tier</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Usage</TableHead>
                <TableHead>Last Login</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredAccounts.map((account) => (
                <TableRow key={account.id}>
                  <TableCell>
                    <div>
                      <div className="font-medium">{account.username}</div>
                      <div className="text-sm text-gray-600">#{account.account_number}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge className={TIER_COLORS[account.tier]}>
                      {account.tier.charAt(0).toUpperCase() + account.tier.slice(1)}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant={account.is_active ? "default" : "secondary"}>
                      {account.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="text-sm">
                        API: {account.api_calls_used_this_month.toLocaleString()}/{TIER_LIMITS[account.tier].max_api_calls_per_month.toLocaleString()}
                      </div>
                      <div className="text-sm">
                        Storage: {account.storage_used_gb.toFixed(1)}GB/{TIER_LIMITS[account.tier].max_storage_gb}GB
                      </div>
                      <div className="text-sm">
                        Workflows: {account.workflow_count}/{TIER_LIMITS[account.tier].max_workflows === -1 ? '∞' : TIER_LIMITS[account.tier].max_workflows}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    {account.last_login_at ? (
                      <div className="text-sm">
                        {new Date(account.last_login_at).toLocaleDateString()}
                      </div>
                    ) : (
                      <div className="text-sm text-gray-400">Never</div>
                    )}
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleEditAccount(account)}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDeleteAccount(account.id)}
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Edit Account Modal */}
      {selectedAccount && (
        <EditAccountModal
          account={selectedAccount}
          isOpen={isEditModalOpen}
          onClose={() => setIsEditModalOpen(false)}
          onSave={handleSaveAccount}
        />
      )}
    </div>
  );
}

// Edit Account Modal Component
interface EditAccountModalProps {
  account: Account;
  isOpen: boolean;
  onClose: () => void;
  onSave: (account: Account) => void;
}

function EditAccountModal({ account, isOpen, onClose, onSave }: EditAccountModalProps) {
  const [editedAccount, setEditedAccount] = useState<Account>(account);

  const handleSave = () => {
    onSave(editedAccount);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Edit Account</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium">Username</label>
            <Input
              value={editedAccount.username}
              onChange={(e) => setEditedAccount(prev => ({ ...prev, username: e.target.value }))}
            />
          </div>
          
          <div>
            <label className="text-sm font-medium">Tier</label>
            <Select
              value={editedAccount.tier}
              onValueChange={(value) => setEditedAccount(prev => ({ ...prev, tier: value as any }))}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="starter">Starter ($29/month)</SelectItem>
                <SelectItem value="professional">Professional ($79/month)</SelectItem>
                <SelectItem value="enterprise">Enterprise ($199/month)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="text-sm font-medium">Status</label>
            <Select
              value={editedAccount.is_active ? "active" : "inactive"}
              onValueChange={(value) => setEditedAccount(prev => ({ ...prev, is_active: value === "active" }))}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="inactive">Inactive</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={onClose}>Cancel</Button>
            <Button onClick={handleSave}>Save Changes</Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
