import { Stage, Layer, Circle, Text, Rect } from 'react-konva';
import { GetWaypoints } from '@/components/webserver';
import React, { useEffect, useRef, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import Loading from '@/components/loading';

class Waypoint {
  symbol: string;
  x: number;
  y: number;
  orbitals: {x: number, y: number}[];
  type: string;
  color: string;

  constructor({ symbol, type, x, y, orbitals }: any) {
    this.symbol = symbol;
    this.x = x;
    this.y = y;
    this.orbitals = orbitals;
    this.type = type;
    // Hardcoded color for now
    this.color = '#FFFFFF';
  }
}

const WAYPOINT_CIRCLE_RADIUS = 5;
const WAYPOINT_ORBITAL_RADIUS = 2;
const ZOOM_SCALE = 1.1;
const ZOOM_MIN_SCALE = 0.3;
const ZOOM_MAX_SCALE = 6;

function OrbitRingRadius(x : number, y : number) {
    return Math.sqrt(x * x + y * y);
}

function FormatType(type : string) {
    /*
    This function formats the type of the waypoint
    Foe example: 'GAS_GIANT' -> 'Gas Giant'
    */
    return type.toLowerCase().replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function Renderer() {
  const [selected_waypoint, setSelectedWaypoint] = useState<Waypoint | null>(null);
  const [system_symbol, setSystemSymbol] = useState<string>("");
  const [waypoints, setWaypoints] = useState<Waypoint[]>([]);
  const stageRef = useRef<any>(null);
  const [scale, setScale] = useState(0.5);
  const [position, setPosition] = useState({ x: window.innerWidth / 2, y: window.innerHeight / 2 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await GetWaypoints();
        setWaypoints(result.waypoints.map((system: any) => new Waypoint(system)));
        setSystemSymbol(result.symbol);
      } catch (error) {
        console.error('Error fetching systems:', error);
      }
      setLoading(false);
    };

    fetchData();
  }, []);

  function SelectedWaypointCard() {
    return (
      <Card className='flex flex-col w-full h-full'>
        {selected_waypoint ? (
          <div>
            <h2 className='text-xl font-bold text-center mt-3'>{selected_waypoint.symbol}</h2>
            <p className='text-center text-sm text-zinc-500 my-2'>{FormatType(selected_waypoint.type)}</p>
            <Separator className='w-10/12 mx-auto' />
            <div className='flex flex-col space-y-2 m-3'>
              <span className='text-md text-muted-foreground space-x-1'>
                <a className='font-bold text-white'>Coordinates: </a>
                {selected_waypoint.x}, {selected_waypoint.y}
              </span>
              <span className='text-md text-muted-foreground space-x-1'>
                <a className='font-bold text-white'>Orbitals: </a>
                {selected_waypoint.orbitals.length}
              </span>
            </div>
            <h2 className='text-sm text-zinc-500 text-center mt-3'>More coming soon...</h2>
          </div>
        ) : (
          <div>
            <h2 className='text-xl font-bold text-center my-3'>No waypoint selected</h2>
            <Separator className='w-10/12 mx-auto' />
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

    if (newScale < ZOOM_MIN_SCALE || newScale > ZOOM_MAX_SCALE) {
      return;
    }

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

  if (loading) {
    return (
      <div className='w-full h-full flex items-center justify-center'>
        <Loading loading_text="Loading waypoints..." />
      </div>
    )
  }

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
        <div className="w-1/6 h-1/2 pointer-events-auto">
          <SelectedWaypointCard />
        </div>
      </div>
    </div>
  );
}

export default Renderer;