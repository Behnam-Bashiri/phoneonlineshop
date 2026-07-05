import {
  Truck,
  Shield,
  Headphones,
  Lock,
  Package,
  Users,
  Award,
  ShoppingBag,
  Star,
  Smartphone,
  Tablet,
  Watch,
  Zap,
  type LucideIcon,
} from "lucide-react";

const iconMap: Record<string, LucideIcon> = {
  Truck,
  Shield,
  Headphones,
  Lock,
  Package,
  Users,
  Award,
  ShoppingBag,
  Star,
  Smartphone,
  Tablet,
  Watch,
  Zap,
};

export function getLucideIcon(name: string): LucideIcon {
  return iconMap[name] || Star;
}
