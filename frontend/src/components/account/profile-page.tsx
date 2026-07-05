"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { profileSchema, type ProfileFormData } from "@/lib/validations/schemas";
import { useAuthStore } from "@/stores/auth-store";
import { toast } from "@/hooks/use-toast";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

export function ProfilePage({ locale }: { locale: Locale }) {
  const { user } = useAuthStore();
  const t = getTranslation(locale);

  const form = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      first_name: user?.first_name || "",
      last_name: user?.last_name || "",
      email: user?.email || "",
      phone: user?.phone || "",
      bio: user?.bio || "",
    },
  });

  const onSubmit = async () => {
    toast({ title: "Profile updated", variant: "success" });
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t.account.profile}</h1>
      <div className="glass-card p-6">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 max-w-lg">
            <div className="grid grid-cols-2 gap-4">
              <FormField control={form.control} name="first_name" render={({ field }) => (
                <FormItem><FormLabel>{t.auth.firstName}</FormLabel><FormControl><Input {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="last_name" render={({ field }) => (
                <FormItem><FormLabel>{t.auth.lastName}</FormLabel><FormControl><Input {...field} /></FormControl><FormMessage /></FormItem>
              )} />
            </div>
            <FormField control={form.control} name="email" render={({ field }) => (
              <FormItem><FormLabel>{t.auth.email}</FormLabel><FormControl><Input type="email" {...field} /></FormControl><FormMessage /></FormItem>
            )} />
            <FormField control={form.control} name="phone" render={({ field }) => (
              <FormItem><FormLabel>{t.auth.phone}</FormLabel><FormControl><Input {...field} /></FormControl><FormMessage /></FormItem>
            )} />
            <Button type="submit" variant="gradient">{t.common.save}</Button>
          </form>
        </Form>
      </div>
    </div>
  );
}
