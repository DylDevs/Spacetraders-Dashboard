import { Stage, Layer, Circle, Text } from 'react-konva';
import { GetSystems } from '@/components/webserver';
import React, { useEffect, useRef, useState } from 'react';
import Loading from '@/components/loading';
import { Card } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';

class System {
  symbol: string;
  x: number;
  y: number;
  agent: string | null;
  type: string;
  color: string;

  constructor({ symbol, type, x, y, agent }: any) {
    this.symbol = symbol;
    this.x = x;
    this.y = y;
    this.agent = agent;
    this.type = type;
    // Hardcoded color for now
    this.color = '#FFFFFF';
  }
}

const SYSTEM_CIRCLE_RADIUS = 25;
const ZOOM_SCALE = 1.15;
const ZOOM_MIN_SCALE = 0.005;
const ZOOM_MAX_SCALE = 2;

function FormatType(type : string) {
    /*
    This function formats the type of the system
    Foe example: 'NEUTRON_STAR' -> 'Neutron Star'
    */
    return type.toLowerCase().replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function Renderer() {
  const [selected_system, setSelectedSystem] = useState<System | null>(null);
  const [systems, setSystems] = useState<System[]>([]);
  const stageRef = useRef<any>(null);
  const [scale, setScale] = useState(0.01);
  const [position, setPosition] = useState({ x: window.innerWidth / 2, y: window.innerHeight / 2 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await GetSystems();
        setSystems(result.map((system: any) => new System(system)));
      } catch (error) {
        console.error('Error fetching systems:', error);
      }
      setLoading(false);
    };

    fetchData();
  }, []);

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

  function SelectedSystemCard() {
    return (
      <Card className='flex flex-col w-full h-full'>
        {selected_system ? (
          <div>
            <h2 className='text-xl font-bold text-center mt-3'>{selected_system.symbol}</h2>
            <p className='text-center text-sm text-zinc-500 my-2'>{FormatType(selected_system.type)}</p>
            <Separator className='w-10/12 mx-auto' />
            <div className='flex flex-col space-y-2 m-3'>
              <span className='text-md text-muted-foreground space-x-1'>
                <a className='font-bold text-white'>Coordinates: </a>
                {selected_system.x}, {selected_system.y}
              </span>
              <span className='text-md text-muted-foreground space-x-1'>
                <a className='font-bold text-white'>Agent: </a>
                {selected_system.agent ? selected_system.agent : 'Nobody'}
              </span>
            </div>
            <h2 className='text-sm text-zinc-500 text-center mt-3'>More coming soon...</h2>
          </div>
        ) : (
          <div>
            <h2 className='text-xl font-bold text-center my-3'>No system selected</h2>
            <Separator className='w-10/12 mx-auto' />
            <p className='text-center text-sm text-zinc-500 mt-3'>Click a system on the map to see its details</p>
          </div>
        )}
      </Card>
    )
  }

  if (loading) {
    return (
      <div className='w-full h-full flex items-center justify-center'>
        <Loading loading_text="Loading systems..." />
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
          {systems.map((system, index) => (
            <React.Fragment key={index}>
              <Circle
                x={system.x}
                y={system.y}
                radius={SYSTEM_CIRCLE_RADIUS}
                fill={system.color}
                onClick={(e) => { setSelectedSystem(system) }}
              />
              {system.agent && scale > 0.1 && (
                <Text
                  x={system.x + SYSTEM_CIRCLE_RADIUS + 15}
                  y={system.y - SYSTEM_CIRCLE_RADIUS}
                  text={system.agent}
                  fontSize={50}
                  fill="white"
                />
              )}
            </React.Fragment>
          ))}
        </Layer>
      </Stage>
      {/* Make the selected system card show in top-left corner below the top bar */}
      <div className="absolute top-20 left-4 z-10 w-full h-full pointer-events-none">
        <div className="w-1/6 h-1/2 pointer-events-auto">
          <SelectedSystemCard />
        </div>
      </div>
    </div>
  );
}

export default Renderer;
