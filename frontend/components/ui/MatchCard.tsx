import { Calendar, MapPin } from 'lucide-react';

interface Match {
    match_id: number;
    team1_name: string;
    team2_name: string;
    match_date: string;
    venue: string;
    status: string;
}

interface MatchCardProps {
    match: Match;
}

export default function MatchCard({ match }: MatchCardProps) {
    const date = new Date(match.match_date).toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });

    return (
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4 hover:shadow-md transition-shadow">
            <div className="flex justify-between items-center mb-4 text-sm text-slate-500">
                <div className="flex items-center space-x-1">
                    <Calendar className="w-4 h-4" />
                    <span>{date}</span>
                </div>
                <div className="flex items-center space-x-1">
                    <MapPin className="w-4 h-4" />
                    <span>{match.venue}</span>
                </div>
            </div>

            <div className="flex items-center justify-between">
                <div className="text-lg font-bold text-slate-900 w-1/3 text-right">
                    {match.team1_name}
                </div>
                <div className="px-4 text-center w-1/3">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${match.status === 'Completed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                        }`}>
                        {match.status}
                    </span>
                </div>
                <div className="text-lg font-bold text-slate-900 w-1/3 text-left">
                    {match.team2_name}
                </div>
            </div>
        </div>
    );
}
