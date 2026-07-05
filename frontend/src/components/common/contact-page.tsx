"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Mail, Phone, MapPin, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { contactSchema, type ContactFormData } from "@/lib/validations/schemas";
import { toast } from "@/hooks/use-toast";
import { getTranslation } from "@/hooks/use-translation";
import type { Locale } from "@/lib/i18n";

export function ContactPageContent({ locale }: { locale: Locale }) {
  const t = getTranslation(locale);
  const form = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
    defaultValues: { name: "", email: "", subject: "", message: "" },
  });

  const onSubmit = async () => {
    toast({ title: "Message sent!", description: "We'll get back to you soon.", variant: "success" });
    form.reset();
  };

  const infoItems = [
    { icon: MapPin, text: t.contact.info.address },
    { icon: Phone, text: t.contact.info.phone },
    { icon: Mail, text: t.contact.info.email },
    { icon: Clock, text: t.contact.info.hours },
  ];

  return (
    <div className="container mx-auto px-4 py-8 md:py-12">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold">{t.contact.title}</h1>
        <p className="text-muted-foreground mt-2">{t.contact.subtitle}</p>
      </div>
      <div className="grid lg:grid-cols-2 gap-8 max-w-5xl mx-auto">
        <div className="glass-card p-6 md:p-8">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField control={form.control} name="name" render={({ field }) => (
                <FormItem><FormLabel>{t.contact.name}</FormLabel><FormControl><Input {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="email" render={({ field }) => (
                <FormItem><FormLabel>{t.contact.email}</FormLabel><FormControl><Input type="email" {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="subject" render={({ field }) => (
                <FormItem><FormLabel>{t.contact.subject}</FormLabel><FormControl><Input {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="message" render={({ field }) => (
                <FormItem><FormLabel>{t.contact.message}</FormLabel><FormControl><textarea className="flex min-h-[120px] w-full rounded-xl border border-input bg-background/50 px-4 py-2 text-sm" {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <Button type="submit" variant="gradient" className="w-full">{t.contact.send}</Button>
            </form>
          </Form>
        </div>
        <div className="space-y-4">
          {infoItems.map(({ icon: Icon, text }) => (
            <div key={text} className="glass-card p-4 flex items-center gap-4">
              <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center shrink-0">
                <Icon className="h-5 w-5 text-blue-600" />
              </div>
              <p className="text-sm">{text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
