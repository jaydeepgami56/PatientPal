import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Stethoscope, Brain, Settings, BarChart3, ArrowRight, Sparkles,
  Shield, CheckCircle, Users, Award, TrendingUp
} from 'lucide-react';
import { Button, Card, CardBody, Badge } from '../components/ui';

/**
 * Professional Healthcare Home Page
 * - Clean, trustworthy design
 * - Light backgrounds with blue/teal accents
 * - Excellent accessibility and readability
 * - Mobile-first responsive
 */

export default function Home() {
  const [reduceMotion, setReduceMotion] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined' && window.matchMedia) {
      const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
      setReduceMotion(mq.matches);
      const handler = (e) => setReduceMotion(e.matches);
      if (mq.addEventListener) mq.addEventListener('change', handler);
      else mq.addListener(handler);
      return () => {
        if (mq.removeEventListener) mq.removeEventListener('change', handler);
        else mq.removeListener(handler);
      };
    }
  }, []);

  const features = [
    {
      title: 'Triage Agent',
      description: 'AI-powered pre-visit assessment using Australian ATS standards. Fast, accurate, and clinically validated.',
      icon: Stethoscope,
      link: '/triage',
      color: 'blue',
      stats: '< 2 min',
      tag: 'Fast Response',
    },
    {
      title: 'Lead Agent',
      description: 'Intelligent orchestration system that routes queries to specialized medical AI agents seamlessly.',
      icon: Brain,
      link: '/lead-agent',
      color: 'teal',
      stats: '5+ Specialists',
      tag: 'AI Orchestration',
    },
    {
      title: 'Agent Configuration',
      description: 'Manage and customize specialist agents including MedGemma, TxGemma, Dermatology, and more.',
      icon: Settings,
      link: '/config',
      color: 'blue',
      stats: 'Customizable',
      tag: 'Full Control',
    },
    {
      title: 'Results Dashboard',
      description: 'Real-time analytics and comprehensive insights from all agent interactions and outcomes.',
      icon: BarChart3,
      link: '/dashboard',
      color: 'teal',
      stats: 'Real-time',
      tag: 'Analytics',
    },
  ];

  const trustIndicators = [
    { icon: Shield, label: 'HIPAA Compliant', color: 'text-green-600' },
    { icon: Award, label: 'Clinically Validated', color: 'text-blue-600' },
    { icon: Users, label: 'Trusted by 500+ Providers', color: 'text-teal-600' },
    { icon: TrendingUp, label: '99.9% Uptime SLA', color: 'text-purple-600' },
  ];

  const stats = [
    { value: '99.9%', label: 'Uptime' },
    { value: '< 2s', label: 'Response' },
    { value: '5+', label: 'AI Specialists' },
    { value: '24/7', label: 'Available' },
  ];

  const subtleFade = reduceMotion
    ? {}
    : {
        initial: { opacity: 0, y: 10 },
        animate: { opacity: 1, y: 0 },
        transition: { duration: 0.5 },
      };

  return (
    <div className="bg-gradient-to-b from-white via-blue-50/30 to-white">
      {/* HERO SECTION */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <motion.div {...subtleFade} className="space-y-6">
            <Badge variant="primary" size="md" icon={<Sparkles className="w-4 h-4" />}>
              NEXT-GENERATION AI PLATFORM
            </Badge>

            <h1 className="text-hero text-gray-900">
              Intelligent Healthcare,{' '}
              <span className="gradient-text">Delivered</span>
            </h1>

            <p className="text-body-large text-gray-600 max-w-2xl">
              Enterprise-ready multi-agent AI platform for faster triage, specialist consultation,
              and actionable clinical insights. Built for modern healthcare teams.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Link to="/triage">
                <Button
                  variant="primary"
                  size="lg"
                  icon={<ArrowRight className="w-5 h-5" />}
                >
                  Start Triage Assessment
                </Button>
              </Link>

              <Link to="/dashboard">
                <Button variant="outline" size="lg">
                  View Dashboard
                </Button>
              </Link>
            </div>

            <p className="text-sm text-gray-500 pt-2">
              <CheckCircle className="w-4 h-4 inline mr-1 text-green-600" />
              No credit card required · 14-day free trial
            </p>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-8">
              {stats.map((stat, idx) => (
                <div key={idx} className="text-center p-4 bg-white rounded-lg border border-gray-200 shadow-sm">
                  <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                  <div className="text-xs text-gray-600 uppercase tracking-wide mt-1">{stat.label}</div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Hero Visual */}
          <div className="hidden lg:flex items-center justify-center">
            <div className="relative w-full max-w-md">
              <div className="aspect-square bg-gradient-to-br from-blue-100 to-teal-100 rounded-3xl shadow-2xl p-12 flex items-center justify-center">
                <div className="text-center space-y-4">
                  <div className="w-24 h-24 mx-auto bg-gradient-to-br from-blue-600 to-teal-600 rounded-2xl shadow-xl flex items-center justify-center">
                    <Brain className="w-14 h-14 text-white" strokeWidth={2} />
                  </div>
                  <div className="text-xl font-bold text-gray-900">AI-Powered Intelligence</div>
                  <div className="text-sm text-gray-600">Multi-agent healthcare platform</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* TRUST INDICATORS */}
      <section className="bg-white border-y border-gray-200 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {trustIndicators.map((item, idx) => {
              const Icon = item.icon;
              return (
                <div key={idx} className="text-center">
                  <Icon className={`w-10 h-10 mx-auto ${item.color}`} strokeWidth={2} />
                  <div className="mt-3 text-sm font-medium text-gray-900">{item.label}</div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
        <div className="text-center mb-12">
          <Badge variant="primary" size="lg" icon={<Sparkles className="w-4 h-4" />}>
            CORE CAPABILITIES
          </Badge>
          <h2 className="text-headline mt-6 text-gray-900">Powerful AI Features for Healthcare</h2>
          <p className="text-body text-gray-600 mt-4 max-w-2xl mx-auto">
            Built for clinicians and health systems. Practical, auditable, and extensible AI solutions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((f, i) => {
            const Icon = f.icon;
            const colorClasses = f.color === 'blue'
              ? 'from-blue-600 to-blue-700'
              : 'from-teal-600 to-teal-700';

            return (
              <Link to={f.link} key={i} className="group block">
                <Card className="h-full">
                  <CardBody className="space-y-4">
                    <div className="flex items-start justify-between">
                      <div className={`p-4 rounded-xl bg-gradient-to-br ${colorClasses} shadow-lg`}>
                        <Icon className="w-8 h-8 text-white" strokeWidth={2} />
                      </div>
                      <Badge variant="default" size="sm">{f.tag}</Badge>
                    </div>

                    <div>
                      <h3 className="text-xl font-bold text-gray-900">{f.title}</h3>
                      <p className="text-gray-600 mt-2 leading-relaxed">{f.description}</p>
                    </div>

                    <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                      <div className="text-sm font-bold text-blue-600">{f.stats}</div>
                      <div className="text-sm text-blue-600 font-medium flex items-center gap-2 group-hover:gap-3 transition-all">
                        <span>Explore</span>
                        <ArrowRight className="w-4 h-4" />
                      </div>
                    </div>
                  </CardBody>
                </Card>
              </Link>
            );
          })}
        </div>
      </section>

      {/* CTA SECTION */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16 sm:pb-24">
        <div className="bg-gradient-to-br from-blue-600 to-teal-600 rounded-3xl shadow-2xl p-8 sm:p-12 text-center text-white">
          <h3 className="text-3xl sm:text-4xl font-bold">Ready to Transform Your Workflow?</h3>
          <p className="text-blue-100 mt-4 text-lg max-w-2xl mx-auto">
            Start a pilot program with our platform or schedule a personalized demo for your organization.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row justify-center gap-4">
            <Link to="/triage">
              <Button
                variant="secondary"
                size="lg"
                className="bg-white text-blue-600 hover:bg-gray-100"
                icon={<ArrowRight className="w-5 h-5" />}
              >
                Get Started Free
              </Button>
            </Link>
            <Button
              variant="outline"
              size="lg"
              className="border-2 border-white text-white hover:bg-white/10"
            >
              Schedule Demo
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
