'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/store/authStore';
import FormInput from '@/components/ui/FormInput';
import { UserPlus } from 'lucide-react';
import Link from 'next/link';

const signupSchema = z.object({
    username: z.string().min(3, 'Username must be at least 3 characters'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
    confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"],
});

type SignupFormData = z.infer<typeof signupSchema>;

export default function SignupPage() {
    const router = useRouter();
    const login = useAuthStore((state) => state.login);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<SignupFormData>({
        resolver: zodResolver(signupSchema),
    });

    const onSubmit = async (data: SignupFormData) => {
        setLoading(true);
        setError('');
        try {
            const res = await api.post('/auth/register', {
                username: data.username,
                password: data.password,
            });
            console.log('Signup response:', res.data);
            login(res.data.data);
            router.push('/admin/dashboard');
        } catch (err: any) {
            console.error('Signup Error:', err);
            const errorMessage = err.response?.data?.message || err.message || 'Registration failed';
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-[60vh]">
            <div className="w-full max-w-md bg-white p-8 rounded-xl shadow-lg border border-slate-100">
                <div className="flex flex-col items-center mb-6">
                    <div className="h-12 w-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                        <UserPlus className="w-6 h-6 text-blue-600" />
                    </div>
                    <h1 className="text-2xl font-bold text-slate-900">Create Account</h1>
                    <p className="text-slate-500 text-sm">Sign up to manage the league</p>
                </div>

                {error && (
                    <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm mb-4 text-center">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <FormInput
                        label="Username"
                        type="text"
                        placeholder="Choose a username"
                        error={errors.username?.message}
                        {...register('username')}
                    />
                    <FormInput
                        label="Password"
                        type="password"
                        placeholder="Choose a password"
                        error={errors.password?.message}
                        {...register('password')}
                    />
                    <FormInput
                        label="Confirm Password"
                        type="password"
                        placeholder="Confirm password"
                        error={errors.confirmPassword?.message}
                        {...register('confirmPassword')}
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-slate-900 text-white py-2 rounded-md hover:bg-slate-800 transition-colors disabled:opacity-50"
                    >
                        {loading ? 'Creating Account...' : 'Sign Up'}
                    </button>
                </form>

                <div className="mt-6 text-center text-sm text-slate-600">
                    Already have an account?{' '}
                    <Link href="/login" className="text-blue-600 hover:underline font-medium">
                        Sign In
                    </Link>
                </div>
            </div>
        </div>
    );
}
