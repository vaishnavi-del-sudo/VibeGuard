import {getServerSession} from 'next-auth';
import {redirect} from 'next/navigation';
import {authOptions} from '../lib/auth';
import Welcome from '../components/Welcome';
export const dynamic = 'force-dynamic';
export default async function Home(){
 const configured=Boolean(process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET && process.env.NEXTAUTH_SECRET);
 if(configured && await getServerSession(authOptions)) redirect('/dashboard');
 return <Welcome configured={configured}/>;
}
