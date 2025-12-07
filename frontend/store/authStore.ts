import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
    _id: number;
    username: string;
    role: string;
    token: string;
}

interface AuthState {
    user: User | null;
    login: (user: User) => void;
    logout: () => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            login: (user) => {
                localStorage.setItem('token', user.token);
                set({ user });
            },
            logout: () => {
                localStorage.removeItem('token');
                set({ user: null });
            },
        }),
        {
            name: 'auth-storage',
        }
    )
);
