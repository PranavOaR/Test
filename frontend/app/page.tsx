'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Trophy, Users, Calendar, BarChart3 } from 'lucide-react';

export default function Home() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
    },
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center">
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="space-y-8"
      >
        <motion.div variants={itemVariants} className="space-y-4">
          <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900 tracking-tight">
            Football League <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-500 to-orange-600">
              Management System
            </span>
          </h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Manage tournaments, teams, players, and matches with ease.
            Track real-time scores and leaderboards in a modern interface.
          </p>
        </motion.div>

        <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-12">
          {[
            { icon: Trophy, label: 'Tournaments', href: '/tournaments', color: 'bg-blue-100 text-blue-600' },
            { icon: Users, label: 'Teams & Players', href: '/teams', color: 'bg-green-100 text-green-600' },
            { icon: Calendar, label: 'Match Schedule', href: '/matches', color: 'bg-purple-100 text-purple-600' },
            { icon: BarChart3, label: 'Leaderboard', href: '/leaderboard', color: 'bg-orange-100 text-orange-600' },
          ].map((item, index) => (
            <Link key={index} href={item.href}>
              <div className="p-6 bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow cursor-pointer border border-slate-100 group">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 ${item.color} group-hover:scale-110 transition-transform`}>
                  <item.icon className="w-6 h-6" />
                </div>
                <h3 className="font-semibold text-slate-900">{item.label}</h3>
              </div>
            </Link>
          ))}
        </motion.div>


      </motion.div>
    </div>
  );
}
