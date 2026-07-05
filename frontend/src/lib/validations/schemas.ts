import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

export const registerSchema = z
  .object({
    first_name: z.string().min(2, "First name is required"),
    last_name: z.string().min(2, "Last name is required"),
    email: z.string().email("Invalid email address"),
    phone: z.string().optional(),
    password: z.string().min(8, "Password must be at least 8 characters"),
    password_confirm: z.string(),
  })
  .refine((data) => data.password === data.password_confirm, {
    message: "Passwords don't match",
    path: ["password_confirm"],
  });

export const forgotPasswordSchema = z.object({
  email: z.string().email("Invalid email address"),
});

export const resetPasswordSchema = z
  .object({
    password: z.string().min(8, "Password must be at least 8 characters"),
    password_confirm: z.string(),
  })
  .refine((data) => data.password === data.password_confirm, {
    message: "Passwords don't match",
    path: ["password_confirm"],
  });

export const profileSchema = z.object({
  first_name: z.string().min(2),
  last_name: z.string().min(2),
  email: z.string().email(),
  phone: z.string().optional(),
  bio: z.string().optional(),
});

export const addressSchema = z.object({
  title: z.string().min(2),
  full_name: z.string().min(2),
  phone: z.string().min(10),
  province: z.string().min(2),
  city: z.string().min(2),
  address: z.string().min(10),
  postal_code: z.string().min(5),
  is_default: z.boolean().optional(),
});

export const checkoutSchema = z.object({
  address_id: z.number(),
  payment_method: z.enum(["online", "wallet", "cod"]),
  shipping_method: z.string(),
  coupon_code: z.string().optional(),
  notes: z.string().optional(),
});

export const contactSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  subject: z.string().min(5),
  message: z.string().min(20),
});

export const reviewSchema = z.object({
  rating: z.number().min(1).max(5),
  title: z.string().min(3),
  comment: z.string().min(10),
});

export const ticketSchema = z.object({
  subject: z.string().min(5),
  category: z.string(),
  message: z.string().min(20),
  priority: z.enum(["low", "medium", "high"]),
});

export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;
export type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>;
export type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>;
export type ProfileFormData = z.infer<typeof profileSchema>;
export type AddressFormData = z.infer<typeof addressSchema>;
export type CheckoutFormData = z.infer<typeof checkoutSchema>;
export type ContactFormData = z.infer<typeof contactSchema>;
export type ReviewFormData = z.infer<typeof reviewSchema>;
export type TicketFormData = z.infer<typeof ticketSchema>;
