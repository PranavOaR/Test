import { Users, Calendar } from 'lucide-react';
import { motion } from 'framer-motion';

interface Team {
    team_id: number;
    team_name: string;
    coach_name: string;
    foundation_year: number;
}

interface TeamCardProps {
    team: Team;
}

export default function TeamCard({ team }: TeamCardProps) {
    return (
        <motion.div
            whileHover={{ y: -5 }}
            className="bg-white rounded-xl shadow-md overflow-hidden border border-slate-100 hover:shadow-xl transition-all"
        >
            <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                    <div className="h-12 w-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-xl">
                        {team.team_name.charAt(0)}
                    </div>
                    <span className="text-xs font-semibold bg-slate-100 text-slate-600 px-2 py-1 rounded-full">
                        ID: {team.team_id}
                    </span>
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">{team.team_name}</h3>
                <div className="space-y-2 text-sm text-slate-600">
                    <div className="flex items-center space-x-2">
                        <Users className="w-4 h-4" />
                        <span>Coach: {team.coach_name}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                        <Calendar className="w-4 h-4" />
                        <span>Est: {team.foundation_year}</span>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
