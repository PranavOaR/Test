'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Trophy } from 'lucide-react';

interface LeaderboardEntry {
    team_id: number;
    team_name: string;
    matches_played: number;
    wins: number;
    draws: number;
    losses: number;
    goals_for: number;
    total_points: number;
}

export default function LeaderboardPage() {
    const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchLeaderboard = async () => {
            try {
                const res = await api.get('/leaderboard');
                setLeaderboard(res.data.data);
            } catch (error) {
                console.error('Failed to fetch leaderboard', error);
            } finally {
                setLoading(false);
            }
        };

        fetchLeaderboard();
    }, []);

    if (loading) {
        return <div className="text-center py-20">Loading leaderboard...</div>;
    }

    return (
        <div className="space-y-8">
            <div className="text-center space-y-4">
                <h1 className="text-4xl font-bold text-slate-900">Leaderboard</h1>
                <p className="text-slate-600 max-w-2xl mx-auto">
                    Current standings in the league.
                </p>
            </div>

            <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-slate-200">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-slate-50 border-b border-slate-200">
                            <tr>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Pos</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Team</th>
                                <th className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">MP</th>
                                <th className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">W</th>
                                <th className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">D</th>
                                <th className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">L</th>
                                <th className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">GF</th>
                                <th className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Pts</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-200">
                            {leaderboard.map((entry, index) => (
                                <tr key={entry.team_id} className="hover:bg-slate-50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                                        {index + 1}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="flex items-center">
                                            <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold mr-3">
                                                {entry.team_name.charAt(0)}
                                            </div>
                                            <span className="text-sm font-medium text-slate-900">{entry.team_name}</span>
                                            {index === 0 && <Trophy className="w-4 h-4 text-yellow-500 ml-2" />}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-center text-slate-500">{entry.matches_played}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-center text-green-600 font-medium">{entry.wins}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-center text-slate-500">{entry.draws}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-center text-red-600">{entry.losses}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-center text-slate-500">{entry.goals_for}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-center font-bold text-slate-900">{entry.total_points}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
