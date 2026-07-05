"use client";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { SectionHeader } from "@/components/common/section-header";
import type { FAQ } from "@/types";

interface FAQSectionProps {
  faqs: FAQ[];
  title: string;
}

export function FAQSection({ faqs, title }: FAQSectionProps) {
  return (
    <section className="py-12 md:py-16 gradient-bg">
      <div className="container mx-auto px-4 max-w-3xl">
        <SectionHeader title={title} align="center" />
        <Accordion type="single" collapsible className="space-y-3">
          {faqs.map((faq) => (
            <AccordionItem
              key={faq.id}
              value={`faq-${faq.id}`}
              className="glass-card rounded-2xl px-6 border-none"
            >
              <AccordionTrigger className="hover:no-underline">
                {faq.question}
              </AccordionTrigger>
              <AccordionContent className="text-muted-foreground">
                {faq.answer}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </section>
  );
}
