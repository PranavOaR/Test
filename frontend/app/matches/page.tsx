'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import MatchCard from '@/components/ui/MatchCard';

interface Match {
    match_id: number;
    team1_name: string;
    team2_name: string;
    match_date: string;
    venue: string;
    status: string;
}

export default function MatchesPage() {
    const [matches, setMatches] = useState<Match[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMatches = async () => {
            try {
                const res = await api.get('/matches');
                setMatches(res.data.data);
            } catch (error) {
                console.error('Failed to fetch matches', error);
            } finally {
                setLoading(false);
            }
        };

        fetchMatches();
    }, []);

    if (loading) {
        return <div className="text-center py-20">Loading matches...</div>;
    }

    return (
        <div className="space-y-8">
            <div className="text-center space-y-4">
                <h1 className="text-4xl font-bold text-slate-900">Match Schedule</h1>
                <p className="text-slate-600 max-w-2xl mx-auto">
                    Upcoming fixtures and past results.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
                {matches.map((match) => (
                    <MatchCard key={match.match_id} match={match} />
                ))}
            </div>
        </div>
    );
}
