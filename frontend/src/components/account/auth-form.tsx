"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
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
import {
  loginSchema,
  registerSchema,
  forgotPasswordSchema,
  resetPasswordSchema,
  type LoginFormData,
  type RegisterFormData,
  type ForgotPasswordFormData,
  type ResetPasswordFormData,
} from "@/lib/validations/schemas";
import { useAuthStore } from "@/stores/auth-store";
import { getApiErrorMessage } from "@/lib/api/client";
import { toast } from "@/hooks/use-toast";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

interface AuthFormProps {
  locale: Locale;
  mode: "login" | "register" | "forgot" | "reset";
}

export function AuthForm({ locale, mode }: AuthFormProps) {
  const router = useRouter();
  const { login, register, isLoading } = useAuthStore();
  const t = getTranslation(locale);

  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  const titles = {
    login: { title: t.auth.loginTitle, subtitle: t.auth.loginSubtitle },
    register: { title: t.auth.registerTitle, subtitle: t.auth.registerSubtitle },
    forgot: { title: t.auth.forgotTitle, subtitle: t.auth.forgotSubtitle },
    reset: { title: t.auth.resetTitle, subtitle: t.auth.resetSubtitle },
  };

  const onSubmit = async (data: LoginFormData) => {
    try {
      if (mode === "login") {
        await login(data.email, data.password);
        router.push(`/${locale}/account`);
      }
    } catch (error) {
      toast({
        title: "Error",
        description: getApiErrorMessage(error),
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="glass-card p-8">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold">{titles[mode].title}</h1>
            <p className="text-muted-foreground mt-2">{titles[mode].subtitle}</p>
          </div>

          {mode === "login" && (
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>{t.auth.email}</FormLabel>
                      <FormControl>
                        <Input type="email" placeholder="you@example.com" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>{t.auth.password}</FormLabel>
                      <FormControl>
                        <Input type="password" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <div className="flex justify-end">
                  <Link
                    href={`/${locale}/auth/forgot-password`}
                    className="text-sm text-blue-600 hover:underline"
                  >
                    {t.auth.forgotPassword}
                  </Link>
                </div>
                <Button
                  type="submit"
                  variant="gradient"
                  className="w-full"
                  disabled={isLoading}
                >
                  {t.auth.signIn}
                </Button>
              </form>
            </Form>
          )}

          {mode === "register" && <RegisterForm locale={locale} />}
          {mode === "forgot" && <ForgotForm locale={locale} />}
          {mode === "reset" && <ResetForm locale={locale} />}

          {mode === "login" && (
            <p className="text-center text-sm text-muted-foreground mt-6">
              {t.auth.noAccount}{" "}
              <Link
                href={`/${locale}/auth/register`}
                className="text-blue-600 hover:underline font-medium"
              >
                {t.auth.signUp}
              </Link>
            </p>
          )}
          {mode === "register" && (
            <p className="text-center text-sm text-muted-foreground mt-6">
              {t.auth.hasAccount}{" "}
              <Link
                href={`/${locale}/auth/login`}
                className="text-blue-600 hover:underline font-medium"
              >
                {t.auth.signIn}
              </Link>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

function RegisterForm({ locale }: { locale: Locale }) {
  const router = useRouter();
  const { register: registerUser, isLoading } = useAuthStore();
  const t = getTranslation(locale);

  const form = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
      phone: "",
      password: "",
      password_confirm: "",
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    try {
      await registerUser(data);
      router.push(`/${locale}/account`);
    } catch (error) {
      toast({
        title: "Error",
        description: getApiErrorMessage(error),
        variant: "destructive",
      });
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
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
        <FormField control={form.control} name="password" render={({ field }) => (
          <FormItem><FormLabel>{t.auth.password}</FormLabel><FormControl><Input type="password" {...field} /></FormControl><FormMessage /></FormItem>
        )} />
        <FormField control={form.control} name="password_confirm" render={({ field }) => (
          <FormItem><FormLabel>{t.auth.confirmPassword}</FormLabel><FormControl><Input type="password" {...field} /></FormControl><FormMessage /></FormItem>
        )} />
        <Button type="submit" variant="gradient" className="w-full" disabled={isLoading}>
          {t.auth.signUp}
        </Button>
      </form>
    </Form>
  );
}

function ForgotForm({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const form = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: { email: "" },
  });

  const onSubmit = async () => {
    toast({ title: "Email sent", description: "Check your inbox for reset instructions." });
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem><FormLabel>{t.auth.email}</FormLabel><FormControl><Input type="email" {...field} /></FormControl><FormMessage /></FormItem>
        )} />
        <Button type="submit" variant="gradient" className="w-full">{t.auth.sendResetLink}</Button>
      </form>
    </Form>
  );
}

function ResetForm({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const form = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: { password: "", password_confirm: "" },
  });

  const onSubmit = async () => {
    toast({ title: "Password reset", description: "Your password has been updated." });
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField control={form.control} name="password" render={({ field }) => (
          <FormItem><FormLabel>{t.auth.password}</FormLabel><FormControl><Input type="password" {...field} /></FormControl><FormMessage /></FormItem>
        )} />
        <FormField control={form.control} name="password_confirm" render={({ field }) => (
          <FormItem><FormLabel>{t.auth.confirmPassword}</FormLabel><FormControl><Input type="password" {...field} /></FormControl><FormMessage /></FormItem>
        )} />
        <Button type="submit" variant="gradient" className="w-full">{t.auth.resetPassword}</Button>
      </form>
    </Form>
  );
}
