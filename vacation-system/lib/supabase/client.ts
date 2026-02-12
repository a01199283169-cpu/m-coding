import { createBrowserClient } from '@supabase/ssr';
import type { SupabaseClient } from '@supabase/supabase-js';

let client: SupabaseClient | null = null;

export function createClient() {
  // Return cached client if exists
  if (client) return client;

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  // During build/SSR without env vars, return a placeholder
  // The actual client will be created on the client-side
  if (!supabaseUrl || !supabaseAnonKey) {
    if (typeof window === 'undefined') {
      // Server-side during build - return a minimal mock
      return {
        auth: {
          getUser: async () => ({ data: { user: null }, error: null }),
          signInWithPassword: async () => ({ data: null, error: { message: 'Not configured' } }),
          signUp: async () => ({ data: null, error: { message: 'Not configured' } }),
          signOut: async () => ({ error: null }),
        },
        from: () => ({
          select: () => ({ eq: () => ({ single: async () => ({ data: null, error: null }), order: async () => ({ data: [], error: null }) }), order: async () => ({ data: [], error: null }) }),
          insert: async () => ({ data: null, error: null }),
          update: () => ({ eq: async () => ({ data: null, error: null }) }),
          delete: () => ({ eq: async () => ({ data: null, error: null }) }),
        }),
      } as unknown as SupabaseClient;
    }
    throw new Error(
      'Missing Supabase environment variables. Please check your .env.local file.'
    );
  }

  client = createBrowserClient(supabaseUrl, supabaseAnonKey);
  return client;
}
