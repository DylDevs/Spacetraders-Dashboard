'use client';
import dynamic from 'next/dynamic';

const SystemsPage = dynamic(() => import('@/components/systems_renderer'), {
  ssr: false,
});

function CircleRadius(x : number, y : number) {
    return Math.sqrt(x * x + y * y);
}

const WAYPOINT_COLORS : Record<string, string> = {
    'PLANET': '#3FA34D',                  // Earth-like green, natural and prominent
    'GAS_GIANT': '#1E90FF',               // Deep sky blue, massive and vibrant
    'MOON': '#AAAAAA',                    // Pale grey, muted but distinct
    'ORBITAL_STATION': '#CCCCFF',         // Soft blue-grey, industrial and visible
    'JUMP_GATE': '#FF69B4',               // Hot pink, sci-fi energy feel
    'ASTEROID_FIELD': '#8B7D7B',          // Dusty brown-grey, cluttered zone feel
    'ASTEROID': '#6E6E6E',                // Solid dark grey
    'ENGINEERED_ASTEROID': '#FFB347',     // Orange-tan, shows artificial tampering
    'ASTEROID_BASE': '#B5651D',           // Rich brown, grounded and hidden
    'NEBULA': '#8A2BE2',                  // Deep violet, gaseous glow
    'DEBRIS_FIELD': '#808080',            // Neutral grey, floating junk
    'GRAVITY_WELL': '#00CED1',            // Bright cyan, intense pull
    'ARTIFICIAL_GRAVITY_WELL': '#7FFFD4', // Aquamarine, techy gravity zone
    'FUEL_STATION': '#FFD700',            // Bright gold, quick recognition
    'ORBITAL': '#A0C4FF',                 // Soft light blue, general orbit marker
}

export default function SpaceTradersDashboard() {
    return (<SystemsPage />);
}