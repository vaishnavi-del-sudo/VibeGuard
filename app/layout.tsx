import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata = { title:'VibeGuard — Trust your vibe',description:'Security insights for AI-generated projects. Scan dependencies, secrets, risky code and hidden instructions.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
