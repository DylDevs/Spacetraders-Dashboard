'use client';
import dynamic from 'next/dynamic';

const SystemsPage = dynamic(() => import('@/components/systems_renderer'), {
  ssr: false,
});
const WaypointsPage = dynamic(() => import('@/components/waypoints_renderer'), {
  ssr: false,
})

export default function SpaceTradersDashboard() {
    return (<WaypointsPage />);
}