'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Users, Search } from 'lucide-react';
import { motion } from 'framer-motion';

interface Player {
    player_id: number;
    name: string;
    position: string;
    team_name: string;
    jersey_number: number;
}

export default function PlayersPage() {
    const [players, setPlayers] = useState<Player[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchPlayers = async () => {
            try {
                const res = await api.get('/players');
                setPlayers(res.data.data);
            } catch (error) {
                console.error('Failed to fetch players:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchPlayers();
    }, []);

    const filteredPlayers = players.filter(player =>
        player.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        player.team_name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="space-y-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 flex items-center">
                        <Users className="mr-3 h-8 w-8 text-blue-600" />
                        Players
                    </h1>
                    <p className="text-slate-500 mt-2">Meet the stars of the league</p>
                </div>
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-5 w-5" />
                    <input
                        type="text"
                        placeholder="Search players or teams..."
                        className="pl-10 pr-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-full md:w-64"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            {loading ? (
                <div className="flex justify-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredPlayers.map((player, index) => (
                        <motion.div
                            key={player.player_id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05 }}
                            className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow"
                        >
                            <div className="flex items-center justify-between mb-4">
                                <div className="h-12 w-12 bg-slate-100 rounded-full flex items-center justify-center text-xl font-bold text-slate-600">
                                    {player.jersey_number}
                                </div>
                                <span className="px-3 py-1 bg-blue-50 text-blue-700 text-sm font-medium rounded-full">
                                    {player.position}
                                </span>
                            </div>
                            <h3 className="text-xl font-bold text-slate-900 mb-1">{player.name}</h3>
                            <p className="text-slate-500 text-sm flex items-center">
                                Playing for <span className="font-semibold text-slate-700 ml-1">{player.team_name}</span>
                            </p>
                        </motion.div>
                    ))}

                    {filteredPlayers.length === 0 && (
                        <div className="col-span-full text-center py-12 text-slate-500">
                            No players found matching your search.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
