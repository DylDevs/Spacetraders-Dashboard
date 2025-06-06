import { Stage, Layer, Circle, Text, Rect } from 'react-konva';
import { GetWaypoints } from '@/components/webserver';
import React, { useEffect, useRef, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';

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

class Waypoint {
  symbol: string;
  x: number;
  y: number;
  orbitals: {x: number, y: number}[];
  color: string;

  constructor({ symbol, type, x, y, orbitals }: any) {
    this.symbol = symbol;
    this.x = x;
    this.y = y;
    this.orbitals = orbitals;
    this.color = WAYPOINT_COLORS[type] || '#FFFFFF';
  }
}
const WAYPOINT_CIRCLE_RADIUS = 5;
const WAYPOINT_ORBITAL_RADIUS = 2;
const ZOOM_SCALE = 1.1;

function OrbitRingRadius(x : number, y : number) {
    return Math.sqrt(x * x + y * y);
}

function Renderer() {
  const [selected_waypoint, setSelectedWaypoint] = useState<Waypoint | null>(null);
  const [system_symbol, setSystemSymbol] = useState<string>("");
  const [waypoints, setWaypoints] = useState<Waypoint[]>([]);
  const stageRef = useRef<any>(null);
  const [scale, setScale] = useState(0.5);
  const [position, setPosition] = useState({ x: window.innerWidth / 2, y: window.innerHeight / 2 });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await GetWaypoints();
        setWaypoints(result.waypoints.map((system: any) => new Waypoint(system)));
        setSystemSymbol(result.symbol);
      } catch (error) {
        console.error('Error fetching systems:', error);
      }
    };

    fetchData();
  }, []);

  function SelectedWaypointCard() {
    return (
      <Card className='flex flex-col w-1/6 h-1/2'>
        {selected_waypoint ? (
          <div>
            <h2 className='text-xl font-bold text-center my-3'>{selected_waypoint.symbol}</h2>
            <Separator className='mx-[20px] w-[calc(100%-40px)]' />
          </div>
        ) : (
          <div>
            <h2 className='text-xl font-bold text-center my-3'>No waypoint selected</h2>
            <Separator className='mx-[20px] w-[calc(100%-40px)]' />
            <p className='text-center text-sm text-zinc-500 mt-3'>Click a waypoint on the map to see its details</p>
          </div>
        )}
      </Card>
    )
  }

  const handleWheel = (e: any) => {
    e.evt.preventDefault();

    const stage = stageRef.current;
    const oldScale = scale;
    const pointer = stage.getPointerPosition();
    const direction = e.evt.deltaY > 0 ? 1 : -1;
    const newScale = direction > 0 ? oldScale / ZOOM_SCALE : oldScale * ZOOM_SCALE;

    const mousePointTo = {
      x: (pointer.x - position.x) / oldScale,
      y: (pointer.y - position.y) / oldScale,
    };

    const newPos = {
      x: pointer.x - mousePointTo.x * newScale,
      y: pointer.y - mousePointTo.y * newScale,
    };

    setScale(newScale);
    setPosition(newPos);
  };

  return (
    <div className='w-full h-full'>
      <Stage
        ref={stageRef}
        width={window.innerWidth}
        height={window.innerHeight}
        draggable
        x={position.x}
        y={position.y}
        scale={{ x: scale, y: scale }}
        onDragEnd={(e) => {
          setPosition({ x: e.target.x(), y: e.target.y() });
        }}
        onWheel={handleWheel}
      >
        <Layer>
          {/* Render the orbit rings before the waypoints to prevent overlapping */}
          {waypoints.map((system, index) => (
            <Circle
                x={0}
                y={0}
                radius={OrbitRingRadius(system.x, system.y)}
                fill="transparent"
                stroke={"#FFFFFF30"}
                strokeWidth={0.2}
              />
          ))}
          {waypoints.map((system, index) => (
            <React.Fragment key={index}>
              <Circle
                x={system.x}
                y={system.y}
                radius={WAYPOINT_CIRCLE_RADIUS}
                fill={system.color}
                onClick={() => setSelectedWaypoint(system)}
              />
              {system.orbitals.map((orbital, index) => (
                <Circle
                  key={index}
                  x={orbital.x}
                  y={orbital.y}
                  radius={WAYPOINT_ORBITAL_RADIUS}
                  fill={system.color}
                />
              ))}
            </React.Fragment>
          ))}
        </Layer>
      </Stage>
      {/* Make the selected waypoint card show in top-left corner below the top bar */}
      <div className="absolute top-20 left-4 z-10 w-full h-full pointer-events-none">
        <div className="w-full h-fullpointer-events-auto">
          <SelectedWaypointCard />
        </div>
      </div>
    </div>
  );
}

export default Renderer;