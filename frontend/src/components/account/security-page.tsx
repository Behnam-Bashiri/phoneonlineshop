"use client";

import { useState } from "react";
import { Shield, Key, Smartphone } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { toast } from "@/hooks/use-toast";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

export function SecurityPage({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const handleChangePassword = () => {
    toast({ title: "Password updated", variant: "success" });
    setOldPassword("");
    setNewPassword("");
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.security}</h1>
      <div className="space-y-6">
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-4">
            <Key className="h-5 w-5 text-blue-600" />
            <h2 className="font-semibold">Change Password</h2>
          </div>
          <div className="space-y-4 max-w-md">
            <div><Label>Current Password</Label><Input type="password" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)} className="mt-1" /></div>
            <div><Label>New Password</Label><Input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} className="mt-1" /></div>
            <Button variant="gradient" onClick={handleChangePassword}>{t.common.save}</Button>
          </div>
        </div>
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-4">
            <Smartphone className="h-5 w-5 text-blue-600" />
            <h2 className="font-semibold">Two-Factor Authentication</h2>
          </div>
          <p className="text-sm text-muted-foreground mb-4">Add an extra layer of security to your account.</p>
          <Button variant="outline">Enable 2FA</Button>
        </div>
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-4">
            <Shield className="h-5 w-5 text-blue-600" />
            <h2 className="font-semibold">Active Sessions</h2>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between items-center p-3 rounded-xl bg-muted/50">
              <div><p className="text-sm font-medium">Current Session</p><p className="text-xs text-muted-foreground">Chrome · macOS</p></div>
              <span className="text-xs text-green-600 font-medium">Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
